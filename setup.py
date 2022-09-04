import os
from glob import glob
from setuptools import setup

package_name = "pysdf"

setup(
    name=package_name,
    version="0.0.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    author="Andreas Bihlmaier",
    author_email="andreas.bihlmaier@gmx.de",
    description="Python library to parse SDF into class hierarchy and export URDF.",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "sdf2urdf = pysdf.sdf2urdf:main",
        ],
    },
)
