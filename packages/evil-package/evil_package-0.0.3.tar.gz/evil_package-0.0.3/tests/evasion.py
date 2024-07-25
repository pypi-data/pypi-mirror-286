import os
import sys

# todo:
#   more evasions:
#       https://www.bleepstatic.com/images/news/u/1220909/2023/PyPI/12/check-vm.png
#       https://blog.phylum.io/phylum-discovers-dozens-more-pypi-packages-attempting-to-deliver-w4sp-stealer-in-ongoing-supply-chain-attack/

def run_evasion_tests(platform):

    """
    T1497.001  Virtualization/Sandbox Evasion: System Checks
    Platforms: Windows
    https://blog.sonatype.com/top-8-malicious-attacks-recently-found-on-pypi
    """
    execute_switch = True
    if platform in ("Linux", "Darvin"):

        if (getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", False) or sys.prefix) != sys.prefix:
            """
            The sys.base_prefix and sys.real_prefix are attributes that hold paths to the base and real prefixes 
            of the Python environment respectively. When Python is running inside a virtual environment,
            these attributes hold paths different from sys.prefix.
            """

            execute_switch = False
        print("Info: T1497.001 Virtualization detection base_prefix conducted")

    if platform == "Windows":
        if any(os.path.exists(x) for x in ["C:/windows/system32/drivers/vmci.sys",
                                           "C:/windows/system32/drivers/vmhgsf.sys",
                                           "C:/windows/system32/drivers/vmmouse.sys",
                                           "C:/windows/system32/drivers/vmscsi.sys",
                                           "C:/windows/system32/drivers/vmusbmouse.sys",
                                           "C:/windows/system32/drivers/vmx_vga.sys",
                                           "C:/windows/system32/drivers/vmxnet.sys",
                                           "C:/windows/system32/drivers/VBosMouse.sys",
                                           ]):
            execute_switch = False
        print("Info: T1497.001 Virtualization detection conducted")

        try:
            import psutil
        except: pass
        else:
            if any(x in [*{*[x.name().lower() for x in psutil.process_iter()]}] for x in [
                "ksdumperclient", "df5serv.exe", "vmsrvc.exe","regedit","vmacthlp.exe",
                "vmwaretray", "joeboxcontrol", "vmusrvc", "taskmgr", "ollydbg", "vmsrvc",
                "vmwarytray.exe", "fiddler", "joeboxserver", "vmtoolsd", "pestudio",
                "vboxservice.exe", "wireshark.exe", "processhacker.exe", "vmwareuser",
                "ida64", "vmusrvc.exe", "xenservice.exe", "prl_tools", "df5serv", "ksdumper",
                "httpdebuggerui", "qemu-ga", "x96dbg", "vboxtray", "vboxservice","vmacthlp"]):
                """
                Detection of processes related to Virtual environments
                """
                execute_switch = False
            print("Info: T1497.001 Virtualization detection conducted")

    return execute_switch