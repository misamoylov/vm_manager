# coding=utf-8
import random


def mac_address_generator():
    """Generate a random mac address

    :return: string: mac address
    """
    mac = [0x00, 0x16, 0x3e,
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))


def uuid_generator():
    """Generate a random UUID"""
    uuid = [random.randint(0, 255) for r in range(0, 16)]
    return uuid_to_string(uuid)


def uuid_to_string(uuid):
    return "-".join(["%02x" * 4, "%02x" * 2, "%02x" * 2, "%02x" * 2,
                     "%02x" * 6]) % tuple(uuid)
