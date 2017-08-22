from conans import ConanFile, CMake, os, tools
import shutil


class AzureUMQTTCConan(ConanFile):
    name = "Azure-uMQTT-C"
    version = "1.0.41"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    url = "https://github.com/bincrafters/conan-azure-umqtt-c"
    source_url = "https://github.com/Azure/azure-umqtt-c"
    description = "General purpose library for communication over the mqtt protocol"
    license = "https://github.com/Azure/azure-iot-sdk-c/blob/master/LICENSE"
    lib_short_name = "azure-umqtt-c"
    release_date = "2017-08-11"
    requires = "Azure-C-Shared-Utility/%s@bincrafters/testing" % version
    release_name = "%s-%s" % (name.lower(), release_date)
    exports = ["azure_c_shared_utilityConfig.cmake"]

    def source(self):
        tools.get("https://github.com/Azure/azure-umqtt-c/archive/%s.tar.gz" % self.release_date)

    def build(self):
        conan_magic_lines='''project(umqtt)
        include(../conanbuildinfo.cmake)
        conan_basic_setup()
        '''
        tools.replace_in_file("%s/CMakeLists.txt" % self.release_name, "project(umqtt)", conan_magic_lines)
        cmake = CMake(self)
        cmake.definitions["use_installed_dependencies"] = True
        cmake.definitions["skip_samples"] = True
        cmake.definitions["azure_c_shared_utility_DIR"] = self.deps_cpp_info["Azure-C-Shared-Utility"].res_paths[0]
        cmake.configure(source_dir=self.release_name)
        cmake.build()

    def package(self):
        include_dir = os.path.join(
            self.lib_short_name, "inc", self.lib_short_name.replace("-","_"))

        self.copy(pattern="*", dst="include", src="include_dir")
        self.copy(pattern="*.lib", dst="lib", src="")

    def package_info(self):
        self.cpp_info.libs = self.collect_libs()
