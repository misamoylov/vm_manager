# coding=utf-8
import paramiko


class SSHManager(object):
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def exec_cmd(self, ip, cmd):
        self.client.connect(ip, 22, 'root', 'TestRoot1')
        ex_res = self.client.exec_command(cmd)
        result = {
            'stdout': ex_res[1].read(),
            'stderr': ex_res[2].read()
        }
        return result

    def execute_command(self, ip, user, password, cmd):
        """Execute command via ssh

        :param ip: string ip address or hostname
        :param user: string with username password
        :param password: string with password
        :param cmd: command string
        :return:
        """
        self.client.connect(ip, 22, user, password)
        self.client.exec_command(cmd)

    def get_remote(self, ip, port, user, password):
        return self.client.connect(ip, port, user, password)

    def close_connection(self):
        self.client.close()

    def exec_interactive_command(self, ip, cmd, interactive_cmd):
        self.client.connect(ip, 22, 'root', 'TestRoot1')
        ex_res = self.client.exec_command(cmd)
        ex_res[0].write('{}\n'.format(interactive_cmd))
        ex_res[0].flush()
        result = {
            'stdout': ex_res[1].read(),
            'stderr': ex_res[2].read()
        }
        return result

    def upload_to_remote(self, ip, user, password, localpath, remotepath):
        """

        :return:
        """
        transport = paramiko.Transport((ip, 22))
        transport.connect(username=user,
                          password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        sftp.put(localpath, remotepath)


