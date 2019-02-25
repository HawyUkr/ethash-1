#!/usr/bin/env python3

# ethash: C/C++ implementation of Ethash, the Ethereum Proof of Work algorithm.
# Copyright 2019 Pawel Bylica.
# Licensed under the Apache License, Version 2.0.

import subprocess
from distutils.errors import CCompilerError
from os import path

from setuptools import setup
from setuptools.command.build_ext import build_ext as setuptools_build_ext


class build_ext(setuptools_build_ext):
    def run(self):
        cmake_opts = [
            '-DCMAKE_INSTALL_PREFIX=.',
            '-DETHASH_BUILD_TESTS=OFF',
            '-DETHASH_INSTALL_CMAKE_CONFIG=OFF'
        ]
        build_dir = self.build_temp
        source_dir = path.dirname(path.abspath(__file__))
        
        r = subprocess.call(['cmake', source_dir] + cmake_opts,
                            cwd=build_dir)
        if r != 0:
            raise CCompilerError(
                "cmake configuration failed with exit status {}".format(r))
        r = subprocess.call(
            ['cmake', '--build', build_dir, '--target', 'install'])
        if r != 0:
            raise CCompilerError(
                "cmake build failed with exit status {}".format(r))

        self.library_dirs.append(path.join(build_dir, 'lib'))

        super(build_ext, self).run()


setup(
    name='ethash',
    version='0.5.0-alpha.0',
    url='https://github.com/chfast/ethash',
    author='Paweł Bylica',
    author_email='pawel@ethereum.org',

    package_dir={'': 'bindings/python'},
    packages=['ethash'],
    cffi_modules=['bindings/python/ethash/_build.py:ffibuilder'],

    setup_requires=['cffi>=1.12', 'cmake>=3.13'],
    install_requires=['cffi>=1.12'],

    test_suite='tests.test_ethash',

    cmdclass={'build_ext': build_ext},
)
