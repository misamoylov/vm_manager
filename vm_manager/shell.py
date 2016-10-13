# coding=utf-8
import sys
import argparse
import os
from helpers.ssh_manager import SSHManager
from helpers.utils import get_os_type
from helpers.utils import add_debian_repos
from helpers.utils import add_ubuntu_repos
from helpers.utils import install_deb
from helpers.utils import add_centos_repos
from helpers.utils import install_rpm

from vm_manager.models.environment import Environment
#
env = Environment()
vm_names = []
ssh = SSHManager()
# Step 1. Prepare vms
for image in env.get_images_list():
    vm_name = env.get_vm_name_from_config(env.create_vm(image=image))
    vm_names.append(vm_name)
    writepath = '/home/msamoylov/vm_manager/vms'
    mode = 'a+' if os.path.exists(writepath) else 'r+'
    with open(writepath, mode) as f:
        if vm_name not in f.readlines():
            f.write('{}\n'.format(vm_name))
# Step 2. Prepare snapshot 'ready'
for vm in env.get_vm_ids():
    with open('/home/msamoylov/vm_manager/vms') as f:
        if env.get_vm_name(vm) in f.read():
            if len(env.snapshots_vm(vm)) == 0 or 'ready' not in env.snapshots_vm(vm):
                env.create_snapshot(vm, 'ready')
                env.suspend(vm)
# Step 3. Resume VM, revert snapshot, upload and run script, suspend vm

with open('/home/msamoylov/vm_manager/vms') as f:
    for vm in f.readlines():
        try:
            virt = vm.rstrip('\n')
            env.resume(vm_name=virt)
            env.revert_snapshot_name(vm_name=virt, snapshot_name='ready')
            vm_ip = env.get_vm_ip(vm_name=virt)
            ssh.upload_to_remote(vm_ip, 'root', 'TestRoot1',
                                '/home/msamoylov/statistics_sender/client.py',
                                '/tmp/client.py')
            cmd = 'python /tmp/client.py'
            result = ssh.exec_cmd(vm_ip, cmd)
            env.suspend(vm_name=virt)
        except Exception as e:
            print("Cannot connect to vm {}".format(virt), e)





# ssh = SSHManager()
# for vm in env.get_vm_ids():
#     print(env.get_vm_ip(vm))
#     print(get_os_type(env.get_vm_ip(vm))['NAME'])
#     if "Ubuntu" in get_os_type(env.get_vm_ip(vm))['NAME']:
#         add_ubuntu_repos(env.get_vm_ip(vm))
#         print(install_deb(env.get_vm_ip(vm))['stdout'])
#     elif "CentOS" in get_os_type(env.get_vm_ip(vm))['NAME']:
#         print(add_centos_repos(env.get_vm_ip(vm))['stdout'])
#         print(install_rpm(env.get_vm_ip(vm))['stdout'])
#     elif "Debian" in get_os_type(env.get_vm_ip(vm))['NAME']:
#         print(add_debian_repos(env.get_vm_ip(vm))['stdout'])
#         print(install_deb(env.get_vm_ip(vm)))



    # lsb_rel = ssh.exec_cmd(env.get_vm_ip(vm), 'lsb_release -a')['stdout'].replace('\t', ' ').strip().split('\n')
    # lsb_rel = dict(e.split(':') for e in ssh.exec_cmd(env.get_vm_ip(vm), 'lsb_release -a')['stdout'].replace('\t', ' ').strip().split('\n'))
    # # lsb_rel.pop()
    # print(lsb_rel)
    # etc_rel = ssh.exec_cmd(env.get_vm_ip(vm), 'cat /etc/*-release')['stdout'].replace('\t', ' ').strip().split('\n')
    # print(etc_rel)



# Подключение под centos 6/7, RHEL
#
# sudo rpm -ivh http://repo.postgrespro.ru/pgpro-9.5/keys/postgrespro-9.5.centos95.noarch.rpm
#
# Подключение под Oracle Linux
#
# sudo rpm -ivh http://repo.postgrespro.ru/pgpro-9.5/keys/postgrespro-9.5.oraclelinux95.noarch.rpm
#
# Подключение под Rosa Enterprise Linux server
#
# sudo rpm -ivh http://repo.postgrespro.ru/pgpro-9.5/keys/postgrespro-9.5.rosa-el95.noarch.rpm
#
# Подключение под Rosa SX Cobalt server
#
# sudo rpm -ivh http://repo.postgrespro.ru/pgpro-9.5/keys/postgrespro-9.5.rosa-sx95.noarch.rpm
#
# Подключение под Rosa DX Cobalt, Rosa Marathon LTS 2012
#
# urpmi.addmedia pgpro http://repo.postgrespro.ru/pgpro-9.5/rosa-dx/x86_64/media/main/
#
# Подключение под debian 7/8
#
# sudo apt-get install lsb-release
# sudo sh -c 'echo "deb http://repo.postgrespro.ru/pgpro-9.5/debian $(lsb_release -cs) main" > /etc/apt/sources.list.d/postgrespro.list'
# wget --quiet -O - http://repo.postgrespro.ru/pgpro-9.5/keys/GPG-KEY-POSTGRESPRO-95 | sudo apt-key add -
# sudo apt-get update
#
# Подключение под ubuntu 12.04/14.04/15.10/16.04
#
# sudo sh -c 'echo "deb http://repo.postgrespro.ru/pgpro-9.5/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/postgrespro.list'
# wget --quiet -O - http://repo.postgrespro.ru/pgpro-9.5/keys/GPG-KEY-POSTGRESPRO-95 | sudo apt-key add -
# sudo apt-get update
#
# Подключение под Alt Linux Centaur 7
#
# sudo sh -c 'echo "rpm http://repo.postgrespro.ru/pgpro-9.5/altlinux/7 x86_64 pgpro" > /etc/apt/sources.list.d/pgpro.list'
# sudo apt-get update
#
# Подключение под alt-linux СПТ 7
#
# sudo sh -c 'echo "rpm http://repo.postgrespro.ru/pgpro-9.5/altlinux-spt/7 x86_64 pgpro" > /etc/apt/sources.list.d/pgpro.list'
# sudo apt-get update
#
# Подключение под alt-linux СПТ 6
#
# sudo sh -c 'echo "rpm http://repo.postgrespro.ru/pgpro-9.5/altlinux-spt/6 x86_64 pgpro" > /etc/apt/sources.list.d/pgpro.list'
# sudo apt-get update
#
# Подключение под SUSE Linux Enterprise Server
#
#  sudo rpm --import http://repo.postgrespro.ru/pgpro-9.5/keys/GPG-KEY-POSTGRESPRO-95
# sudo zypper addrepo http://repo.postgrespro.ru/pgpro-9.5/suse/11 pgpro
#
# Подключение под Astra Linux Smolensk 1.4
#
# sudo sh -c 'echo "deb
#  http://repo.postgrespro.ru/pgpro-9.5/astra-smolensk smolensk main"> /etc/apt/sources.list.d/postgrespro.list' wget --quiet -O -
#  http://repo.postgrespro.ru/pgpro-9.5/keys/GPG-KEY-POSTGRESPRO-95 |
#  sudo apt-key add - sudo apt-get update


