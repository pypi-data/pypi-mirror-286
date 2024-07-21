import os
import re
import sys
import glob
import shutil
import sysconfig

import setuptools
from setuptools.command.build_ext import build_ext as build_ext
from setuptools.command.install_lib import install_lib as install_lib

templates = {
  "gluex.hddm_r": ["gluex/hddm_r/rest.xml"]
}

package_data = {
  "gluex.hddm_r": ["rest.xml",
                   "XRootD/client/*",
                   "pyxrootd/*",
                   "xrootd*",
                  ]
}

sources = {
  "zlib.url": "https://github.com/rjones30/zlib.git",
  "zlib.tag": "",
  "bzip2.url": "https://github.com/rjones30/bzip2.git",
  "bzip2.tag": "",
  "xerces-c.url": "https://github.com/rjones30/xerces-c.git",
  "xerces-c.tag": "",
  "hdf5.url": "https://github.com/HDFGroup/hdf5.git",
  "hdf5.tag": "tags/hdf5-1_10_8",
  "pthread-win32.url": "https://github.com/GerHobbelt/pthread-win32.git",
  "pthread-win32.tag": "version-3.1.0-release",
  "libuuid.url": "https://github.com/rjones30/libuuid.git",
  "libuuid.tag": "",
  "libxml2.url": "https://github.com/rjones30/libxml2.git",
  "libxml2.tag": "",
  "cpr.url": "https://github.com/rjones30/cpr.git",
  "cpr.tag": "",
  "xrootd.url": "https://github.com/rjones30/xrootd.git",
  "xrootd.tag": "stable-5.6-for-hddm",
  "HDDM.url": "https://github.com/rjones30/HDDM.git",
  "HDDM.tag": "streaming_input",
}

class CMakeExtension(setuptools.Extension):

    def __init__(self, name):
        super().__init__(name, sources=[])


