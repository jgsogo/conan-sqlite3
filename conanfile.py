from conans import ConanFile
import os, shutil
from conans.tools import download, unzip, check_sha1
from conans import CMake

class SQLite3Conan(ConanFile):
    name = "sqlite3"
    version = "3.14.1"
    license = "Public domain"
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"
    url="http://github.com/rdeterre/conan-sqlite3"
    exports = ["CMakeLists.txt"]
    ZIP_FOLDER_NAME = "sqlite-amalgamation-3140100"

    def source(self):
        zip_name = "sqlite-amalgamation-3140100.zip"
        download("http://www.sqlite.org/2016/%s" % zip_name, zip_name)
        check_sha1(zip_name, "ea8c25abc33733ec3541be2affe41b804b08c5ca")
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        shutil.move("CMakeLists.txt", "%s/CMakeLists.txt" % self.ZIP_FOLDER_NAME)
        cmake = CMake(self.settings)
        self.run("mkdir _build")
        self.run('cd _build && cmake ../%s %s' % (self.ZIP_FOLDER_NAME, cmake.command_line))
        self.run("cd _build && cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", "include", "%s" % (self.ZIP_FOLDER_NAME), keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="_build", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src="_build", keep_path=False)
        self.copy(pattern="*.pdb", dst="lib", src="_build", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['sqlite3']
        if not self.settings.os == "Windows":
            self.cpp_info.libs.append("pthread")
            self.cpp_info.libs.append("dl")
