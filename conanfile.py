
import os
import shutil
import re
import unittest

from conans import ConanFile
from conans.tools import download, untargz
from conans import CMake

VERSION = "3.18.0"
YEAR = "2017"


class ConanRecipe(ConanFile):
    name = "sqlite3"
    version = VERSION
    license = "Public domain"
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"
    url = "http://github.com/jgsogo/conan-sqlite3"
    exports = ["FindSQLite3.cmake", "CMakeLists.txt", ]
    description = """SQLite is an in-process library that implements a self-contained, serverless,
                     zero-configuration, transactional SQL database engine."""

    _build_dir = "build"

    def __init__(self, *args, **kwargs):
        self.sqlite3 = SQLite3Data(VERSION)
        super(ConanRecipe, self).__init__(*args, **kwargs)

    def source(self):
        zip_name = self.sqlite3.zip_name
        download("http://www.sqlite.org/{}/{}".format(YEAR, zip_name), zip_name)
        #check_sha1(zip_name, "ea8c25abc33733ec3541be2affe41b804b08c5ca")
        untargz(zip_name)
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self.settings)
        shutil.move("CMakeLists.txt", "%s/CMakeLists.txt" % self.sqlite3.zip_folder)
        self.run("mkdir {}".format(self._build_dir))
        
        command = "cd {} && cmake ../{} {}".format(self._build_dir, self.sqlite3.zip_folder, cmake.command_line)
        self.output.info(command)
        self.run(command)

        command = "cd {} && cmake --build . {}".format(self._build_dir, cmake.build_config)
        self.output.info(command)
        self.run(command)

    def package(self):
        self.copy("FindSQLite3.cmake", ".", ".")
        self.copy("*.h", dst="include", src=self.sqlite3.zip_folder)
        if self.settings.os == "Windows":
            self.copy(pattern="*.lib", dst="lib", src=self._build_dir, keep_path=False)
            self.copy(pattern="*.dll", dst="bin", src=self._build_dir, keep_path=False)
        else:
            self.copy(pattern="*.a", dst="lib", src=self._build_dir, keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src=self._build_dir, keep_path=False)
            self.copy(pattern="*.pdb", dst="lib", src=self._build_dir, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['sqlite3']
        if not self.settings.os == "Windows":
            self.cpp_info.libs.append("pthread")
            self.cpp_info.libs.append("dl")


class SQLite3Data(object):
    version_re = re.compile(r"^\d+\.\d+(\.\d+)?$")
    amalgamation = "autoconf"  # amalgamation or autoconf

    def __init__(self, version):
        assert self.version_re.match(version), "Version {!r} does not match valid pattern.".format(version)
        self.version = version

    @property
    def version_number(self):
        vitems = self.version.split(".")
        ret = vitems[0]
        for it in vitems[1:] + ["0"]*(4-len(vitems)):
            ret += it.zfill(2)
        return ret

    @property
    def zip_name(self):
        return "sqlite-{amalgamation}-{version}.tar.gz".format(amalgamation=self.amalgamation, version=self.version_number)

    @property
    def zip_folder(self):
        return self.zip_name.split(".tar.gz", 1)[0]


class SQLite3DataTests(unittest.TestCase):
    def test_version(self):
        self.assertRaises(AssertionError, SQLite3Data, "3.12.3.4")
        self.assertRaises(AssertionError, SQLite3Data, ".12.3")
        self.assertRaises(AssertionError, SQLite3Data, "3.a.4")
        self.assertRaises(AssertionError, SQLite3Data, "3.12.3-alpha1")

    def test_version_number(self):
        self.assertEqual("3150200", SQLite3Data("3.15.2").version_number)
        self.assertEqual("3150000", SQLite3Data("3.15").version_number)
        self.assertEqual("3010200", SQLite3Data("3.1.2").version_number)
