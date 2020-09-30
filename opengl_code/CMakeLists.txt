cmake_minimum_required(VERSION 3.10)

project(foo VERSION 1.0)

set(CMAKE_CXX_STANDARD 11)

message(${CMAKE_HOST_SYSTEM})


find_package(Boost 1.72.0 COMPONENTS locale)
find_package(OpenCV)
find_package(glfw3  REQUIRED)
#find_package(OpenGL REQUIRED)
find_package(GLEW 2.2.0 REQUIRED)




message(${CMAKE_CURRENT_SOURCE_DIR})
message(${OPENGL_gl_LIBRARY})
#include_directories(${GLEW_INCLUDE_DIRS})
include_directories(${Boost_INCLUDES_DIRS})
include_directories(${GLFW_INCLUDES_DIRS})
include_directories(${OPENGL_INCLUDE_DIR}$)
add_executable(opengl main.cpp)
target_link_libraries(opengl glfw GLEW::GLEW) # ${OPENGL_gl_LIBRARY})







#find_library(BOOST_LIBRARY 
#	NAMES libboost_locale-mt.a
#	PATHS /usr/local/Cellar/boost/1.72.0_3/lib)
#find_path(BOOST_INCLUDES 
#	  	 boost/locale.hpp 
#		 boost/algorithm/string/case_conv.hpp
#		 /usr/local/Cellar/boost/1.72.0_3/include)
