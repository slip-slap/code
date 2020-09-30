cmake_minimum_required(VERSION 3.10)

project(foo VERSION 1.0)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Werror -std=c++14")
message(${PROJECT_SOURCE_DIR})
message(${CMAKE_CURRENT_BINARY_DIR})


find_package(Boost 1.72.0 COMPONENTS locale)
find_package(OpenCV)


message(${CMAKE_CURRENT_SOURCE_DIR})
message(${OpenCV_INCLUDE_DIRS})
include_directories(${Boost_INCLUDES_DIRS})
add_executable(demo main.cpp)
target_link_libraries(demo ${Boost_LIBRARIES})





#find_library(BOOST_LIBRARY 
#	NAMES libboost_locale-mt.a
#	PATHS /usr/local/Cellar/boost/1.72.0_3/lib)
#find_path(BOOST_INCLUDES 
#	  	 boost/locale.hpp 
#		 boost/algorithm/string/case_conv.hpp
#		 /usr/local/Cellar/boost/1.72.0_3/include)
