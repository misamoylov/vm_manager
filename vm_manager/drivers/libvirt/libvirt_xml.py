# coding=utf-8
from xml.dom import minidom
from xml.etree import ElementTree as ET
from vm_manager.templates.qcow2_templates import template


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
