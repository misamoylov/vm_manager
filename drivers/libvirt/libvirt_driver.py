# coding=utf-8
import libvirt


class LibvirtManager(object):
    def __init__(self, hypervisor):
        self.conn = libvirt.open('{}:///system'.format(hypervisor))

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
