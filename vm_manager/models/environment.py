import libvirt
import os
from xml.dom import minidom
import sys
import shutil
import subprocess


from vm_manager.settings import IMAGES_PATH
from vm_manager.settings import IMAGES_WORKING_DIRECTORY

from vm_manager.drivers.libvirt.libvirt_xml import LibvirtXmlManager as XMLManager

class Environment(object):
    def __init__(self):
        self.conn = libvirt.open('qemu:///system')
        self.xml_manager = XMLManager()

    def vm_conn(self, vm_id):
        return self.conn.lookupByID(vm_id)

    def get_images_list(self):
        return os.listdir(IMAGES_PATH)

    def create_vm_config(self):
        pass

    def get_vms_info(self):
        """Get information about all vms on local machine

        :return: dict: {"vm_name": str, "vm_ip": str, "vm_id": int, "vm_status": str)
        """
        vm_ids = self.get_vm_ids()

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
        return self.xml_manager.get_mac(raw_xml)

    def create_vm_configs_from_image(self, image, vm_count, cluster_name='env_name'):
        """

        :param image: str, path to source image
        :param vm_count: int, count of vm that will be created
        :return:
        """
        try:
            with open(IMAGES_PATH + image) as f:
                pass
        except IOError as e:
            print("Error: Image file {} not found.".format(IMAGES_PATH + image))

        configs = []
        for node in (range(1, vm_count+1)):
            name = "node-{}".format(node)
            new_image = "{}{}_{}_{}".format(IMAGES_WORKING_DIRECTORY, cluster_name, name, image)
            shutil.copy(IMAGES_PATH + image, new_image)
            config = self.xml_manager.build_domain_xml(vm_name="{}_{}_{}".format(cluster_name,
                                                                                 name, image),
                                                       source_image=new_image)
            configs.append(config)
        return configs

    def create_domain(self, image, vm_count, cluster_name='env_name'):
        configs = self.create_vm_configs_from_image(image, vm_count, cluster_name)
        for config in configs:
            self.conn.createXML(config)

    def prepare_vm(self, vm_ip):
        pass

    def get_ip_by_mac(self, mac):
        process = subprocess.Popen(['arp', '-a'], stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        process.wait()
        for line in process.stdout:
            if mac in line:
                return line.split()[1].strip('()')

    def run_vm(self, vm_id):
        pass

    def delete_vm(self, vm_id):
        pass

    def suspend_vm(self, vm_id):
        """Suspend VM

        :param vm_id: virtual machine id
        :return: None
        """
        self.vm_conn(vm_id).suspend()

    def resume_vm(self, vm_id):
        """Resume virtual machine

        :param vm_id: virtual machine id
        :return:
        """
        self.vm_conn(vm_id).resume()


