# coding=utf-8
import random

from vm_manager.helpers.ssh_manager import SSHManager


def mac_address_generator():
    """Generate random mac address

    :return: string: mac address
    """
    mac = [0x00, 0x16, 0x3e,
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))


def get_os_type(ip):
    ssh = SSHManager()
    return dict(
        v.split("=") for v in ssh.exec_cmd(
            ip, 'cat /etc/*-release')['stdout'].replace(
            '\t', ' ').strip().split('\n') if v.strip() and "=" in v)


def add_ubuntu_repos(ip):
    ssh = SSHManager()
    cmd = "sh -c \'echo \"deb http://repo.postgrespro.ru/pgproee-9.6-beta/ubuntu/" \
          " $(lsb_release -cs) main\" " \
          "> /etc/apt/sources.list.d/postgrespro.list\'"
    ssh.exec_cmd(ip, cmd)
    cmd = "wget --quiet -O" \
          " - http://repo.postgrespro.ru/pgproee-9.6-beta/keys/GPG-KEY-POSTGRESPRO-95" \
          " |  apt-key add -"
    ssh.exec_cmd(ip, cmd)
    cmd = "apt-get update"
    return ssh.exec_cmd(ip, cmd)


def add_debian_repos(ip):
    ssh = SSHManager()
    cmd = "sh -c \'echo \"deb http://repo.postgrespro.ru/pgproee-9.6-beta/debian/" \
          " $(lsb_release -cs) main\" " \
          "> /etc/apt/sources.list.d/postgrespro.list\'"
    ssh.exec_cmd(ip, cmd)
    cmd = "wget --quiet -O" \
          " - http://repo.postgrespro.ru/pgproee-9.6-beta/keys/GPG-KEY-POSTGRESPRO-95" \
          " |  apt-key add -"
    ssh.exec_cmd(ip, cmd)
    cmd = "apt-get update"
    return ssh.exec_cmd(ip, cmd)


def add_centos_repos(ip):
    ssh = SSHManager()
    cmd = "rpm -ivh " \
          "http://repo.postgrespro.ru/pgproee-9.6-beta/keys/postgrespro-9.6.centos96.noarch.rpm"
    ssh.exec_cmd(ip, cmd)
    cmd = "yum update"
    return ssh.exec_interactive_command(ip, cmd, 'y')


def install_deb(ip):
    """Install PostgresproEE on Debian, Ubuntu, Astra Linux
    :param ip:
    :return:
    """
    ssh = SSHManager()
    cmd = "apt-get install postgrespro-9.6"
    return ssh.exec_interactive_command(ip, cmd, 'y')


def install_rpm(ip):
    """Install PostgresproEE CentOS, Oracle, ROSA

    :param ip:
    :return:
    """
    ssh = SSHManager()
    cmd = "yum install postgrespro96-server"
    return ssh.exec_interactive_command(ip, cmd, 'y')


