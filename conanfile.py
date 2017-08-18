from conans import ConanFile, CMake, os, tools


class AzureUMQTTCConan(ConanFile):
    name = "Azure-uMQTT-C"
    version = "1.0.41"
    generators = "cmake" 
    settings = "os", "arch", "compiler", "build_type"
    url = "https://github.com/bincrafters/conan-azure-umqtt-c"
    source_url = "https://github.com/Azure/azure-umqtt-c"
    git_tag = "2017-08-11"
    description = "General purpose library for communication over the mqtt protocol"
    license = "https://github.com/Azure/azure-iot-sdk-c/blob/master/LICENSE"
    lib_short_name = "azure-umqtt-c"
    build_requires = "Azure-CTest/1.1.0@bincrafters/testing", \
                        "Azure-C-Testrunnerswitcher/1.1.0@bincrafters/testing", \
                        "uMock-C/1.1.0@bincrafters/testing"
    requires = "Azure-C-Shared-Utility/1.0.41@bincrafters/testing"
    
    
    def source(self):
        # Despite using conan dependencies, doing recursive clone because of
        # Source level dependency on sharedutil cmake file :(
        self.run("git clone --depth=1 --branch={0} {1}.git"
                .format(self.git_tag, self.source_url))                
                
        utility_root = self.deps_cpp_info["Azure-C-Shared-Utility"].rootpath
        
        #cmake_includes = ""
        for resdir in self.deps_cpp_info["Azure-C-Shared-Utility"].resdirs:
            cmake_include_dir = os.path.join(utility_root, resdir)
            cmake_includes = '\n'.join('include("' + os.path.join(cmake_include_dir, file) + '")' \
                    for file in os.listdir(cmake_include_dir) \
                            if file.endswith('.cmake'))
         
        cmake_lists_path = os.path.join(self.lib_short_name,"CMakeLists.txt")
        cmake_contents_orig = tools.load(cmake_lists_path)
        
        cmake_contents_new = "include(../conanbuildinfo.cmake)\n" \
            + cmake_includes + "\n" \
            + 'MESSAGE( STATUS "CONAN_LIBS:         " ${CONAN_LIBS} )' + "\n" \
            + cmake_contents_orig \
            .replace("target_link_libraries(umqtt aziotsharedutil)", \
                        "target_link_libraries(umqtt $CONAN_LIBS)") \
            .replace("add_subdirectory(add_subdirectory(deps/azure-c-testrunnerswitcher))","") \
            .replace("add_subdirectory(deps/umock-c)","") \
            .replace("include(\"dependencies.cmake\")","") \
            .replace("include(\"dependencies-test.cmake\")","")
            #.replace("add_subdirectory(deps/azure-ctest)","") \
                           
        tools.save(cmake_lists_path, cmake_contents_new)

    def build(self):
        
        cmake = CMake(self)
        cmake.definitions["use_installed_dependencies"] = "ON"
        cmake.configure(source_dir=self.lib_short_name, build_dir="./")
        cmake.build()
        
    def package(self):
        include_dir = os.path.join(
            self.lib_short_name, "inc", self.lib_short_name.replace("-","_"))
            
        self.copy(pattern="*", dst="include", src="include_dir")		
        self.copy(pattern="*.lib", dst="lib", src="")

    def package_info(self):
        self.cpp_info.libs = self.collect_libs()

