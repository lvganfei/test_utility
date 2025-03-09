# from algorithm_service_scheduling_kernel.service_pb2 import *
# from algorithm_service_scheduling_kernel.service_pb2_grpc import *
import grpc
import service_pb2
import service_pb2_grpc
import error_pb2
import error_pb2_grpc




channel = grpc.insecure_channel('10.12.10.113:50051')

stub = service_pb2_grpc.ServiceStub(channel)


def getState():
    getStateRequest = service_pb2.GetStateRequest()
    res = stub.GetState(getStateRequest)
    print(res)

def getNumberOfGPUs():
    getNumberOfGPUsRequest = service_pb2.GetNumberOfGPUsRequest()
    res = stub.GetNumberOfGPUs(getNumberOfGPUsRequest)
    print(res)

def connectAllTaskState():
    connectAllTaskStateRequest = service_pb2.ConnectAllTaskStateRequest()

    res = stub.ConnectAllTaskState(connectAllTaskStateRequest)

    print(res)
    print(res.task_id)
    print(res.state)

def connectTaskProgress():
    connectTaskProgressRequest = service_pb2.ConnectTaskProgressRequest()
    res = stub.ConnectTaskProgress(connectTaskProgressRequest)

    print(res)
    

def commitTask():
    commitTaskRequest = service_pb2.CommitTaskRequest(
        case_id='T20220426002608H28fd5b38',
        alg_id='coronary', 
        running_mode='full', 
        config='5', 
        use_cuda=True, 
        timeout=7, 
        priority=1, 
        preposed=True)
    
    res = stub.CommitTask(commitTaskRequest)
    print(res)
if __name__ == '__main__':
    commitTask()