# coding=utf-8

template = """<domain type='kvm'>
  <name>default</name>
  <uuid>f5b8c05b-9c7a-3211-49b9-2bd635f7e2aa</uuid>
  <memory unit='GB'>1</memory>
  <vcpu>1</vcpu>
  <os>
    <type>hvm</type>
    <boot dev='hd'/>
  </os>
  <features>
    <acpi/>
  </features>
  <clock offset='utc'/>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>destroy</on_crash>
  <devices>
    <emulator>/usr/bin/kvm</emulator>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2' cache='none'/>
      <source file='/home/msamoylov/postgres_images/standalone.qcow2'/>
      <target dev='vda' bus='virtio'/>
    </disk>
    <interface type='bridge'>
      <mac address='52:87:93:76:1d:37'/>
      <source bridge='virbr0'/>
      <model type='virtio'/>
    </interface>
    <input type='tablet' bus='usb'/>
    <input type='mouse' bus='ps2'/>
    <graphics type='vnc' port='-1' listen='127.0.0.1'/>
  </devices>
</domain>
"""
