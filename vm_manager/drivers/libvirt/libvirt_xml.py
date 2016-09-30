# coding=utf-8
from xml.dom import minidom
from xml.etree import ElementTree as ET
from vm_manager.templates.qcow2_templates import template
from vm_manager.helpers.utils import mac_address_generator as mac_gen


class LibvirtXmlManager(object):
    def __init__(self):
        self.template = template
        self.root = ET.fromstring(self.template)

    def get_mac(self, dom_xml):
        xml = minidom.parseString(dom_xml)
        interfaceTypes = xml.getElementsByTagName('interface')
        for interfaceType in interfaceTypes:
            interfaceNodes = interfaceType.childNodes
            for interfaceNode in interfaceNodes:
                if interfaceNode.nodeName == 'mac':
                    for attr in interfaceNode.attributes.keys():
                        return interfaceNode.attributes[attr].value

    def build_domain_xml(self, vm_name='default', source_image='default.qcow2', vcpu_count="1",
                         memory="1"):
        root = self.root
        #Change mac in template
        root.find(".//mac").attrib['address'] = mac_gen()

        #Change vm_name in template
        root.find('.//name').text = vm_name.rstrip('.qcow2')

        #Set source_image file
        root.find('.//source').attrib['file'] = source_image
        #Set memory
        root.find('.//memory').text = memory

        #Set vcpu
        root.find('.//vcpu').text = vcpu_count


        return ET.tostring(root)

