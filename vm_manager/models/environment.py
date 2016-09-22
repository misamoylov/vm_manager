import libvirt
import os
from xml.dom import minidom
import sys
import shutil
import subprocess
import xmltodict


from vm_manager.drivers.libvirt.libvirt_driver import LibvirtManager as Manager
from vm_manager.settings import IMAGES_PATH
from vm_manager.templates import qcow2_templates as config


class Environment(object):
    def __init__(self):
        self.conn = libvirt.open('qemu:///system')

    def get_images_list(self):
        return os.listdir(IMAGES_PATH)

    def get_vm_ids(self):
        """

        :return: list of virtual machines id
        """
        return [i.ID() for i in self.conn.listAllDomains()]

    def get_vm_mac(self, vm_id):
        """Connect to vm and return their mac address

        :param vm_id: integer, virtual machine ID
        :return:
        """
        vm = self.conn.lookupByID(vm_id)
        raw_xml = vm.XMLDesc(0)
        xml = minidom.parseString(raw_xml)
        interfaceTypes = xml.getElementsByTagName('interface')
        for interfaceType in interfaceTypes:
            interfaceNodes = interfaceType.childNodes
            for interfaceNode in interfaceNodes:
                if interfaceNode.nodeName == 'mac':
                    for attr in interfaceNode.attributes.keys():
                        return interfaceNode.attributes[attr].value

    # def get_vms(self):
    #     return self.conn.


    # def vm_config(self, name='default', memory='1', vcpu='1', image_name='ubuntu-12.04.qcow2'):
    #     return config.template2.format(name, memory, vcpu, image_name)

    def prepare_vm(self, vm_ip):
        pass


    def get_ip_by_mac(self,mac):
        process = subprocess.Popen(['arp', '-a'], stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        process.wait()
        for line in process.stdout:
            if mac in line:
                return line.split()[1].strip('()')

    def run_vm(self):
        pass

    def delete_vm(self):
        pass

    def suspend_vm(self):
        pass


