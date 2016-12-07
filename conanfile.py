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

    def source(self):
        zip_name = "sqlite-autoconf-3150200.tar.gz"
        download("http://www.sqlite.org/2016/%s" % zip_name, zip_name)
        #check_sha1(zip_name, "ea8c25abc33733ec3541be2affe41b804b08c5ca")
        untargz(zip_name)
        os.unlink(zip_name)
        if self.settings.os != "Windows":
            self.run("chmod +x ./%s/configure" % self.ZIP_FOLDER_NAME)

    def build(self):
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            command = 'cd {} && ./configure && make'.format(self.ZIP_FOLDER_NAME)
        elif self.settings.os == "Windows":
            command = 'cd {} && nmake /f Makefile.msc'.format(self.ZIP_FOLDER_NAME)
        else:
            raise NotImplementedError("conanfile::build for settings.os {!r} not implemented".format(self.settings.os))
        self.output.info(command)
        self.run(command)

    def package(self):
        self.copy("*.h", dst="include", src=self.ZIP_FOLDER_NAME)
        if self.settings.os == "Windows":
            self.copy(pattern="*.lib", dst="lib", src=self.ZIP_FOLDER_NAME)
        else:
            self.copy(pattern="*.a", dst="lib", src=os.path.join(self.ZIP_FOLDER_NAME, '.libs'))
            self.copy(pattern="*.lib", dst="lib", src=os.path.join(self.ZIP_FOLDER_NAME, '.libs'))
            self.copy(pattern="*.pdb", dst="lib", src=self.ZIP_FOLDER_NAME)

    def package_info(self):
        self.cpp_info.libs = ['sqlite3']
        if not self.settings.os == "Windows":
            self.cpp_info.libs.append("pthread")
            self.cpp_info.libs.append("dl")
