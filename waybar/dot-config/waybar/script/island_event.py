import sys
import socket

if __name__ == "__main__":
    conn = socket.create_connection(("127.0.0.1", 11451))
    match sys.argv[1]:
        case "click":
            conn.send(b"rmbc")
            
