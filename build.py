import os
from conan.packager import ConanMultiPackager
from conanfile import SQLite3Conan

username = os.getenv("CONAN_USERNAME", "jgsogo")
reference = os.getenv("CONAN_REFERENCE", "{}/{}".format(SQLite3Conan.name, SQLite3Conan.version))


if __name__ == "__main__":
    builder = ConanMultiPackager(username=username, reference=reference)
    builder.add_common_builds()
    print("{} builds ahead!".format(len(builder.builds)))
    builder.run()

