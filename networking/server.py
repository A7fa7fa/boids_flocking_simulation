from networking.sock.sock import MySocket, ADDR
import threading


msg = {"type": "test_info", "body": {"msg": "This is a test."}}


def handle_client(conn, addr: tuple, flock):
    """handels new connection in separate thread"""

    print(f"[NEW CONNECTION] {addr} connected." )

    client_msg = conn.recv_msg()

    if not client_msg: 
        print('no message')

    print(f"Received: {client_msg}")

    # do stuff here
    while True:
        flock.calc()
        try:
            conn.send_msg(flock.dictify())
        except Exception as e:
            #print(e)
            break
    
    conn.sock.close()
    print(f'[CLIENT DISCONNECTED] {addr}')



def server(flock):

    
    flock.calc()

    #create a costume socket of MySocket Class
    server = MySocket()

    #bind it to the public interface
    server.sock.bind(ADDR)


    # Enable a server to accept connections. 
    # If backlog is specified, it must be at least 0 (if it is lower, it is set to 0); 
    # it specifies the number of unaccepted connections that the system will allow before refusing new connections. 
    # If not specified, a default reasonable value is chosen.
    # The backlog parameter is now optional.
    server.sock.listen(5)
    print(f'[SERVER] is listening on {ADDR}')

    while True:
        conn, addr = server.sock.accept()
        conn = MySocket(sock=conn)

        # only handle one connection - TODO only allow own webserver to connect
        handle_client(conn, addr, flock)
        
        #print(f"ACTIVE CONNECTIONS {threading.active_count() -1}")


