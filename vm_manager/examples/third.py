import os

from vm_manager.models.environment import Environment
from vm_manager.helpers.ssh_manager import SSHManager


"""
IMAGES_PATH - directory with images
IMAGES_WORKING_PATH - directory with images for working virtual machines
"""

env = Environment()
vm_names = []
ssh = SSHManager()
# Step 1. Prepare vms
for image in env.get_images_list():
    vm_name = env.get_vm_name_from_config(env.create_vm(image=image))
    vm_names.append(vm_name)
    writepath = '/home/msamoylov/vm_manager/vms'
    mode = 'a+' if os.path.exists(writepath) else 'r+'
    with open(writepath, mode) as f:
        if vm_name not in f.readlines():
            f.write('{}\n'.format(vm_name))

# Step 2. Prepare snapshot 'ready'
for vm in env.get_vm_ids():
    with open('/home/msamoylov/vm_manager/vms') as f:
        if env.get_vm_name(vm) in f.read():
            if len(env.snapshots_vm(vm)) == 0 or 'ready' not in env.snapshots_vm(vm):
                env.create_snapshot(vm, 'ready')
                env.suspend(vm)
# Step 3. Resume VM, revert snapshot, upload and run script, suspend vm

with open('/home/msamoylov/vm_manager/vms') as f:
    for vm in f.readlines():
        try:
            virt = vm.rstrip('\n')
            env.resume(vm_name=virt)
            env.revert_snapshot_name(vm_name=virt, snapshot_name='ready')
            vm_ip = env.get_vm_ip(vm_name=virt)
            ssh.upload_to_remote(vm_ip, 'root', 'TestRoot1',
                                '/home/msamoylov/statistics_sender/client.py',
                                '/tmp/client.py')
            cmd = 'python /tmp/client.py'
            result = ssh.exec_cmd(vm_ip, cmd)
            env.suspend(vm_name=virt)
        except Exception as e:
            print("Cannot connect to vm {}".format(virt), e)