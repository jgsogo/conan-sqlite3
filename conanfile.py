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
    url="http://github.com/jgsogo/conan-sqlite3"
    ZIP_FOLDER_NAME = "sqlite-amalgamation-3140100"

    def source(self):
        zip_name = "sqlite-amalgamation-3140100.zip"
        download("http://www.sqlite.org/2016/%s" % zip_name, zip_name)
        check_sha1(zip_name, "ea8c25abc33733ec3541be2affe41b804b08c5ca")
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            command = 'cd {} && ./configure && make'.format(self.ZIP_FOLDER_NAME)
        elif self.settings.os == "Windows":
            command = 'cd {} && nmake /f makefile.msc sqlite3.c'.format(self.ZIP_FOLDER_NAME)
        else:
            raise NotImplementedError("conanfile::build for settings.os {!r} not implemented".format(self.settings.os))
        self.output.info(command)
        self.run(command)

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

