import socket
import time
import threading
import matplotlib.pyplot as plt
import random

PORT = 8080
BUFFER_SIZE = 1024
DATA_SIZE = 100000000
SAMPLE_INTERVAL = 1
HOST = '127.0.0.1'
INITIAL_CWND = 10
MSS = BUFFER_SIZE
VEGAS_INC = 1
VEGAS_DEC = 0.5
VEGAS_TARGET_RTT = 0.05

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print("Server listening on port", PORT)

    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    while True:
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            break
        time.sleep(0.01)
        client_socket.send(b'ACK')
    client_socket.close()
    server_socket.close()
    print("Server connection closed.")

def simulate_tcp_vegas():
    times = []
    throughputs = []

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = (HOST, PORT)
    sock.connect(server_addr)

    buffer = b'A' * BUFFER_SIZE
    start_time = time.time()
    bytes_sent = 0
    last_bytes_sent = 0
    last_time = time.time()

    cwnd = INITIAL_CWND
    rtt_estimate = VEGAS_TARGET_RTT

    while bytes_sent < DATA_SIZE:
        current_time = time.time()
        sock.send(buffer[:MSS])

        send_time = time.time()
        sock.recv(BUFFER_SIZE)

        rtt = time.time() - send_time

        if rtt < VEGAS_TARGET_RTT:
            cwnd += VEGAS_INC
        elif rtt > VEGAS_TARGET_RTT:
            cwnd = max(1, int(cwnd * VEGAS_DEC))

        bytes_sent += MSS

        elapsed_time = current_time - start_time
        if elapsed_time - (last_time - start_time) >= SAMPLE_INTERVAL:
            throughput = (bytes_sent - last_bytes_sent) / (elapsed_time - (last_time - start_time)) / (1024 * 1024)
            times.append(elapsed_time)
            throughputs.append(throughput)
            print(f"Time: {elapsed_time:.2f}s, Throughput: {throughput:.2f} MB/s, cwnd: {cwnd} segments, RTT: {rtt:.4f}s")
            last_time = current_time
            last_bytes_sent = bytes_sent

    sock.close()
    return times, throughputs

def main():
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    time.sleep(1)

    print("Simulating TCP Vegas throughput...")

    times, throughputs = simulate_tcp_vegas()

    if times and throughputs:
        plt.plot(times, throughputs, label='Throughput (MB/s)', color='blue')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Throughput (MB/s)')
        plt.title('TCP Vegas Throughput Simulation')
        plt.legend()
        plt.grid(True)
        plt.show()
    else:
        print("No data collected. Check the throughput calculation interval and ensure data is being sent.")

if __name__ == '__main__':
    main()
