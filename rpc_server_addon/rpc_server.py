bl_info = {
  "name": "RPC Server",
  "blender": (4, 2, 0)}

from xmlrpc.server import SimpleXMLRPCServer
import bpy
import threading

HOST = "127.0.0.1"
PORT = 8000

def launch_server():
  server = SimpleXMLRPCServer((HOST, PORT))
  server.register_function(list_objects)
  server.register_function(import_obj)
  server.register_function(eval_code)
  server.serve_forever()

def server_start():
  t = threading.Thread(target=launch_server)
  t.daemon = True
  t.start()
  
def list_objects():
  return bpy.data.objects.keys()
  
def import_obj(path:str):
  status = bpy.ops.import_scene.obj(filepath=path)
  return "OK"

def eval_code(code:str):
  return eval(code)


# Define a class to handle starting the RPC server
class RPCServerStarter(bpy.types.Operator):
  bl_idname = "wm.rpc_server_starter"
  bl_label = "Start RPC Server"
  def execute(self, context):
    # Start the RPC server in a separate thread
    t = threading.Thread(target=launch_server)
    t.daemon = True
    t.start()
    return {'FINISHED'}


# Register the operator
def register():
  bpy.utils.register_class(RPCServerStarter)
  # Optionally, immediately start the RPC server
  bpy.ops.wm.rpc_server_starter()

# Unregister the operator
def unregister():
  bpy.utils.unregister_class(RPCServerStarter)

# Running the script
if __name__ == "__main__":
  register()
