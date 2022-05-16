from imp import reload
import sys
import threading
from .dependencies import unreal
from .dependencies.rpc import maya_server

if sys.version_info.major == 2:
    reload(unreal)

def start_RPC_servers():
    unreal.bootstrap_unreal_with_rpc_server()

    # start the blender rpc server if its not already running
    if 'MayaRPCServer' not in [thread.name for thread in threading.enumerate()]:
        rpc_server = maya_server.RPCServer()
        rpc_server.start(threaded=True)
