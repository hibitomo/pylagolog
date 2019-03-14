import grpc
from pylagolog.proto import pylagolog_pb2
from pylagolog.proto import pylagolog_pb2_grpc

def gen_message():
    messages = [
        pylagolog_pb2.ModifyRule(Type=pylagolog_pb2.ADD, Rule="q1(x) :- p(x)."),
        pylagolog_pb2.ModifyRule(Type=pylagolog_pb2.ADD, Rule="p('test')."),
    ]
    for msg in messages:
        yield msg

def mod_rules(stub):
    response = stub.ModRules(gen_message())
    print(response)

def gen_queries():
    messages = [
        pylagolog_pb2.Query(Query="q1(x)"),
    ]
    for msg in messages:
        yield msg
    
def queries(stub):
    responses = stub.Queries(gen_queries())
    for response in responses:
        print(response)
    
    
def run():
    with grpc.insecure_channel('0.0.0.0:10484') as channel:
        stub = pylagolog_pb2_grpc.DatalogStub(channel)
        print("Modyfy Rules")
        mod_rules(stub)
        queries(stub)

rif __name__ == '__main__':
    run()
