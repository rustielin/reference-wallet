# Copyright (c) The Libra Core Contributors
# SPDX-License-Identifier: Apache-2.0

import os

from setuptools import setup

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="libra-vasp-validator",
    version="1.0.0.dev1",
    author="TBD",
    description="Libra VASP validation library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache-2.0",
    url="https://github.com/libra/libra-reference-wallet",
    package_dir={"": "libra"},
    packages=["vasp_validator"],
    install_requires=[
        "libra-client-sdk",
        "dataclasses_json",
        "requests",
        "pytest",
    ],
    entry_points={
        "console_scripts": [
            "validate-vasp = vasp_validator.tests:automatic_validation_main",
        ],
    },
    python_requires=">=3.7",
)
