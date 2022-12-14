# Copyright Epic Games, Inc. All Rights Reserved.

import os
import sys
from . import base_server
from .base_server import BaseRPCServerThread, BaseRPCServerManager


def execute_queued_calls():
    """
    Adds calls in the execution que that get picked up by blender app timer.
    :return float: The amount of time between timer calls.
    """
    try:
        base_server.execute_queued_calls()
    except Exception as error:
        sys.stderr.write(str(error))
    return 0.02


class MayaRPCServerThread(BaseRPCServerThread):
    def thread_safe_call(self, callable_instance, *args):
        """
        Implementation of a thread safe call in Blender.
        """
        return lambda *args: base_server.run_in_main_thread(callable_instance, *args)


class RPCServer(BaseRPCServerManager):
    def __init__(self):
        """
        Initialize the blender rpc server, with its name and specific port.
        """
        if sys.version_info.major == 3:
            super().__init__()
        else:
            super(RPCServer, self).__init__()
        self.name = 'MayaRPCServer'
        self.port = int(os.environ.get('RPC_PORT', 9996))
        self.threaded_server_class = MayaRPCServerThread

    def start_server_thread(self):
        """
        Starts the server thread.
        """
        import maya.api.OpenMaya as OpenMaya
        def _call_back(*args):
            execute_queued_calls()
        OpenMaya.MTimerMessage.addTimerCallback(1, _call_back)
        super(RPCServer, self).start_server_thread()
