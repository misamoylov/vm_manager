# coding=utf-8
import sys
import argparse

from vm_manager.models.environment import Environment


class Shell(Environment):
    def __init__(self, args):
        self.args = args
        self.params = self.get_params()

    def execute(self):
        command_name = 'do_{}'.format(self.params.command.replace('-', '_'))
        command_method = getattr(self, command_name)
        command_method()


    def do_image_list(self):
        self.get_images_list()

    def get_params(self):
        images_parser = argparse.ArgumentParser(add_help=False)
        images_parser.add_argument('images', action='store_const', const=self.do_image_list(),
                                   dest='image-list')

        # parser = argparse.ArgumentParser(
        #     description="Virtual Machines Manager. "
        #                 "For additional help, use with -h/--help option")
        # subparsers = parser.add_subparsers(title="Operation commands",
        #                                    help='available commands',
        #                                    dest='command')
        # subparsers.add_parser('list',
        #                       parents=[images_parser],
        #                       help="Show virtual machines",
        #                       description="Show virtual machines on host")

        if len(self.args) == 0:
            self.args = ['-h']
        return images_parser.parse_args(self.args)


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    shell = Shell(args)
    shell.execute()
