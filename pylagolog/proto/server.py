import grpc
from concurrent import futures

import time
from pylagolog.proto import pylagolog_pb2
from pylagolog.proto import pylagolog_pb2_grpc

from pylagolog.congress.policy_engines import agnostic

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class DatalogServicer(pylagolog_pb2_grpc.DatalogServicer):

    def __init__(self, runtime):
        self.run = runtime
        return

    def ModRules(self, request_iterator, context):
        print("ModRules")
        for command in request_iterator:
            self.run.insert(command.Rule)
        return pylagolog_pb2.Result(Result = pylagolog_pb2.SUCCESS)

    def Queries(self, request_iterator, context):
        print("Queries")
        results = []
        for query in request_iterator:
            ans = self.run.select(query.Query)
            results.append(pylagolog_pb2.QueryResult(Result=ans))
        for result in results:
            yield result
    
def serve():
    policy = "default"
    run = agnostic.Runtime()
    run.create_policy(policy)
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pylagolog_pb2_grpc.add_DatalogServicer_to_server(
        DatalogServicer(run), server)
    server.add_insecure_port('[::]:10484')
    print("Server Start")
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
