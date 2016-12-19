from conans.model.conan_file import ConanFile
from conans import CMake
import os
import re

channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "jgsogo")


def get_version():
    # Just want to be sure that I'm always testing this version
    cfile = os.path.join(os.path.dirname(__file__), "..", "conanfile.py")
    version_pattern = re.compile(r'^VERSION = "(?P<version>[\d\.]+)"(\s+#.*)?$')
    with open(cfile) as f:
        for line in f:
            m = version_pattern.match(line.strip())
            if m:
                return m.group('version')
    raise Exception("Cannot get version from {!r}".format(cfile))


class DefaultNameConan(ConanFile):
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"
    requires = "sqlite3/{version}@{username}/{channel}".format(version=get_version(), username=username, channel=channel)

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake %s %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib", dst="bin", src="lib")

    def test(self):
        self.run(os.path.join(".", "bin", "test"))

