#!/usr/bin/python3
# Copyright (c) 2019 Nippon Telegraph and Telephone Corporation

import sys
import os

from oslo_config import cfg
from oslo_log import log as logging

from birdwatcher.congress.datalog import base as datalog_base
from birdwatcher.congress.datalog import database
from birdwatcher.congress.datalog import nonrecursive
from birdwatcher.congress.datalog import compile
from birdwatcher.congress.datalog import materialized
from birdwatcher.congress.datalog import utility
from birdwatcher.congress.tests import helper
from birdwatcher.congress.policy_engines import agnostic

from birdwatcher.congress.db import db_policy_rules


from birdwatcher.congress import exception

LOG = logging.getLogger(__name__)

common_opts = [
    cfg.StrOpt('rules',
               short='r',
               default='rules.datalog',
               help='ruls'),
    cfg.StrOpt('query',
               short='q',
               default='querys.datalog',
               help='query')
]

if __name__ == '__main__' :
    conf = cfg.ConfigOpts()
    conf.register_cli_opts(common_opts)
    conf(sys.argv[1:])

    # print('rules %s' % (conf.rules, ))
    # print('querys %s' % (conf.query, ))

    default_policy = "default"
    run = agnostic.Runtime()
    run.create_policy(default_policy)

    for l in open(os.path.join(os.getcwd(), conf.rules)).readlines():
        run.insert(l)

    err_count=0
    for l in open(os.path.join(os.getcwd(), conf.query)).readlines():
        ans = run.select(l)
        if ans != '':
            err_count += 1
            print(ans)
        
