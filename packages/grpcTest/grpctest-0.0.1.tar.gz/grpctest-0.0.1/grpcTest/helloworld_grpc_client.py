import grpc
import helloworld_pb2
import helloworld_pb2_grpc
def run():
    channel = grpc.insecure_channel('localhost:50051')
    print('调用成功')
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(helloworld_pb2.HelloRequest(name='cz1'))
    print("Greeter client receoved:"+response.message)
    response = stub.SayHelloAgain(helloworld_pb2.HelloRequest(age='26',name='daydaygo'))
    print("Greeter client received:"+response.message)