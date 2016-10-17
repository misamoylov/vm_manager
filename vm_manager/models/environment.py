import libvirt
import os
import random
import shutil
import subprocess
from xml.dom import minidom

from vm_manager.settings import IMAGES_PATH
from vm_manager.settings import IMAGES_WORKING_DIRECTORY

from vm_manager.drivers.libvirt.libvirt_xml import LibvirtXmlManager as XMLManager


class Environment(object):
    def __init__(self, images_path=None, images_working_directory=None):
        self.conn = libvirt.open('qemu:///system')
        self.xml_manager = XMLManager()
        self.snapshot = None
        if images_path is None:
            self.images_path = IMAGES_PATH
        else:
            self.images_path = images_path
        if images_working_directory is None:
            self.images_working_directory = IMAGES_WORKING_DIRECTORY
        else:
            self.images_working_directory = images_working_directory

    def get_image_name(self, full_image_name):
        return full_image_name.rstrip('.qcow2')

    def vm_conn(self, vm_id=None, vm_name=None):
        if vm_id is not  None:
            return self.conn.lookupByID(vm_id)
        elif vm_name is not None:
            return self.conn.lookupByName(vm_name)

    def get_images_list(self):
        return os.listdir(self.images_path)

    def get_vm_ids(self):
        """

        :return: list of virtual machines id
        """
        return [i.ID() for i in self.conn.listAllDomains()]

    def get_vm_names(self):
        """

        :return: list of virtual machines names
        """
        return [i.name() for i in self.conn.listAllDomains()]

    def get_vm_mac(self, vm_id=None, vm_name=None):
        """Connect to vm and return their mac address

        :param vm_id: integer, virtual machine ID
        :return:
        """
        if vm_id is not None:
            vm = self.conn.lookupByID(vm_id)
        elif vm_name is not None:
            vm = self.conn.lookupByName(vm_name)
        raw_xml = vm.XMLDesc(0)
        return self.xml_manager.get_mac(raw_xml)

    def create_vm_config_standalone_vm(self, image):
        """

                :param image: str, path to source image
                :param vm_count: int, count of vm that will be created
                :return:
                """
        try:
            with open(self.images_path + image) as f:
                pass
        except IOError as e:
            print("Error: Image file {} not found.".format(self.images_path + image), e)

        new_image = "{}{}".format(self.images_working_directory, image)
        try:
            shutil.copy(self.images_path + image, new_image)
            config = self.xml_manager.build_domain_xml(vm_name="{}".format(image),
                                                       source_image=new_image)
        except IOError as e:
            print("Your are already has vm with with image {}. Creating new image file".format(
                image), e)
            rand = random.randint(1, 100)
            new_image = "{}{}-{}".format(self.images_working_directory, rand, image)
            shutil.copy(self.images_path + image, new_image)
            config = self.xml_manager.build_domain_xml(vm_name="{}-{}".format(rand, image),
                                                       source_image=new_image)
        return config

    def get_vm_name_from_config(self, vm_config):
        return self.xml_manager.get_vm_name(vm_config)

    def get_vm_name(self, vm_id):
        return self.vm_conn(vm_id=vm_id).name()

    def create_vm_configs_from_image(self, image, vm_count, cluster_name='env_name'):
        """

        :param image: str, path to source image
        :param vm_count: int, count of vm that will be created
        :return:
        """
        try:
            with open(self.images_path + image) as f:
                pass
        except IOError as e:
            print("Error: Image file {} not found.".format(self.images_path + image), e)

        configs = []
        for node in (range(1, vm_count+1)):
            name = "node-{}".format(node)
            new_image = "{}{}_{}_{}".format(self.images_working_directory, cluster_name, name,
                                            image)
            shutil.copy(self.images_path + image, new_image)
            config = self.xml_manager.build_domain_xml(vm_name="{}_{}_{}".format(cluster_name,
                                                                                 name, image),
                                                       source_image=new_image)
            configs.append(config)
        return configs

    def create_cluster(self, image, vm_count, cluster_name='env_name'):
        configs = self.create_vm_configs_from_image(image, vm_count, cluster_name)
        for config in configs:
            self.conn.createXML(config)
        return configs

    def create_vm(self, image):

        config = self.create_vm_config_standalone_vm(image)
        self.conn.createXML(config)
        return config

    def define_vm(self, image):

        config = self.create_vm_config_standalone_vm(image)
        self.conn.defineXML()
        return config

    def get_ip_by_mac(self, mac):
        process = subprocess.Popen(['arp', '-a'], stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        process.wait()
        for line in process.stdout:
            if mac in line:
                return line.split()[1].strip('()')

    def get_vm_ip(self, vm_id=None, vm_name=None):
        """Get vm ip

        :param vm_id: virtual machine id
        :return: str: virtual machine ip
        """
        if vm_id is not None:
            return self.get_ip_by_mac(self.get_vm_mac(vm_id))
        elif vm_name is not None:
            return self.get_ip_by_mac(self.get_vm_mac(vm_name=vm_name))

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

    def start(self, vm_id):
        """
        Start VM.
        """
        if self.vm_status(vm_id) is False:
            self.vm_conn(vm_id).create()

    def vm_status(self, vm_id):
        """Property to check if VM is active.
         :return: if VM is active.
        :rtype: Boolean
        """
        return bool(self.vm_conn(vm_id).isActive())

    def suspend(self, vm_id=None, vm_name=None):
        """
        Suspend VM.
        """
        if vm_id is not None:
            self.conn.lookupByID(vm_id).suspend()
        elif vm_name is not None:
            self.conn.lookupByName(vm_name).suspend()
        # if self.vm_status(vm_id):
        #     self.vm_conn(vm_id).suspend()

    def resume(self, vm_id=None, vm_name=None):
        """
        Resume VM.
        """
        if vm_id is not None:
            self.vm_conn(vm_id).resume()
        elif vm_name is not None:
            self.vm_conn(vm_name=vm_name).resume()

    def reboot(self, vm_id):
        """
        Reboot VM.
        """
        if self.vm_status(vm_id):
            self.vm_conn(vm_id).reboot()

    def shutdown(self, vm_id):
        """
        Shutdown VM.
        """
        if self.vm_status(vm_id):
            self.vm_conn(vm_id).shutdown()

    def reset(self, vm_id):
        """
        Reset VM.
        """
        if self.vm_status(vm_id):
            self.vm_conn(vm_id).reset()

    def stop(self, vm_id):
        """
        Stop VM.
        """
        if self.vm_status(vm_id):
            self.vm_conn(vm_id).destroy()

    def snapshots_vm(self, vm_id):
        """List of snapshots for vm

        :param vm_id: vm id
        :return: list of snapshots
        """
        vm = self.conn.lookupByID(vm_id)
        return vm.snapshotListNames()

    def create_xml_for_snapshot(self, name=None):
        def create_element(doc, tag, text):
            el = doc.createElement(tag)
            txt = doc.createTextNode(text)
            el.appendChild(txt)
            return el

        doc = minidom.Document()
        root = doc.createElement('domainsnapshot')
        doc.appendChild(root)
        if name is not None:
            root.appendChild(create_element(doc, 'name', name))
        description = 'Snapshot for VM'
        root.appendChild(create_element(doc, 'description', description))
        return doc.toxml()

    def snapshots(self, vm_id):
        return self.vm_conn(vm_id).snapshotListNames()

    def create_snapshot(self, vm_id, name=None):
        """
        Creates a snapshot for vm.
        """
        xml = self.create_xml_for_snapshot(name)
        self.snapshot = self.vm_conn(vm_id).snapshotCreateXML(xml)
        return self.snapshot

    def revert_snapshot(self, vm_id):
        """
        Revert to previous snapshot.
        """
        if self.snapshot is not None:
            self.vm_conn(vm_id).revertToSnapshot(self.snapshot)

    def delete_snapshot(self, vm_id):
        """
        Delete the current snapshot.
        """
        if self.snapshot is not None:
            self.snapshot.delete()
            self.snapshot = None

    def restore_snapshot(self):
        """
        Revert to previous snapshot and delete the snapshot point.
        """
        self.revert_snapshot()
        self.delete_snapshot()

    def revert_snapshot_name(self, vm_id=None, vm_name=None, snapshot_name=None):
        """

        :return:
        """
        if vm_id is not  None:
            vm = self.conn.lookupByID(vm_id)
        elif vm_name is not None:
            vm = self.conn.lookupByName(vm_name)
        try:
            vm_snapshot = vm.snapshotLookupByName(snapshot_name)
            vm.revertToSnapshot(vm_snapshot, 0)
        except Exception as e:
            print("Snapshot with name: {} not found".format(snapshot_name), e)
            print("Available snapshots for vm: {}".format(vm.snapshotListNames()))





