cmake_minimum_required(VERSION 3.20)
project(test_package LANGUAGES C CXX)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -fPIC")
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(glog 0.7.0 REQUIRED)
find_package(Protobuf REQUIRED)
find_package(gossip REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
set_target_properties(${PROJECT_NAME} PROPERTIES LINKER_LANGUAGE CXX)
if(TARGET gossip-static)
    target_link_libraries(${PROJECT_NAME} PRIVATE protobuf::libprotobuf glog::glog gossip-static)
else()
    target_link_libraries(${PROJECT_NAME} PRIVATE protobuf::libprotobuf glog::glog gossip)
endif()
