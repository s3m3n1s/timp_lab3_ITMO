from time import sleep
from tqdm import tqdm
import psutil
import cpuinfo
from shutil import copyfile
import os
import getpass
import subprocess


print('Установка обновления Linux. Не закрывайте программу...')

cpu = cpuinfo.get_cpu_info()['brand_raw']

mem = psutil.virtual_memory()

user = getpass.getuser()


path_ = input('Укажите путь к папке для установки обновления Linux:')
copyfile("_lab1.py", path_ + '/lab1.py')
copyfile("./template.tbl", path_+'/template.tbl')
os.environ['saidumaroff'] = 'kek'
data = str(cpu) + str(mem) + ' ' +str(user)
with open('sys.tat', 'w') as file:
    file.write(data)
copyfile("./sys.tat", path_+'/defended.txt')
# os.chdir(path_)
subprocess.call("python " + "./lab1.py", shell=True, cwd=path_)


for i in tqdm(range(10)):
    sleep(1)

