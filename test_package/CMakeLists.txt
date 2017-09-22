#Copyright (c) Microsoft. All rights reserved.
#Licensed under the MIT license. See LICENSE file in the project root for full license information.

#this is CMakeLists.txt for test_package

cmake_minimum_required(VERSION 2.8.11)
project(azure-umqtt-c-test)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

set(CMAKE_VERBOSE_MAKEFILE ON)

set(test_package_c_files
    mqtt_client_sample.c
)

set(test_package_c_files ${test_package_c_files} main.c)

set(test_package_h_files
    mqtt_client_sample.h
)

IF(WIN32)
    #windows needs this define
    add_definitions(-D_CRT_SECURE_NO_WARNINGS)
    add_definitions(-DGB_MEASURE_MEMORY_FOR_THIS -DGB_DEBUG_ALLOC)
ENDIF(WIN32)

include_directories(.)

add_executable(test_package ${test_package_c_files} ${test_package_h_files})
set_property(TARGET test_package PROPERTY C_STANDARD 99)

if (WIN32)
    target_link_libraries(test_package
        aziotsharedutil
        umqtt
        secur32
        ws2_32)
    if(${use_openssl})
        target_link_libraries(test_package $ENV{OpenSSLDir}/lib/ssleay32.lib $ENV{OpenSSLDir}/lib/libeay32.lib)
        file(COPY $ENV{OpenSSLDir}/bin/libeay32.dll DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/Debug)
        file(COPY $ENV{OpenSSLDir}/bin/ssleay32.dll DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/Debug)
    endif()
    if(${use_wolfssl})
        target_link_libraries(test_package $ENV{WolfSSLDir}/Debug/wolfssl.lib)
    endif()
else()
    target_link_libraries(test_package
        aziotsharedutil
        pthread
        umqtt)
    #if(${use_openssl})
        target_link_libraries(test_package ${OPENSSL_LIBRARIES})
    #endif()
endif()
