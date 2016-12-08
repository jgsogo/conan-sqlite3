from conans import ConanFile
import os, shutil
from conans.tools import download, untargz, check_sha1
from conans import CMake

class SQLite3Conan(ConanFile):
    name = "sqlite3"
    version = "3.15.2"
    license = "Public domain"
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"
    url="http://github.com/jgsogo/conan-sqlite3"
    ZIP_FOLDER_NAME = "sqlite-autoconf-3150200"
    exports = ["FindSQLite3.cmake", "CMakeLists.txt", ]

    _build_dir = "build"

    def source(self):
        zip_name = "sqlite-autoconf-3150200.tar.gz"
        download("http://www.sqlite.org/2016/%s" % zip_name, zip_name)
        #check_sha1(zip_name, "ea8c25abc33733ec3541be2affe41b804b08c5ca")
        untargz(zip_name)
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self.settings)
        shutil.move("CMakeLists.txt", "%s/CMakeLists.txt" % self.ZIP_FOLDER_NAME)
        self.run("mkdir {}".format(self._build_dir))
        
        command = "cd {} && cmake ../{} {}".format(self._build_dir, self.ZIP_FOLDER_NAME, cmake.command_line)
        self.output.info(command)
        self.run(command)

        command = "cd {} && cmake --build . {}".format(self._build_dir, cmake.build_config)
        self.output.info(command)
        self.run(command)

    def package(self):
        self.copy("FindSQLite3.cmake", ".", ".")
        self.copy("*.h", dst="include", src=self.ZIP_FOLDER_NAME)
        if self.settings.os == "Windows":
            self.copy(pattern="*.lib", dst="lib", src=self._build_dir)
            self.copy(pattern="*.dll", dst="bin", src=self._build_dir)
        else:
            self.copy(pattern="*.a", dst="lib", src=self._build_dir)
            self.copy(pattern="*.lib", dst="lib", src=self._build_dir)
            self.copy(pattern="*.pdb", dst="lib", src=self._build_dir)

    def package_info(self):
        self.cpp_info.libs = ['sqlite3']
        if not self.settings.os == "Windows":
            self.cpp_info.libs.append("pthread")
            self.cpp_info.libs.append("dl")

