# coding=utf-8
# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument("square", type=int,
#                     help="display a square of a given number")
# parser.add_argument("-v", "--verbose", action="store_true",
#                     help="increase output verbosity")
# args = parser.parse_args()
# answer = args.square**2
# if args.verbose:
#     print("the square of {} equals {}".format(args.square, answer))
# else:
#     print(answer)
from vm_manager.models.environment import Environment

a = Environment()
print(a.get_vm_mac(a.get_vm_ids()[0]))
