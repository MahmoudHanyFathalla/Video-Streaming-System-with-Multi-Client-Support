import cv2
import socket
import threading
import time

# Global variables to track the video state
current_frame_index = 0
lock = threading.Lock()

# Client states
clients = {}

def broadcast_frame(video_path, fps):
    global current_frame_index  # Declare global variable at the start of this function

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Cannot open video file")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = 1 / fps  # Time interval between frames

    while True:
        with lock:
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame_index)
            ret, frame = cap.read()
            if not ret:
                current_frame_index = 0  # Restart video when it ends
                continue
            _, frame_data = cv2.imencode('.jpg', frame)

        # Send frame to all clients
        to_remove = []
        for client_socket, state in clients.items():
            try:
                client_socket.sendall(frame_data.tobytes() + b'END')
            except (ConnectionResetError, BrokenPipeError):
                to_remove.append(client_socket)

        # Remove disconnected clients
        for client_socket in to_remove:
            del clients[client_socket]

        # Increment frame index for server-side playback
        with lock:
            current_frame_index = (current_frame_index + 1) % total_frames

        time.sleep(frame_interval)

    cap.release()

def handle_client(client_socket, client_address):
    global current_frame_index  # Declare global variable at the start of this function

    clients[client_socket] = {"status": "play", "buffer": [], "index": 0}

    try:
        while True:
            command = client_socket.recv(1024).decode('utf-8').strip()
            if command == "pause":
                clients[client_socket]["status"] = "pause"
            elif command == "play":
                clients[client_socket]["status"] = "play"
            elif command == "rewind":
                clients[client_socket]["status"] = "pause"
                clients[client_socket]["index"] = max(0, clients[client_socket]["index"] - 10)  # Rewind by 10 frames
            elif command == "fast-forward":
                clients[client_socket]["status"] = "pause"
                clients[client_socket]["index"] = min(len(clients[client_socket]["buffer"]) - 1, clients[client_socket]["index"] + 10)  # Fast-forward by 10 frames
    except (ConnectionResetError, BrokenPipeError):
        print(f"Client {client_address} disconnected")
        del clients[client_socket]
    finally:
        client_socket.close()

def server(host="0.0.0.0", port=8000, video_path="kokoko.mp4", fps=30):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print("Server started. Waiting for clients...")

    # Start the video broadcasting thread
    threading.Thread(target=broadcast_frame, args=(video_path, fps), daemon=True).start()

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Client {client_address} connected")
        threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()

if __name__ == "__main__":
    server()
