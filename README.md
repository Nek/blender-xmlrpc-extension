# Blender RPC Control

This project provides a system for remote interaction with Blender using XML-RPC. It consists of a Python server that runs as a Blender addon and a Clojure client that can make calls to this server to perform operations in Blender remotely.

## Project Description

The system allows for automation of Blender operations, integration of Blender with other software, and control of Blender from external scripts or applications. The server exposes various Blender operations via RPC, which can be called by the client.

## Requirements

### Server (Blender Addon)
- Blender 4.2.0 or later
- Python 3.x (included with Blender)

### Client (Clojure)
- Clojure 1.11.2 or later
- Java Development Kit (JDK) 17 or later

## Setup and Running

1. Install the Blender addon:
   - Copy the `rpc_server_addon` folder to Blender's addon directory.
   - Enable the "RPC Server" addon in Blender's preferences.

2. Start the RPC server in Blender:
   - Open Blender.
   - In the 3D Viewport, find the "RPC Server" panel in the sidebar.
   - Click "Run Server" to start the XML-RPC server.

3. Set up the Clojure client:
   - Ensure you have Clojure and the required dependencies installed.
   - Navigate to the `rpc-client-clj` directory.
   - Run the client using your preferred method (e.g., `clj -M -m client`).

## Available RPC Calls

The server exposes the following RPC methods:

1. `list_objects()`: Returns a list of all object names in the current Blender scene.
2. `import_obj(path)`: Imports an OBJ file at the specified path.
3. `eval_code(code)`: Evaluates the given Python code in Blender's context.
4. `move_object(object_name, x, y, z)`: Moves the specified object to the given coordinates.
5. `send_a(v)`, `send_b(v)`, `send_c(v)`, `send_d(v)`: Sets the values of variables a, b, c, and d respectively.

Example usage from the Clojure client:

```clojure
(xml-rpc/call "http://localhost:8000" :eval_code "bpy.data.objects.keys()")
```

This call will return a list of all object names in the current Blender scene.

## Note

Ensure that Blender is running and the RPC server is started before attempting to use the Clojure client.
