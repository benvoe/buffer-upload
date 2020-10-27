import argparse

parser = argparse.ArgumentParser(description='Python tool to download an image from Instagram and submit it into a Buffer queue.')
parser.add_argument('-v', '--verbose', action='store_true', help='Set verbosity of script.')
subparsers = parser.add_subparsers(dest='subcommand', help='Select the functionality you like to use.')

# INIT COMMAND
parser_init = subparsers.add_parser('init')
parser_init.add_argument('username', help='Your instagram user name.')

# REPOST COMMAND
parser_repost = subparsers.add_parser('repost')
parser_repost.add_argument('username', help='Your instagram user name.')
parser_repost.add_argument('ig_link', help='Instagram Link of the image you like to repost.')

# CLEANUP COMMAND
parser_cleanup = subparsers.add_parser('cleanup')
parser_cleanup.add_argument('-a', '--all', action='store_true', help='Select to cleanup the whole workspace including posts directory.')