class build_ext_with_cmake(build_ext):

    def run(self):
        build_extension_solibs = []
        for ext in self.extensions:
            self.build_with_cmake(ext)
            if ext.name in templates:
                build_extension_solibs.append(ext)
        self.extensions = build_extension_solibs
        super().run()

    def build_with_cmake(self, ext):
        if "win" in ext.name and not "win" in sysconfig.get_platform():
            return 0
        elif "xrootd" in ext.name and "win" in sysconfig.get_platform():
            return 0
        elif ext.name[:3] == "lib" and "win" in sysconfig.get_platform():
            return 0
        cwd = os.getcwd()
        if f"{ext.name}.url" in sources:
            if not os.path.isdir(ext.name):
                self.spawn(["git", "clone", sources[ext.name + ".url"]])
            os.chdir(ext.name)
            tag = sources[ext.name + ".tag"]
            if tag:
                self.spawn(["git", "checkout", tag])
            os.chdir(cwd)
        else:
            return 0
            raise Exception("missing sources",
                            f"no package sources specified for {ext.name}")
        
        cmake_config = "Debug" if self.debug else "Release"
        build_args = ["--config", cmake_config]
        if shutil.which("cmake"):
            cmake = ["cmake"]
        else:
            # Only happens on Windows, try to install it
            self.spawn(["scripts/install_cmake.bat"])
            cmake = ["cmake.exe"]
        if "xrootd" in ext.name:
            # pip module needed by xrootd cmake --install
            pyversion = f"python{sys.version_info[0]}.{sys.version_info[1]}"
            modpath = re.sub("/bin/python.*",
                             "/lib/" + pyversion + "/site-packages",
                             sys.executable)
            sys.path.append(modpath)
            os.environ['PYTHONPATH'] = modpath
            self.spawn(["python", "-m", "pip", "-V"])

        build_temp = f"build.{ext.name}"
        if not os.path.isdir(build_temp):
            os.mkdir(build_temp)
        os.chdir(build_temp)
        cmake_args = [
          f"-DCMAKE_INSTALL_PREFIX={os.path.abspath(cwd)}/build",
          f"-DEXTRA_INCLUDE_DIRS={os.path.abspath(cwd)}/build/include",
          f"-DCMAKE_BUILD_TYPE={cmake_config}",
          f"-DBUILD_SHARED_LIBS:bool=off",
          f"-DCMAKE_POSITION_INDEPENDENT_CODE:bool=on",
          f"-DCMAKE_OSX_DEPLOYMENT_TARGET=10.15",
          f"-DCMAKE_VERBOSE_MAKEFILE:BOOL=on",
        ]
        if sysconfig.get_platform() == "win32":
            cmake_args += ["-A", "Win32"]
        elif "arm64" in sysconfig.get_platform():
            cmake_args += [f"-DCMAKE_OSX_ARCHITECTURES=arm64"]
        if "xrootd" in ext.name:
            cmake_args += [f"-DXRDCL_LIB_ONLY:bool=on"]
            cmake_args += [f"-DOPENSSL_INCLUDE_DIR:path={os.path.abspath(cwd)}/build/include"]
        self.spawn(cmake + [f"../{ext.name}"] + cmake_args)
        if "xerces" in ext.name and sysconfig.get_platform != "win32":
            for inc in glob.glob(os.path.join(cwd, "build", "include", "uuid", "uuid.h")):
                self.spawn(echo + mv + [inc, inc + "idden"])
                self.spawn(mv + [inc, inc + "idden"])
        if not self.dry_run:
            if "uuid" in ext.name or sysconfig.get_platform() == "win32":
                self.spawn(cmake + ["--build", "."] + build_args)
            else:
                self.spawn(cmake + ["--build", "."] + build_args + ["-j4"])
            self.spawn(cmake + ["--install", "."])
            os.chdir(cwd)
            for solib in glob.glob(os.path.join("build", "lib", "*.so*")):
               self.spawn(["mkdir", "-p", os.path.join("build", "lib64")])
               self.spawn(["cp", solib, re.sub("/lib/", "/lib64/", solib)])
            for arlib in glob.glob(os.path.join("build", "lib64", "*.a")):
               self.spawn(["mkdir", "-p", os.path.join("build", "lib")])
               self.spawn(["cp", arlib, re.sub("/lib64/", "/lib/", arlib)])
            for arlib in glob.glob(os.path.join("build", "lib*", "*.a")):
               if re.match(r".*_static\.a$", arlib):
                  self.spawn(["cp", arlib, re.sub(r"_static\.a$", ".a", arlib)])
               else:
                  self.spawn(["cp", arlib, re.sub(r"\.a$", "_static.a", arlib)])
            self.spawn(["rm", "-rf", ext.name])
            self.spawn(["rm", "-rf", f"build.{ext.name}"])
        os.chdir(cwd)
        self.spawn(["ls", "-l", "-R", "build"])
        print("build target architecture is", sysconfig.get_platform())
        if ext.name == "HDDM": # finish construction of the hddm module
            if "win" in sysconfig.get_platform():
                if "PATH" in os.environ:
                    os.environ["PATH"] += f";{cwd}/build/bin"
                else:
                    os.environ["PATH"] = f"{cwd}/build/bin"
            else:
                if "PATH" in os.environ:
                    os.environ["PATH"] += f":{cwd}/build/bin"
                else:
                    os.environ["PATH"] = f"{cwd}/build/bin"
            for lib in glob.glob("build/lib*"):
                for ldpath in ["LD_LIBRARY_PATH", "DYLD_LIBRARY_PATH"]:
                    if ldpath in os.environ:
                        os.environ[ldpath] += f":{cwd}/{lib}"
                    else:
                        os.environ[ldpath] = f":{cwd}/{lib}"
            #os.environ["DYLD_PRINT_LIBRARIES"] = "1"
            #os.environ["DYLD_PRINT_LIBRARIES_POST_LAUNCH"] = "1"
            #os.environ["DYLD_PRINT_RPATHS"] = "1"
            for module in templates:
                for model in templates[module]:
                    os.chdir(os.path.join(*model.split('/')[:-1]))
                    self.spawn(["hddm-cpp", model.split('/')[-1]])
                    self.spawn(["hddm-py", model.split('/')[-1]])
                    modname = module.split('.')[-1]
                    self.spawn(["cp", f"py{modname}.cpy", f"py{modname}.cpp"])
                    os.chdir(cwd)


