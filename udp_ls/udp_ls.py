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

def udp_client(host, port):
    i = 0
#    breakpoint()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        msg = f"Hello, UDP Server! {i}"

        s.sendto(msg.encode("utf-8"), (host, port))
        time.sleep(2)
        i += 1

    s.close()

def main():
    host = "0.0.0.0"
    port1 = 10001
    port2 = 10002
    port_client = 8080

    # Create a ThreadPoolExecutor with two threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Submit each listener to the executor
        executor.submit(udp_server, host, port1)
        executor.submit(udp_server, host, port2)
        executor.submit(udp_client, host, port_client)
    # The ThreadPoolExecutor will manage the threads and automatically clean up when done


if __name__ == "__main__":
    main()
