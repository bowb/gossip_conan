cmake_minimum_required(VERSION 3.28)
project(test_package LANGUAGES C CXX)

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
