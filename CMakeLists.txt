# This CMakeLists.txt file helps defining your block building and compiling
# Include the main biicode macros and functions
# To learn more about the CMake use with biicode, visit http://docs.biicode.com/c++/building.html
# Or check the examples below


include(${CMAKE_HOME_DIRECTORY}/biicode.cmake)
# Initializes block variables
INIT_BIICODE_BLOCK()

set(OpenCV_DIR "${BIICODE_ENV_DIR}/opencv/3.0/build")
FIND_PACKAGE(OpenCV REQUIRED)

# Actually create targets: EXEcutables and libraries.
ADD_BIICODE_TARGETS()

IF(WIN32)
	get_filename_component(_OpenCV_LIB_PATH "${OpenCV_LIB_PATH}/../bin" ABSOLUTE)
ELSE()
	get_filename_component(_OpenCV_LIB_PATH "${OpenCV_LIB_PATH}../bin" ABSOLUTE)
ENDIF()
file(COPY ${_OpenCV_LIB_PATH} DESTINATION ${CMAKE_SOURCE_DIR}/../ FILES_MATCHING PATTERN *.dll)

target_include_directories(${BII_LIB_TARGET} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
TARGET_LINK_LIBRARIES(${BII_LIB_TARGET} PUBLIC ${OpenCV_LIBS})
