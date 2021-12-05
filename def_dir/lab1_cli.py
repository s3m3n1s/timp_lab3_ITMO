import hashlib
import json
import os
import pyAesCrypt
import glob
from threading import Thread
import time

global stop
stop = False


def set_new_password(password):
    hash_object = hashlib.md5(password.encode())
    with open('template.tbl', 'r') as file:
        old = json.load(file)
    with open('template.tbl', 'w') as file:
        old["password"] = hash_object.hexdigest()
        json.dump(old, file)


def add_new_file(file_name):
    with open('template.tbl', 'r') as file:
        old = json.load(file)
    with open('template.tbl', 'w') as file:
        old["files"].append(file_name)
        json.dump(old, file)


def del_file(file_name):
    with open('template.tbl', 'r') as file:
        old = json.load(file)
    with open('template.tbl', 'w') as file:
        old["files"].remove(file_name)
        json.dump(old, file)


def crypt_files(password):
    bufferSize = 64 * 1024
    with open('template.tbl', 'r') as file:
        fi = json.load(file)
    if hashlib.md5(password.encode()).hexdigest() == fi['password']:
        for i in fi['files']:
            for j in glob.glob(i):
                pyAesCrypt.encryptFile(j, j + ".enc", password, bufferSize)
                os.remove(j)
    return fi['files']


def decrypt_files(password):
    bufferSize = 64 * 1024
    with open('template.tbl', 'r') as file:
        fi = json.load(file)
    if hashlib.md5(password.encode()).hexdigest() == fi['password']:
        for i in fi['files']:
            for j in glob.glob(i + '.enc'):
                pyAesCrypt.decryptFile(j, '.'.join(j.split('.')[0:-1]), password, bufferSize)
                os.remove(j)


def init(password):
    if 'template.tbl.enc' in os.listdir():
        bufferSize = 64 * 1024
        pyAesCrypt.decryptFile('template.tbl.enc', 'template.tbl', password, bufferSize)


def end(password):
    bufferSize = 64 * 1024
    pyAesCrypt.encryptFile('template.tbl', 'template.tbl.enc', password, bufferSize)
    os.remove('template.tbl')


def check_and_delete(files):
    for i in files:
        for j in glob.glob(i):
            if '.enc' not in j:
                os.remove(j)


def checker(files):
    global stop
    while True:
        time.sleep(5)
        if stop:
            return 0
        check_and_delete(files)


def set_files_right_no(password):
    with open('template.tbl', 'r') as file:
        fi = json.load(file)
    for i in fi['files']:
        for j in glob.glob(i + '.enc'):
            os.chmod(j, 0o000)


def set_files_right_yes(password):
    with open('template.tbl', 'r') as file:
        fi = json.load(file)
    for i in fi['files']:
        for j in glob.glob(i):
            os.chmod(j, 0o777)
        for j in glob.glob(i + '.enc'):
            os.chmod(j, 0o777)


def start_def(password):
    init(password)
    files = crypt_files(password)
    set_files_right_no(password)
    end(password)
    return files


def stop_def(password):
    init(password)
    set_files_right_yes(password)
    decrypt_files(password)
    # set_files_right_yes(password)


def cli():
    global stop
    password = input("Password: ")
    cmd = input('>')

    while cmd != 'exit':
        if cmd == 'start':
            files = start_def(password)
            my_thread = Thread(target=checker, args=(files,))
            my_thread.start()
        elif cmd == 'stop':
            stop_def(password)
            stop = True
        elif cmd == 'env':
            print(os.environ['saidumaroff'])
        cmd = input('>')


cli()
