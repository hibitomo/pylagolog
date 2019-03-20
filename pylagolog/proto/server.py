import sys
import grpc
from concurrent import futures

from oslo_config import cfg
from oslo_log import log as logging

import time
from pylagolog.proto import pylagolog_pb2
from pylagolog.proto import pylagolog_pb2_grpc

from pylagolog.congress.policy_engines import agnostic

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

LOG = logging.getLogger(__name__)
CONF = cfg.CONF
DOMAIN = "lagolog-server"

logging.register_options(CONF)
logging.setup(CONF, DOMAIN)

common_opts = [
    cfg.StrOpt('port',
        short='p',
        default='[::]:10484',
        help='An insecure port for accepting RPCs'),
]

class DatalogServicer(pylagolog_pb2_grpc.DatalogServicer):

    def __init__(self, runtime):
        self.run = runtime
        return

    def ModRules(self, request_iterator, context):
        LOG.info("ModRules:")
        for command in request_iterator:
            if command.Type == pylagolog_pb2.ADD :
                LOG.info("ADD: %s" % command.Rule)
                self.run.insert(command.Rule)
            else :
                LOG.info("DEL: %s" % command.Rule)
                self.run.delete(command.Rule)
        return pylagolog_pb2.Result(Result = pylagolog_pb2.SUCCESS)

    def Queries(self, request_iterator, context):
        results = []
        for query in request_iterator:
            LOG.info("Query: %s" % query.Query)
            ans = self.run.select(query.Query)
            if ans != "":
                results.append(pylagolog_pb2.QueryResult(Result=ans))
        LOG.info("ANS: %s" % results)
        for result in results:
            yield result
    
def serve():
    conf = cfg.ConfigOpts()
    conf.register_cli_opts(common_opts)
    conf(sys.argv[1:])
    policy = "default"
    run = agnostic.Runtime()
    run.create_policy(policy)
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pylagolog_pb2_grpc.add_DatalogServicer_to_server(
        DatalogServicer(run), server)
    server.add_insecure_port(conf.port)
    LOG.info("Server Start %s" % (conf.port))
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
