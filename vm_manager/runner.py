# coding=utf-8

from vm_manager.models import environment


def main():
    env = environment.Environment()
    confs = []
    for image in env.get_images_list():
        vm_name = env.get_vm_name_from_config(env.create_vm(image=image))
        confs.append(vm_name)

    print(confs)
