import os

from devops.drivers.libvirt.libvirt_driver import LibvirtManager as Manager
from devops.settings import IMAGES_PATH
from devops.templates import qcow2_templates as config


class Environment(object):

    def get_images_list(self):
        return os.listdir(IMAGES_PATH)

    def vm_config(self, name='default', memory='1', vcpu='1', image_name='ubuntu-12.04.qcow2'):
        return config.template2.format(name, memory, vcpu, image_name)

    def prepare_vm(self, vm_ip):
        pass

    def download_sources_postgrespro_from_gitlab(self, branch):
        pass

    def install_postgrespro_from_sources(self):
        pass

    def install_postgrespro_from_repos(self):
        pass
