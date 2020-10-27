#!/usr/bin/env python3

import argparse
from pathlib import Path

from utils.arguments import parser
from utils.subcmd import initialize, repost, cleanup

args = vars(parser.parse_args())
basedir = Path(__file__).absolute().parent

if args['subcommand'] == 'init':
    initialize(basedir, args['username'])
elif args['subcommand'] == 'repost':
    repost(basedir, args['username'], args['ig_link'])
elif args['subcommand'] == 'cleanup':
    cleanup(basedir, args['all'])
