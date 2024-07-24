import os
import sys
from skbuild import setup
from setuptools import find_packages

# src/debian/changelog
workdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
change_log = os.path.join(workdir, "src", "debian", "changelog")
with open(change_log, "r") as f:
    lines = f.readlines()
    while lines[0].strip() == "":
        lines.pop(0)
    title = lines[0].strip()
    # like "arducam-tof-sdk-dev (0.1.4) UNRELEASED; urgency=medium"
    version = title.split(" ")[1]
    # remove the parentheses
    version = version[1:-1]
    # check if the version is \d+\.\d+\.\d+
    if not version.replace(".", "").isdigit():
        raise ValueError("Invalid version in changelog")
    if version.count(".") != 2:
        raise ValueError("Invalid version in changelog")

cmake_args = [
    "-DLOG_WARN=OFF",
    "-DLOG_INFO=OFF",
    "-DWITH_CSI=ON",
    "-DWITH_USB=ON",
    "-DONLY_PYTHON=ON",
    "-DVERSION_INFO=" + version,
]
if sys.version_info < (3, 7):
    cmake_args += ["-DWITH_OLD_PYBIND11=ON"]

setup(
    name="ArducamDepthCamera",
    version=version,
    description="Driver development kit for arducam tof camera",
    author="Arducam <support@arducam.com>",
    packages=find_packages(),
    cmake_args=cmake_args,
    cmake_source_dir="..",
    cmake_install_dir="ArducamDepthCamera",
    package_data={"ArducamDepthCamera": ["ArducamDepthCamera.pyi"]},
    include_package_data=True,
)
