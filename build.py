import os
from conan.packager import ConanMultiPackager


username = os.getenv("CONAN_USERNAME", "jgsogo")


if __name__ == "__main__":
    builder = ConanMultiPackager(username=username)
    builder.add_common_builds()
    print("{} builds ahead!".format(len(builder.builds)))
    builder.run()

