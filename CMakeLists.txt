cmake_minimum_required(VERSION 3.18)
project(covariance_models)

function(add_executable_with_matplotlib basename)
    #set C++ standard to C++17
    set(CMAKE_CXX_STANDARD 17)

    if (WITH_EIGEN)
        add_definitions("-DWITH_EIGEN")
    endif()

    add_executable(${basename} ${basename}.cpp ./matplotlib-cpp/matplotlibcpp.h)
    target_link_librariers(${basename} ${Python3_LIBRARIES})
endfunction(add_executable_with_matplotlib)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH}
    "${CMAKE_SOURCE_DIR}/cmake/modules/")
enable_testing()
find_package(Eigen3 3.3 REQUIRED)
find_package(Sophus REQUIRED)
find_package(GTest REQUIRED)

if (${Eigen3_FOUND})
    message(STATUS "Eigen3 found")
endif()

if (${Sophus_FOUND})
    message(STATUS "Sophus found")
endif()

if (${GTest_FOUND})
    message(STATUS "GTest found")
endif()

find_package(Python3 COMPONENTS Interpreter Development)
if (${Python3_FOUND})
  include_directories(${Python3_INCLUDE_DIRS})
else()
  message(FATAL_ERROR "Python3 not found, please install it.")
endif()

find_package(NumPy)
if (${PYTHON_NUMPY_FOUND})
  include_directories(${PYTHON_NUMPY_INCLUDE_DIR})
else()
  message(WARNING "Python3 NumPy not found, proceeding with -DWITHOUT_NUMPY."
  " Some functions might not work.")
  add_definitions(-DWITHOUT_NUMPY)
endif()

set(LIBRARY_SOURCES
    ./src/cvm_core/stochastic_process.cpp)
include_directories(include)
add_library(cvm SHARED ${LIBRARY_SOURCES})
target_link_libraries(cvm Eigen3::Eigen Sophus::Sophus)


## Examples
add_executable(white_noise ./examples/white_noise.cpp )

## tests
set(TEST_SOURCES
    ./tests/test_stochastic_process.cpp)
add_executable(${PROJECT_NAME}_tests ${TEST_SOURCES})
target_link_libraries(${PROJECT_NAME}_tests GTest::GTest GTest::Main cvm)
target_include_directories(${PROJECT_NAME}_tests PUBLIC
                           ${GTEST_INCLUDE_DIRS}
                           ./include)
gtest_discover_tests(${PROJECT_NAME}_tests)
