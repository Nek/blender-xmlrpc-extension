bl_info = {
  "name": "RPC Server",
  "blender": (4, 2, 0),
  "category": "View"}

from xmlrpc.server import SimpleXMLRPCServer
import bpy
import threading
from bpy.props import BoolProperty
import mathutils   

HOST = "127.0.0.1"
PORT = 8000

server = None
server_thread = None

a = None
b = None
c = None
d = None

def launch_server():
    global server
    server = SimpleXMLRPCServer((HOST, PORT), allow_none=True)
    server.register_function(list_objects)
    server.register_function(import_obj)
    server.register_function(eval_code)
    server.register_function(send_a)
    server.register_function(send_b)
    server.register_function(send_c)
    server.register_function(send_d)
    server.register_function(move_object)
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

def list_objects():
  return bpy.data.objects.keys()
  
def import_obj(path:str):
  status = bpy.ops.import_scene.obj(filepath=path)
  return "OK"

def eval_code(code:str):
  return eval(code)

def send_a(v):
  a = v
  return "OK"

def send_b(v):
  b = v
  return "OK"

def send_c(v):
  c = v
  return "OK"

def send_d(v):
  d = v
  return "OK"

def move_object(object_name: str, x: float, y: float, z: float):                                                                                         
    obj = bpy.data.objects.get(object_name)                                                                                                              
    if obj is None:                                                                                                                                      
        return f"Object '{object_name}' not found"                                                                                                       
                                                                                                                                                        
    obj.location = mathutils.Vector((x, y, z))                                                                                                           
    return f"Moved '{object_name}' to position ({x}, {y}, {z})"    


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
  bl_label = "Python XMLRPC Server"
  bl_idname = "VIEW3D_PT_rpc_server"
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'UI'
  bl_category = 'RPC Server'

  def draw(self, context):
    layout = self.layout
    scene = context.scene   
    label = "Stop Server" if scene.rpc_server_running else "Run Server"         
    layout.operator("wm.rpc_server_toggle", text=label)

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
