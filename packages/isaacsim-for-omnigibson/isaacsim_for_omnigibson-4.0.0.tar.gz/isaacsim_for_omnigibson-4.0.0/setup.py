import os
import urllib.request
import subprocess
from setuptools import find_packages, setup
from setuptools.command.install import install
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

class CustomInstallCommand(install):
    ISAAC_SIM_PACKAGES = [
        "omniverse_kit-106.0.0",
        "isaacsim_kernel-4.0.0.0", "isaacsim_app-4.0.0.0", "isaacsim_core-4.0.0.0",
        "isaacsim_gui-4.0.0.0", "isaacsim_utils-4.0.0.0", "isaacsim_storage-4.0.0.0",
        "isaacsim_asset-4.0.0.0", "isaacsim_sensor-4.0.0.0", "isaacsim_robot_motion-4.0.0.0",
        "isaacsim_robot-4.0.0.0", "isaacsim_benchmark-4.0.0.0", "isaacsim_code_editor-4.0.0.0",
        "isaacsim_ros1-4.0.0.0", "isaacsim_cortex-4.0.0.0", "isaacsim_example-4.0.0.0",
        "isaacsim_replicator-4.0.0.0", "isaacsim_rl-4.0.0.0", "isaacsim_robot_setup-4.0.0.0",
        "isaacsim_ros2-4.0.0.0", "isaacsim_template-4.0.0.0", "isaacsim_test-4.0.0.0",
        "isaacsim-4.0.0.0", "isaacsim_extscache_physics-4.0.0.0", "isaacsim_extscache_kit-4.0.0.0",
        "isaacsim_extscache_kit_sdk-4.0.0.0"
    ]
    BASE_URL = "https://pypi.nvidia.com"

    def run(self):
        for package in self.ISAAC_SIM_PACKAGES:
            self.install_package(package)
        install.run(self)

    def install_package(self, package):
        package_name = package.split('-')[0].replace('_', '-')
        filename = self.get_filename(package)
        url = f"{self.BASE_URL}/{package_name}/{filename}"

        try:
            self.download_package(url, filename)
            install_filename = self.rename_if_necessary(filename)
            self.pip_install(install_filename)
        except Exception as e:
            print(f"Failed to install {package}: {str(e)}")
        finally:
            self.cleanup(filename)

    @staticmethod
    def get_filename(package):
        if os.name == "nt":
            return f"{package}-cp310-cp310-win_amd64.whl"
        return f"{package}-cp310-none-manylinux_2_34_x86_64.whl"

    @staticmethod
    def download_package(url, filename):
        try:
            urllib.request.urlretrieve(url, filename)
        except Exception as e:
            raise ValueError(f"Failed to download {url}") from e

    def rename_if_necessary(self, filename):
        if os.name == "posix" and self.is_glibc_older():
            new_filename = filename.replace("manylinux_2_34", "manylinux_2_31")
            os.rename(filename, new_filename)
            return new_filename
        return filename

    @staticmethod
    def is_glibc_older():
        try:
            dist_info = subprocess.check_output(['ldd', '--version']).decode('utf-8')
            if any(version in dist_info for version in ['2.31', '2.32', '2.33']):
                return True
            elif any(version in dist_info for version in ['2.34', '2.35', '2.36', '2.37', '2.38', '2.39']):
                return False
            else:
                raise ValueError("Incompatible GLIBC version")
        except subprocess.CalledProcessError:
            return False

    @staticmethod
    def pip_install(filename):
        try:
            subprocess.run(["pip", "install", filename], check=True)
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Failed to install {filename}") from e

    @staticmethod
    def cleanup(filename):
        if os.path.exists(filename):
            os.remove(filename)



setup(
    name="isaacsim-for-omnigibson",
    version="4.0.0",
    author="Stanford University, Isaac Sim team",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/StanfordVL/OmniGibson",
    zip_safe=False,
    packages=find_packages(),
    cmdclass={
        'install': CustomInstallCommand,
    },
    tests_require=[],
    python_requires="==3.10.*",
    include_package_data=True,
)