bl_info = {
  "name": "RPC Server",
  "blender": (4, 2, 0),
  "category": "View"}

from xmlrpc.server import SimpleXMLRPCServer
import bpy
import threading
from bpy.props import BoolProperty

HOST = "127.0.0.1"
PORT = 8000

server = None
server_thread = None

def launch_server():
    global server
    server = SimpleXMLRPCServer((HOST, PORT), allow_none=True)
    server.register_function(list_objects)
    server.register_function(import_obj)
    server.register_function(eval_code)
    server.register_function(shutdown)
    server.serve_forever()

def server_start():
    global server_thread
    if not hasattr(bpy.types.Scene, "rpc_server_running"):
        bpy.types.Scene.rpc_server_running = BoolProperty(
            name="RPC Server Running",
            description="Indicates whether the RPC server is currently running",
            default=False
        )
    if not bpy.context.scene.rpc_server_running:
        server_thread = threading.Thread(target=launch_server)
        server_thread.daemon = True
        server_thread.start()
        bpy.context.scene.rpc_server_running = True

def server_stop():
    global server, server_thread
    if bpy.context.scene.rpc_server_running:
        bpy.context.scene.rpc_server_running = False
        if server:
            server.shutdown()
        if server_thread:
            server_thread.join()
        server = None
        server_thread = None

def shutdown():
    # This function will be called via RPC to stop the server
    bpy.app.timers.register(server_stop, first_interval=0.1)
    return "Server shutdown initiated"

def list_objects():
  return bpy.data.objects.keys()
  
def import_obj(path:str):
  status = bpy.ops.import_scene.obj(filepath=path)
  return "OK"

def eval_code(code:str):
  return eval(code)


# Define a class to handle toggling the RPC server
class RPCServerToggle(bpy.types.Operator):
  bl_idname = "wm.rpc_server_toggle"
  bl_label = "Toggle RPC Server"
  def execute(self, context):
    if context.scene.rpc_server_running:
      server_stop()
    else:
      server_start()
    return {'FINISHED'}

# Define the GUI panel
class RPCServerPanel(bpy.types.Panel):
  bl_label = "RPC Server Control"
  bl_idname = "VIEW3D_PT_rpc_server"
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'UI'
  bl_category = 'RPC Server'

  def draw(self, context):
    layout = self.layout
    scene = context.scene
    layout.prop(scene, "rpc_server_running", text="Server Running")
    layout.operator("wm.rpc_server_toggle", text="Toggle Server")

# Register the operator and panel
def register():
  bpy.utils.register_class(RPCServerToggle)
  bpy.utils.register_class(RPCServerPanel)
  bpy.types.Scene.rpc_server_running = BoolProperty(
    name="RPC Server Running",
    description="Indicates whether the RPC server is currently running",
    default=False
  )

# Unregister the operator and panel
def unregister():
  bpy.utils.unregister_class(RPCServerToggle)
  bpy.utils.unregister_class(RPCServerPanel)
  del bpy.types.Scene.rpc_server_running

# Running the script
if __name__ == "__main__":
  register()
