from os import path
from conans import ConanFile, CMake, tools


class AzureUMQTTCConan(ConanFile):
    name = "Azure-uMQTT-C"
    version = "1.0.46"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    url = "https://github.com/bincrafters/conan-azure-umqtt-c"
    description = "General purpose library for communication over the mqtt protocol"
    license = "https://github.com/Azure/azure-umqtt-c/blob/master/LICENSE"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    lib_short_name = "umqtt"
    release_date = "2017-10-20"
    release_name = "%s-%s" % (name.lower(), release_date)
    requires = "Azure-C-Shared-Utility/1.0.46@bincrafters/stable"

    def source(self):
        source_url = "https://github.com/Azure/azure-umqtt-c"
        tools.get("%s/archive/%s.tar.gz" % (source_url, self.release_date))

    def configure(self):
        del self.settings.compiler.libcxx

    def build(self):
        conan_magic_lines='''project(%s)
        include(../conanbuildinfo.cmake)
        conan_basic_setup()
        ''' % self.lib_short_name
        cmake_file = "%s/CMakeLists.txt" % self.release_name
        res_paths = self.deps_cpp_info["Azure-C-Shared-Utility"].res_paths[0]
        if self.settings.os == "Windows":
            res_paths = res_paths.replace("\\", "/")
        tools.replace_in_file(cmake_file, "project(%s)" % self.lib_short_name, conan_magic_lines)
        conan_magic_lines = "include(%s/deps/c-utility/configs/azure_iot_build_rules.cmake)" % res_paths
        tools.replace_in_file(cmake_file, "include(deps/c-utility/configs/azure_iot_build_rules.cmake)", conan_magic_lines)
        content = tools.load(cmake_file)
        tools.save(cmake_file, content[0:content.find("if(${use_installed_dependencies})")])
        conan_magic_lines = '''    find_package(azure_c_shared_utility REQUIRED CONFIG
        HINTS %s/deps/c-utility/configs/)''' % res_paths
        tools.replace_in_file("%s/dependencies.cmake" % self.release_name, "    find_package(azure_c_shared_utility REQUIRED CONFIG)", conan_magic_lines)
        cmake = CMake(self)
        cmake.definitions["skip_samples"] = True
        cmake.definitions["use_installed_dependencies"] = True
        if self.settings.os == "Windows" and self.options.shared:
            cmake.definitions["CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS"] = True
        cmake.configure(source_dir=self.release_name)
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst=".", src=".")
        self.copy(pattern="*", dst="include", src=path.join(self.release_name, "inc"))
        self.copy(pattern="umqttConfig.cmake", dst="res", src=path.join(self.release_name, "configs"))
        self.copy(pattern="*.cmake", dst="res", src=path.join("CMakeFiles", "Export", "cmake"))
        self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src=".", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", src=".", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
