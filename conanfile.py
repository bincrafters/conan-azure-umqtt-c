from os import path
from conans import ConanFile, CMake, tools


class AzureUMQTTCConan(ConanFile):
    name = "Azure-uMQTT-C"
    version = "1.0.43"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    url = "https://github.com/bincrafters/conan-azure-umqtt-c"
    description = "General purpose library for communication over the mqtt protocol"
    license = "https://github.com/Azure/azure-umqtt-c/blob/master/LICENSE"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    lib_short_name = "umqtt"
    release_date = "2017-09-08"
    release_name = "%s-%s" % (name.lower(), release_date)
<<<<<<< HEAD
    requires = "Azure-C-Shared-Utility/1.0.43@bincrafters/testing"
=======
    requires = "Azure-C-Shared-Utility/1.0.43@bincrafters/stable"
>>>>>>> stable/1.0.43
    
    def source(self):
        source_url = "https://github.com/Azure/azure-umqtt-c"
        tools.get("%s/archive/%s.tar.gz" % (source_url, self.release_date))
<<<<<<< HEAD

=======
        
>>>>>>> stable/1.0.43
    def configure(self):
        # TODO: static library fails on Linux    
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            self.options.shared = False

        if self.settings.os == "Linux":
            self.options.shared = True

    def build(self):
        conan_magic_lines='''project(%s)
        include(../conanbuildinfo.cmake)
        conan_basic_setup()
        ''' % self.lib_short_name
        
        cmake_file = "%s/CMakeLists.txt" % self.release_name
        tools.replace_in_file(cmake_file, "project(%s)" % self.lib_short_name, conan_magic_lines)
        content = tools.load(cmake_file)
        tools.save(cmake_file, content[0:content.find("if(${use_installed_dependencies})")])
        cmake = CMake(self)
        cmake.definitions["skip_samples"] = True
        cmake.definitions["use_installed_dependencies"] = True
        cmake.definitions["azure_c_shared_utility_DIR"] = self.deps_cpp_info["Azure-C-Shared-Utility"].res_paths[0]
        cmake.configure(source_dir=self.release_name)
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst=".", src=".")
        self.copy(pattern="*", dst="include", src=path.join(self.release_name, "inc"))
        self.copy(pattern="umqttConfig.cmake", dst="res", src=path.join(self.release_name, "configs"))
        self.copy(pattern="*.cmake", dst="res", src=path.join("CMakeFiles", "Export", "cmake"))
        self.copy(pattern="*.lib", dst="lib", src="lib")
        self.copy(pattern="*.dll", dst="bin", src=".")
        self.copy(pattern="*.a", dst="lib", src="lib")
        self.copy(pattern="*.so*", dst="lib", src=".")
        self.copy(pattern="*.dylib", dst="lib", src=".")

    def package_info(self):
        self.cpp_info.libs = self.collect_libs()
