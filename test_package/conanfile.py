from conans import ConanFile, CMake
import os

class AzureumqttcTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    user = os.getenv("CONAN_USERNAME", "bincrafters")
    channel = os.getenv("CONAN_CHANNEL", "testing")
    requires = "Azure-uMQTT-C/1.0.41@%s/%s" % (user, channel)

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir=self.conanfile_directory, build_dir="./")
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")

    def test(self):
        os.chdir("bin")
        app_name = "mqtt_client_sample"
        if platform.os == "Windows":
            app_name += ".exe"
        assert(os.path.isfile(app_name))
