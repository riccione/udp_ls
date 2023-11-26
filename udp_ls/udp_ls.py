import socket
import concurrent.futures
import time


def udp_server(host, port):
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Bind the socket to the specified port
        sock.bind((host, port))
        print(f"Listening on UDP port {port}...")

        while True:
            # Receive data from the socket
            data, addr = sock.recvfrom(1024)
            print(f"Received data from {addr} on port {port}: {data.decode('utf-8')}")


def tcp_server(host, port):
    # breakpoint()
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Bind the socket to the specified port
        sock.bind((host, port))
        sock.listen(5)  # max number of queued conns
        print(f"Listening on TCP port {port}...")

        while True:
            # Receive data from the socket
            conn, addr = sock.accept()
            print(f"Connection established from {addr}")
            data = conn.recv(1024)
            print(f"Received data: {data.decode('utf-8')}")


def client(protocol, host, port):
    i = 0
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if protocol == "UDP":
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg = f"Hello, UDP Server! {i}"
        if protocol == "UDP":
            s.sendto(msg.encode("utf-8"), (host, port))
        else:
            s.connect((host, port))
            s.sendall(msg.encode("utf-8"))
        time.sleep(2)
        i += 1
        s.close()


def main():
    host = "127.0.0.1"
    port1 = 10001
    port2 = 10002
    port_client = 8080
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Submit each listener to the executor
        executor.submit(client, "TCP", host, 8080)
        executor.submit(tcp_server, host, 10001)
        executor.submit(tcp_server, host, 10002)
        # The ThreadPoolExecutor will manage the threads and automatically clean up when done


if __name__ == "__main__":
    main()
