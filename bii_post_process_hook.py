#print bii

import os
import platform

install_folder = os.path.join(bii.environment_folder, "opencv/3.0/")

if platform.system() == "Windows":
	if not os.path.exists(install_folder):
		filename = "opencv-3.0.exe"
		url = "http://sourceforge.net/projects/opencvlibrary/files/opencv-win/3.0.0-beta/opencv-3.0.0-beta.exe/download"
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
		filename = "opencv-3.0.zip"
		url = "https://github.com/Itseez/opencv/archive/3.0.0-beta.zip"
		filepath = os.path.join(bii.environment_folder, filename)
		if not os.path.exists(filepath):
			bii.download(url, filepath)

		if not os.path.exists(install_folder):
			os.makedirs(install_folder)
		os.system('unzip %s -d %s' % (filepath, install_folder))
		os.system('mv %s/opencv-3.0.0-beta %s' % (install_folder, sources_folder))
	build_folder = os.path.join(install_folder, "build")
	if not os.path.exists(build_folder):
		os.makedirs(build_folder)
		os.chdir(build_folder)
		cmake_flags=" -DBUILD_EXAMPLES=OFF -DBUILD_DOCS=OFF -DBUILD_TESTS=OFF -DBUILD_opencv_apps=OFF -DBUILD_PERF_TESTS=OFF"
		if platform.system() != "Darwin":
			os.system('sudo apt-get install libgtk2.0-dev pkg-config')
			os.system('cmake ../sources %s' % (cmake_flags))
		else:
			os.system('cmake -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ ../sources %s' % (cmake_flags))
		os.system('make -j4')
