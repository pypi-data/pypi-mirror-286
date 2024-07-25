# Install script for directory: /home/amit/Projects/FERMAT/KLIFF_Serve/kliff_serve/kusp/KUSP__MO_000000000000_000

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}/opt/kim_api/install/libexec/kim-api/../../lib/kim-api/portable-models/KUSP__MO_000000000000_000/libkim-api-portable-model.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/opt/kim_api/install/libexec/kim-api/../../lib/kim-api/portable-models/KUSP__MO_000000000000_000/libkim-api-portable-model.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}/opt/kim_api/install/libexec/kim-api/../../lib/kim-api/portable-models/KUSP__MO_000000000000_000/libkim-api-portable-model.so"
         RPATH "")
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/opt/kim_api/install/libexec/kim-api/../../lib/kim-api/portable-models/KUSP__MO_000000000000_000/libkim-api-portable-model.so")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/opt/kim_api/install/libexec/kim-api/../../lib/kim-api/portable-models/KUSP__MO_000000000000_000" TYPE MODULE FILES "/home/amit/Projects/FERMAT/KLIFF_Serve/kliff_serve/kusp/KUSP__MO_000000000000_000/build/libkim-api-portable-model.so")
  if(EXISTS "$ENV{DESTDIR}/opt/kim_api/install/libexec/kim-api/../../lib/kim-api/portable-models/KUSP__MO_000000000000_000/libkim-api-portable-model.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/opt/kim_api/install/libexec/kim-api/../../lib/kim-api/portable-models/KUSP__MO_000000000000_000/libkim-api-portable-model.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}/opt/kim_api/install/libexec/kim-api/../../lib/kim-api/portable-models/KUSP__MO_000000000000_000/libkim-api-portable-model.so"
         OLD_RPATH "/opt/kim_api/install/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}/opt/kim_api/install/libexec/kim-api/../../lib/kim-api/portable-models/KUSP__MO_000000000000_000/libkim-api-portable-model.so")
    endif()
  endif()
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/amit/Projects/FERMAT/KLIFF_Serve/kliff_serve/kusp/KUSP__MO_000000000000_000/build/yaml-cpp/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/amit/Projects/FERMAT/KLIFF_Serve/kliff_serve/kusp/KUSP__MO_000000000000_000/build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
