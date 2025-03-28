# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import service_pb2 as service__pb2


class ServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetState = channel.unary_unary(
                '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/GetState',
                request_serializer=service__pb2.GetStateRequest.SerializeToString,
                response_deserializer=service__pb2.GetStateResponse.FromString,
                )
        self.ConnectState = channel.unary_stream(
                '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/ConnectState',
                request_serializer=service__pb2.ConnectStateRequest.SerializeToString,
                response_deserializer=service__pb2.ConnectStateResponse.FromString,
                )
        self.GetNumberOfGPUs = channel.unary_unary(
                '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/GetNumberOfGPUs',
                request_serializer=service__pb2.GetNumberOfGPUsRequest.SerializeToString,
                response_deserializer=service__pb2.GetNumberOfGPUsResponse.FromString,
                )
        self.ConnectNumberOfGPUs = channel.unary_stream(
                '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/ConnectNumberOfGPUs',
                request_serializer=service__pb2.ConnectNumberOfGPUsRequest.SerializeToString,
                response_deserializer=service__pb2.ConnectNumberOfGPUsResponse.FromString,
                )
        self.GetTaskQueueSize = channel.unary_unary(
                '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/GetTaskQueueSize',
                request_serializer=service__pb2.GetTaskQueueSizeRequest.SerializeToString,
                response_deserializer=service__pb2.GetTaskQueueSizeResponse.FromString,
                )
        self.ConnectTaskQueueSize = channel.unary_stream(
                '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/ConnectTaskQueueSize',
                request_serializer=service__pb2.ConnectTaskQueueSizeRequest.SerializeToString,
                response_deserializer=service__pb2.ConnectTaskQueueSizeResponse.FromString,
                )
        self.GetTaskProgress = channel.unary_unary(
                '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/GetTaskProgress',
                request_serializer=service__pb2.GetTaskProgressRequest.SerializeToString,
                response_deserializer=service__pb2.GetTaskProgressResponse.FromString,
                )
        self.ConnectTaskProgress = channel.unary_stream(
                '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/ConnectTaskProgress',
                request_serializer=service__pb2.ConnectTaskProgressRequest.SerializeToString,
                response_deserializer=service__pb2.ConnectTaskProgressResponse.FromString,
                )
        self.ConnectAllTaskProgress = channel.unary_stream(
                '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/ConnectAllTaskProgress',
                request_serializer=service__pb2.ConnectAllTaskProgressRequest.SerializeToString,
                response_deserializer=service__pb2.ConnectAllTaskProgressResponse.FromString,
                )
        self.GetTaskPriority = channel.unary_unary(
                '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/GetTaskPriority',
                request_serializer=service__pb2.GetTaskPriorityRequest.SerializeToString,
                response_deserializer=service__pb2.GetTaskPriorityResponse.FromString,
                )
        self.SetTaskPriority = channel.unary_unary(
                '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/SetTaskPriority',
                request_serializer=service__pb2.SetTaskPriorityRequest.SerializeToString,
                response_deserializer=service__pb2.SetTaskPriorityResponse.FromString,
                )
        self.GetTaskState = channel.unary_unary(
                '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/GetTaskState',
                request_serializer=service__pb2.GetTaskStateRequest.SerializeToString,
                response_deserializer=service__pb2.GetTaskStateResponse.FromString,
                )
        self.ConnectTaskState = channel.unary_stream(
                '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/ConnectTaskState',
                request_serializer=service__pb2.ConnectTaskStateRequest.SerializeToString,
                response_deserializer=service__pb2.ConnectTaskStateResponse.FromString,
                )
        self.ConnectAllTaskState = channel.unary_stream(
                '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/ConnectAllTaskState',
                request_serializer=service__pb2.ConnectAllTaskStateRequest.SerializeToString,
                response_deserializer=service__pb2.ConnectAllTaskStateResponse.FromString,
                )
        self.RevokeTask = channel.unary_unary(
                '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/RevokeTask',
                request_serializer=service__pb2.RevokeTaskRequest.SerializeToString,
                response_deserializer=service__pb2.RevokeTaskResponse.FromString,
                )
        self.KillTask = channel.unary_unary(
                '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/KillTask',
                request_serializer=service__pb2.KillTaskRequest.SerializeToString,
                response_deserializer=service__pb2.KillTaskResponse.FromString,
                )
        self.CommitTask = channel.unary_unary(
                '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/CommitTask',
                request_serializer=service__pb2.CommitTaskRequest.SerializeToString,
                response_deserializer=service__pb2.CommitTaskResponse.FromString,
                )
        self.Suicide = channel.unary_unary(
                '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/Suicide',
                request_serializer=service__pb2.SuicideRequest.SerializeToString,
                response_deserializer=service__pb2.SuicideResponse.FromString,
                )


class ServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetState(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ConnectState(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetNumberOfGPUs(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ConnectNumberOfGPUs(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTaskQueueSize(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ConnectTaskQueueSize(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTaskProgress(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ConnectTaskProgress(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ConnectAllTaskProgress(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTaskPriority(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetTaskPriority(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTaskState(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ConnectTaskState(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ConnectAllTaskState(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RevokeTask(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def KillTask(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CommitTask(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Suicide(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetState': grpc.unary_unary_rpc_method_handler(
                    servicer.GetState,
                    request_deserializer=service__pb2.GetStateRequest.FromString,
                    response_serializer=service__pb2.GetStateResponse.SerializeToString,
            ),
            'ConnectState': grpc.unary_stream_rpc_method_handler(
                    servicer.ConnectState,
                    request_deserializer=service__pb2.ConnectStateRequest.FromString,
                    response_serializer=service__pb2.ConnectStateResponse.SerializeToString,
            ),
            'GetNumberOfGPUs': grpc.unary_unary_rpc_method_handler(
                    servicer.GetNumberOfGPUs,
                    request_deserializer=service__pb2.GetNumberOfGPUsRequest.FromString,
                    response_serializer=service__pb2.GetNumberOfGPUsResponse.SerializeToString,
            ),
            'ConnectNumberOfGPUs': grpc.unary_stream_rpc_method_handler(
                    servicer.ConnectNumberOfGPUs,
                    request_deserializer=service__pb2.ConnectNumberOfGPUsRequest.FromString,
                    response_serializer=service__pb2.ConnectNumberOfGPUsResponse.SerializeToString,
            ),
            'GetTaskQueueSize': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTaskQueueSize,
                    request_deserializer=service__pb2.GetTaskQueueSizeRequest.FromString,
                    response_serializer=service__pb2.GetTaskQueueSizeResponse.SerializeToString,
            ),
            'ConnectTaskQueueSize': grpc.unary_stream_rpc_method_handler(
                    servicer.ConnectTaskQueueSize,
                    request_deserializer=service__pb2.ConnectTaskQueueSizeRequest.FromString,
                    response_serializer=service__pb2.ConnectTaskQueueSizeResponse.SerializeToString,
            ),
            'GetTaskProgress': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTaskProgress,
                    request_deserializer=service__pb2.GetTaskProgressRequest.FromString,
                    response_serializer=service__pb2.GetTaskProgressResponse.SerializeToString,
            ),
            'ConnectTaskProgress': grpc.unary_stream_rpc_method_handler(
                    servicer.ConnectTaskProgress,
                    request_deserializer=service__pb2.ConnectTaskProgressRequest.FromString,
                    response_serializer=service__pb2.ConnectTaskProgressResponse.SerializeToString,
            ),
            'ConnectAllTaskProgress': grpc.unary_stream_rpc_method_handler(
                    servicer.ConnectAllTaskProgress,
                    request_deserializer=service__pb2.ConnectAllTaskProgressRequest.FromString,
                    response_serializer=service__pb2.ConnectAllTaskProgressResponse.SerializeToString,
            ),
            'GetTaskPriority': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTaskPriority,
                    request_deserializer=service__pb2.GetTaskPriorityRequest.FromString,
                    response_serializer=service__pb2.GetTaskPriorityResponse.SerializeToString,
            ),
            'SetTaskPriority': grpc.unary_unary_rpc_method_handler(
                    servicer.SetTaskPriority,
                    request_deserializer=service__pb2.SetTaskPriorityRequest.FromString,
                    response_serializer=service__pb2.SetTaskPriorityResponse.SerializeToString,
            ),
            'GetTaskState': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTaskState,
                    request_deserializer=service__pb2.GetTaskStateRequest.FromString,
                    response_serializer=service__pb2.GetTaskStateResponse.SerializeToString,
            ),
            'ConnectTaskState': grpc.unary_stream_rpc_method_handler(
                    servicer.ConnectTaskState,
                    request_deserializer=service__pb2.ConnectTaskStateRequest.FromString,
                    response_serializer=service__pb2.ConnectTaskStateResponse.SerializeToString,
            ),
            'ConnectAllTaskState': grpc.unary_stream_rpc_method_handler(
                    servicer.ConnectAllTaskState,
                    request_deserializer=service__pb2.ConnectAllTaskStateRequest.FromString,
                    response_serializer=service__pb2.ConnectAllTaskStateResponse.SerializeToString,
            ),
            'RevokeTask': grpc.unary_unary_rpc_method_handler(
                    servicer.RevokeTask,
                    request_deserializer=service__pb2.RevokeTaskRequest.FromString,
                    response_serializer=service__pb2.RevokeTaskResponse.SerializeToString,
            ),
            'KillTask': grpc.unary_unary_rpc_method_handler(
                    servicer.KillTask,
                    request_deserializer=service__pb2.KillTaskRequest.FromString,
                    response_serializer=service__pb2.KillTaskResponse.SerializeToString,
            ),
            'CommitTask': grpc.unary_unary_rpc_method_handler(
                    servicer.CommitTask,
                    request_deserializer=service__pb2.CommitTaskRequest.FromString,
                    response_serializer=service__pb2.CommitTaskResponse.SerializeToString,
            ),
            'Suicide': grpc.unary_unary_rpc_method_handler(
                    servicer.Suicide,
                    request_deserializer=service__pb2.SuicideRequest.FromString,
                    response_serializer=service__pb2.SuicideResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Service(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetState(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/GetState',
            service__pb2.GetStateRequest.SerializeToString,
            service__pb2.GetStateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ConnectState(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/ConnectState',
            service__pb2.ConnectStateRequest.SerializeToString,
            service__pb2.ConnectStateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetNumberOfGPUs(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/GetNumberOfGPUs',
            service__pb2.GetNumberOfGPUsRequest.SerializeToString,
            service__pb2.GetNumberOfGPUsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ConnectNumberOfGPUs(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/ConnectNumberOfGPUs',
            service__pb2.ConnectNumberOfGPUsRequest.SerializeToString,
            service__pb2.ConnectNumberOfGPUsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetTaskQueueSize(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/GetTaskQueueSize',
            service__pb2.GetTaskQueueSizeRequest.SerializeToString,
            service__pb2.GetTaskQueueSizeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ConnectTaskQueueSize(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/ConnectTaskQueueSize',
            service__pb2.ConnectTaskQueueSizeRequest.SerializeToString,
            service__pb2.ConnectTaskQueueSizeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetTaskProgress(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/GetTaskProgress',
            service__pb2.GetTaskProgressRequest.SerializeToString,
            service__pb2.GetTaskProgressResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ConnectTaskProgress(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/ConnectTaskProgress',
            service__pb2.ConnectTaskProgressRequest.SerializeToString,
            service__pb2.ConnectTaskProgressResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ConnectAllTaskProgress(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/ConnectAllTaskProgress',
            service__pb2.ConnectAllTaskProgressRequest.SerializeToString,
            service__pb2.ConnectAllTaskProgressResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetTaskPriority(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/GetTaskPriority',
            service__pb2.GetTaskPriorityRequest.SerializeToString,
            service__pb2.GetTaskPriorityResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetTaskPriority(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/SetTaskPriority',
            service__pb2.SetTaskPriorityRequest.SerializeToString,
            service__pb2.SetTaskPriorityResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetTaskState(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/GetTaskState',
            service__pb2.GetTaskStateRequest.SerializeToString,
            service__pb2.GetTaskStateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ConnectTaskState(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/ConnectTaskState',
            service__pb2.ConnectTaskStateRequest.SerializeToString,
            service__pb2.ConnectTaskStateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ConnectAllTaskState(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/ConnectAllTaskState',
            service__pb2.ConnectAllTaskStateRequest.SerializeToString,
            service__pb2.ConnectAllTaskStateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RevokeTask(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/RevokeTask',
            service__pb2.RevokeTaskRequest.SerializeToString,
            service__pb2.RevokeTaskResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def KillTask(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/KillTask',
            service__pb2.KillTaskRequest.SerializeToString,
            service__pb2.KillTaskResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CommitTask(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/CommitTask',
            service__pb2.CommitTaskRequest.SerializeToString,
            service__pb2.CommitTaskResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Suicide(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/algorithm_engineering.beggar_algorithm_service_system.algorithm_service_scheduling_kernel.Service/Suicide',
            service__pb2.SuicideRequest.SerializeToString,
            service__pb2.SuicideResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
