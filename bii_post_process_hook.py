#print bii

import os
import platform

install_folder = os.path.join(bii.environment_folder, "opencv/2.4.10/")

if platform.system() == "Windows":
    if not os.path.exists(install_folder):
        filename = "opencv-2.4.10.exe"
        url = "http://sourceforge.net/projects/opencvlibrary/files/opencv-win/2.4.10/opencv-2.4.10.exe/download"
        filepath = os.path.join(bii.environment_folder, filename)
        if not os.path.exists(filepath):
            bii.download(url, filepath)
        os.system('%s -o"%s" -y' % (filepath, bii.environment_folder))
        os.makedirs(install_folder)
        os.system('move %s/opencv/build %s/build' % (bii.environment_folder, install_folder))
        os.system('move %s/opencv/sources %s/sources' % (bii.environment_folder, install_folder))
else:
    sources_folder = os.path.join(install_folder, "sources")
    if not os.path.exists(sources_folder):
        filename = "opencv-2.4.10.zip"
        url = "http://sourceforge.net/projects/opencvlibrary/files/opencv-unix/2.4.10/opencv-2.4.10.zip/download"
        filepath = os.path.join(bii.environment_folder, filename)
        if not os.path.exists(filepath):
            bii.download(url, filepath)
        if not os.path.exists(install_folder):
            os.makedirs(install_folder)
        os.system('unzip %s -d %s' % (filepath, install_folder))
        os.system('mv %s/opencv-2.4.10 %s' % (install_folder, sources_folder))
    build_folder = os.path.join(install_folder, "build")
    if not os.path.exists(build_folder):
        os.makedirs(build_folder)
        os.chdir(build_folder)
        # These flags are to disable compiling many targets that are not libs, not required by the user
        cmake_flags=" -DBUILD_EXAMPLES=OFF -DBUILD_DOCS=OFF -DBUILD_TESTS=OFF -DBUILD_opencv_apps=OFF -DBUILD_PERF_TESTS=OFF"
        osinfo = platform.system()
        bii.out.info("OS: %s" % osinfo)
        cmake_file_path = os.path.join(bii.environment_folder, "cmake_path")
        if os.path.exists(cmake_file_path):
            with open(cmake_file_path, "r") as f:
                cmake_path = f.read().strip()
                os.environ["PATH"] += os.pathsep + cmake_path
        if osinfo == 'Linux':            
            dist = platform.linux_distribution()[0]
            bii.out.info("Detected Linux...")
            if dist in ("Ubuntu", "debian"):
                bii.out.info("Ubuntu/Debian compiling...")
                os.system('sudo apt-get install libgtk2.0-dev pkg-config')
            elif dist in ("Fedora", "CentOS"):
                bii.out.info("Fedora/Centos compiling...")
                os.system('sudo yum install gtk+-devel gtk2-devel')
            else:
                bii.out.error("Error, linux distribution not supported: %s" % dist)
            os.system('cmake ../sources %s' % (cmake_flags))
        elif osinfo == 'Darwin':
            bii.out.info("OSx compiling...")
            os.system('cmake -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ ../sources %s' % (cmake_flags))
        else:
            bii.out.error("%s not supported!!!" % osinfo)

        os.system('make -j4')
