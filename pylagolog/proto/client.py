import sys
import grpc

from oslo_config import cfg
from oslo_log import log as logging

from pylagolog.proto import pylagolog_pb2
from pylagolog.proto import pylagolog_pb2_grpc

common_opts = [
    cfg.StrOpt('add',
               short='a',
               help='Add a rule'),
    cfg.StrOpt('delete',
               short='d',
               help='Delete a rule'),
    cfg.StrOpt('query',
               short='q',
               help='Query')
]

def gen_message(type, message):
    messages = [
        pylagolog_pb2.ModifyRule(Type=type, Rule=message),
    ]
    for msg in messages:
        yield msg

def gen_queries(query):
    messages = [
        pylagolog_pb2.Query(Query=query),
    ]
    for msg in messages:
        yield msg
    
    
def client():
    conf = cfg.ConfigOpts()
    conf.register_cli_opts(common_opts)
    conf(sys.argv[1:])

    with grpc.insecure_channel('0.0.0.0:10484') as channel:
        stub = pylagolog_pb2_grpc.DatalogStub(channel)
        if conf.add != None :
            response = stub.ModRules(gen_message(pylagolog_pb2.ADD, conf.add))
            if response.Result == pylagolog_pb2.SUCCESS :
                print("ADD: %s\n" % conf.add)
            else :
                print("Fail ADD: %s\n" % conf.add)
        if conf.delete != None :
            response = stub.ModRules(gen_message(pylagolog_pb2.DELETE, conf.delete))
            if response.Result == pylagolog_pb2.SUCCESS :
                print("DEL: %s\n" % conf.delete)
            else :
                print("Fail DEL: %s\n" % conf.delete)
        if conf.query != None :
            responses = stub.Queries(gen_queries(conf.query))
            for response in responses:
                print(response)

