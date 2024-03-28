from conan import ConanFile, tools
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import get, copy, rmdir, save
from conan.tools.scm import Version

import os
import textwrap

required_conan_version = ">=1.60.0"

class GossipConan(ConanFile):
  name = "gossip"
  url = "https://github.com/conan-io/conan-center-index"
  description = "SWIM Gossip and Consensus algorithm"
  license = ("Apache-2.0")
  homepage = "https://github.com/bowb/gossip"
  settings = "os", "compiler", "build_type", "arch"
  topics = ("gossip", "swim")
  package_type = "library"
  generators = "cmake_find_package", "cmake_paths"

  options = {
      "shared": [True, False],
      "fPIC": [True, False],
  }

  default_options = {
      "shared": False,
      "fPIC": True,
      "glog:with_gflags": False,
      "zeromq:shared": False,
      "Protobuf:shared": False,
      "openssl:shared": False,
      # used only in testing
      "gtest:shared": True,
      "libuv:shared": True,
      "http_parser:shared": True
  }
  
  def build_requirements(self):
    self.tool_requires("cryptopp/8.9.0")
    self.tool_requires("glog/0.7.0")
    self.tool_requires("gtest/1.14.0")
    self.tool_requires("protobuf/3.21.12")
    self.tool_requires("cppzmq/4.10.0")
    self.tool_requires("openssl/3.2.1")
    self.tool_requires("cryptopp/8.9.0")
    self.tool_requires("zeromq/4.3.5")
    self.tool_requires("boost/1.84.0")
    self.tool_requires("libuv/1.48.0")
    self.tool_requires("date/3.0.1")

  def configure(self):
      if self.options.shared:
          self.options.rm_safe("fPIC")

  def validate(self):
    if self.settings.os != "Linux":
      raise ConanInvalidConfiguration("Only linux supported")
  
  def layout(self):
    cmake_layout(self, src_folder="src")

  def source(self):
    get(self, **self.conan_data["sources"][self.version], strip_root=True)

  def generate(self):
      tc = CMakeToolchain(self)
      tc.variables["BUILD_TESTING"] = False
      tc.generate()

      deps = CMakeDeps(self)
      deps.generate()

  def package(self):
    copy(self, "LICENSE-2.0.txt", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
    cmake = CMake(self)
    cmake.install()
      
    self._create_cmake_module_alias_targets(
        os.path.join(self.package_folder, self._module_file_rel_path),
        {self._gossip_target: "gossip::gossip"}
    )

  def _create_cmake_module_alias_targets(self, module_file, targets):
      content = ""
      for alias, aliased in targets.items():
          content += textwrap.dedent(f"""\
              if(TARGET {aliased} AND NOT TARGET {alias})
                  add_library({alias} INTERFACE IMPORTED)
                  set_property(TARGET {alias} PROPERTY INTERFACE_LINK_LIBRARIES {aliased})
              endif()
          """)
      save(self, module_file, content)

  def build(self):
    cmake = CMake(self)
    cmake.configure()
    cmake.build()
    
    if not tools.build.cross_building(self):
      cmake.test()

  @property
  def _module_file_rel_path(self):
    return os.path.join("lib", "cmake", f"conan-official-{self.name}-targets.cmake")

  @property
  def _gossip_target(self):
    return "gossip" if self.options.shared else "gossip-static"

  def package_info(self):
    self.cpp_info.set_property("cmake_file_name", "gossip")
    self.cpp_info.set_property("cmake_target_name", self._gossip_target)
    self.cpp_info.libs = ["gossip"]
    if not self.options.shared:
      self.cpp_info.defines.append("GOSSIP_STATIC")
    
    # TODO: to remove in conan v2 once cmake_find_package_* generators removed
    self.cpp_info.build_modules["cmake_find_package"] = [self._module_file_rel_path]
    self.cpp_info.build_modules["cmake_find_package_multi"] = [self._module_file_rel_path]
