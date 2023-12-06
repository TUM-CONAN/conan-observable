#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout, CMakeDeps
from conan.tools.scm import Git
from conan.tools.files import load, update_conandata, copy, replace_in_file, get
import os


class observableConan(ConanFile):

    name = "observable"
    _version = "0.1"
    revision = "-dev"
    version = _version+revision

    license = "Apache-2.0"
    homepage = "https://github.com/ulricheck/observable"
    url = "https://github.com/TUM-CONAN/conan-observable"
    description = "c++ observable properties"
    topics = ("Pattern", "Architecture")

    settings = "os", "compiler", "build_type", "arch"
    options = {
         "shared": [True, False],
         "fPIC": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True
    }

    def export(self):
        update_conandata(self, {"sources": {
            "commit": "master",  #"{}".format(self.version),
            "url": "https://github.com/ulricheck/observable.git"
            }}
            )

    def source(self):
        git = Git(self)
        sources = self.conan_data["sources"]
        git.clone(url=sources["url"], target=self.source_folder)
        git.checkout(commit=sources["commit"])


    def source(self):
        get(self, "https://github.com/ulricheck/observable/archive/refs/heads/master.tar.gz",
            strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)

        def add_cmake_option(option, value):
            var_name = "{}".format(option).upper()
            value_str = "{}".format(value)
            var_value = "ON" if value_str == 'True' else "OFF" if value_str == 'False' else value_str
            tc.variables[var_name] = var_value

        for option, value in self.options.items():
            add_cmake_option(option, value)

        tc.cache_variables["CPP_STANDARD"] = str(self.settings.compiler.cppstd)

        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def layout(self):
        cmake_layout(self, src_folder="source_folder")

    def build(self):
        #disable unneeded targets
        replace_in_file(self, os.path.join(self.source_folder, "CMakeLists.txt"), "add_subdirectory(tests)", "#add_subdirectory(tests)")
        replace_in_file(self, os.path.join(self.source_folder, "CMakeLists.txt"), "add_subdirectory(benchmark)", "#add_subdirectory(benchmark)")
        replace_in_file(self, os.path.join(self.source_folder, "CMakeLists.txt"), "add_subdirectory(docs)", "#add_subdirectory(docs)")
        replace_in_file(self, os.path.join(self.source_folder, "CMakeLists.txt"), "add_subdirectory(examples)", "#add_subdirectory(examples)")
        replace_in_file(self, os.path.join(self.source_folder, "CMakeLists.txt"), "add_subdirectory(vendor)", "#add_subdirectory(vendor)")

        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        copy(self, "*.hpp", os.path.join(self.source_folder, "observable", "include"), os.path.join(self.package_folder, "include"))

    def package_info(self):
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
