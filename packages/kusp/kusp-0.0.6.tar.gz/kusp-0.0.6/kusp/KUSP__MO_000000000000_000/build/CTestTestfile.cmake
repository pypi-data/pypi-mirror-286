# CMake generated Testfile for 
# Source directory: /home/amit/Projects/FERMAT/KLIFF_Serve/kliff_serve/kusp/KUSP__MO_000000000000_000
# Build directory: /home/amit/Projects/FERMAT/KLIFF_Serve/kliff_serve/kusp/KUSP__MO_000000000000_000/build
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(shared_library_test_KUSP__MO_000000000000_000 "/opt/kim_api/install/libexec/kim-api/kim-api-shared-library-test" "/home/amit/Projects/FERMAT/KLIFF_Serve/kliff_serve/kusp/KUSP__MO_000000000000_000/build/libkim-api-portable-model.so")
set_tests_properties(shared_library_test_KUSP__MO_000000000000_000 PROPERTIES  _BACKTRACE_TRIPLES "/opt/kim_api/install/share/cmake/kim-api-items/kim-api-items-macros.cmake;723;add_test;/opt/kim_api/install/share/cmake/kim-api-items/kim-api-items-macros.cmake;815;add_kim_api_test;/opt/kim_api/install/share/cmake/kim-api-items/kim-api-items-macros.cmake;111;_add_kim_api_library;/home/amit/Projects/FERMAT/KLIFF_Serve/kliff_serve/kusp/KUSP__MO_000000000000_000/CMakeLists.txt;33;add_kim_api_model_library;/home/amit/Projects/FERMAT/KLIFF_Serve/kliff_serve/kusp/KUSP__MO_000000000000_000/CMakeLists.txt;0;")
subdirs("yaml-cpp")