class install_ext_solibs(install_lib):

    def run(self):
        super().run()
        for wheel in glob.glob("build/bdist.*/wheel"):
            for solib in os.listdir(wheel):
                for mext in re.finditer("^([^/]*).cpython.*", solib):
                    if not mext.group(1) in templates:
                        self.spawn(["rm", "-f", f"{wheel}/{solib}"])
            print(f"install_ext_solibs in gluex tree:")
            for mext in glob.glob("build/lib*/python*/site-packages"):
               self.spawn(["ls", "-lR", mext])
               print(f"copying site-packages into gluex...")
               tarball = "build/site_packages.tar"
               self.spawn(["tar", "-cf", tarball, "-C", mext, "."])
               self.spawn(["tar", "-xf", tarball, "-C", f"gluex/hddm_r"])
               for solibdir in glob.glob("build/lib*"):
                  cwd = os.getcwd()
                  os.chdir(solibdir)
                  solibs = glob.glob("*.so*")
                  solibs += glob.glob("*.dylib*")
                  os.chdir(cwd)
                  if len(solibs) > 0:
                     self.spawn(["tar", "-cf", tarball, "-C", solibdir] + solibs)
                     self.spawn(["tar", "-xf", tarball, "-C", f"gluex/hddm_r/pyxrootd"])
               self.spawn(["ls", "-lR", "gluex"])
 

with open("README.md", "r") as fh:
    long_description = fh.read()

if "win" in sysconfig.get_platform():
    extension_include_dirs = ["gluex\\hddm_r",
                              "build\\include",
                             ]
    extension_library_dirs = ["build\\lib"]
    extension_libraries = ["libhdf5_hl",
                           "libhdf5",
                           "xstream",
                           "bz2",
                           "zlibstatic",
                           "xerces-c_3",
                           "libpthreadVC3",
                           "ws2_32",
                           "httpstream",
                           "cpr",
                           "libcurl",
                           "libssl",
                           "libcrypto",
                           "Advapi32",
                           "Crypt32",
                          ]
    extension_compile_args = ["-std:c++17",
                              "-DHDF5_SUPPORT",
                              "-DISTREAM_OVER_HTTP",
                             ]
else:
    extension_include_dirs = ["gluex/hddm_r",
                              "build/include",
                              "build/include/libxml2",
                              "build/include/xrootd",
                             ]
    extension_library_dirs = ["build/lib"]
    extension_libraries = ["hdf5_hl_static",
                           "hdf5_static",
                           "xstream",
                           "bz2_static",
                           "z_static",
                           "xerces-c_static",
                           "pthread",
                           "httpstream",
                           "cpr_static",
                           "curl_static",
                           "ssl_static",
                           "crypto_static",
                           "xrootdstream",
                           "XrdCl_static",
                           "XrdUtils_static",
                           "XrdXml_static",
                           "uuid_static",
                           "xml2_static",
                          ]
    extension_compile_args = ["-std=c++17",
                              "-DHDF5_SUPPORT",
                              "-DISTREAM_OVER_HTTP",
                              "-DISTREAM_OVER_XROOTD"
                             ]
if "macos" in sysconfig.get_platform():
    extension_compile_args += ["-mmacosx-version-min=10.15"]

setuptools.setup(
    name = "gluex.hddm_r",
    version = "2.1.11",
    url = "https://github.com/rjones30/hddm_r",
    author = "Richard T. Jones",
    description = "i/o module for GlueX reconstructed events",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = templates.keys(),
    namespace_packages=['gluex'],
    package_data = package_data,
    include_package_data = True,
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires = '>=3.6',              # Minimum version requirement of the package
    #install_requires = [                   # Install other dependencies if any
    #  "setuptools-git",
    #],
    ext_modules = [
      CMakeExtension("zlib"),
      CMakeExtension("bzip2"),
      CMakeExtension("xerces-c"),
      CMakeExtension("hdf5"),
      CMakeExtension("pthread-win32"),
      CMakeExtension("libuuid"),
      CMakeExtension("libxml2"),
      CMakeExtension("cpr"),
      CMakeExtension("xrootd"),
      CMakeExtension("HDDM"),
      setuptools.Extension("gluex.hddm_r",
           include_dirs = extension_include_dirs,
           library_dirs = extension_library_dirs,
           libraries = extension_libraries,
           extra_compile_args = extension_compile_args,
           sources = ["gluex/hddm_r/hddm_r++.cpp",
                      "gluex/hddm_r/pyhddm_r.cpp"]
      ),
    ],
    cmdclass = {
      "build_ext": build_ext_with_cmake,
      "install_lib": install_ext_solibs,
    }
)
