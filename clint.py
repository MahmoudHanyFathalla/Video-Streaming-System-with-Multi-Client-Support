import cv2
import socket
import threading
import numpy as np
import time
from collections import deque

# Buffer to store frames (thread-safe)
frame_buffer = deque(maxlen=300)  # Store up to 300 frames
current_frame_index = 0
status = "play"  # Can be "play", "pause", "rewind"
resize_factor = 0.2  # Resize factor for video window
lock = threading.Lock()  # To synchronize buffer access


def receive_frames(client_socket):
    """Thread to receive frames from the server."""
    global frame_buffer

    while True:
        frame_data = b""
        while True:
            part = client_socket.recv(4096)
            frame_data += part
            if b'END' in part:
                break

        if frame_data:
            # Decode and store frame into buffer
            frame_data = frame_data[:-3]  # Remove 'END' marker
            with lock:
                frame_buffer.append(frame_data)


def display_video():
    """Thread to display video frames."""
    global current_frame_index, status

    while True:
        if status == "play":
            with lock:
                if current_frame_index < len(frame_buffer):
                    frame_data = frame_buffer[current_frame_index]
                    current_frame_index += 1
                else:
                    time.sleep(0.01)
                    continue

            # Decode and display the frame
            frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
            if frame is not None:
                frame_resized = cv2.resize(frame, None, fx=resize_factor, fy=resize_factor)
                cv2.imshow("Video Stream", frame_resized)

        elif status == "rewind":
            with lock:
                if current_frame_index > 0:
                    frame_data = frame_buffer[current_frame_index - 1]
                    current_frame_index -= 1
                else:
                    time.sleep(0.01)
                    continue

            # Decode and display the frame
            frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
            if frame is not None:
                frame_resized = cv2.resize(frame, None, fx=resize_factor, fy=resize_factor)
                cv2.imshow("Video Stream", frame_resized)

        elif status == "pause":
            time.sleep(0.1)  # Pause for a short duration

        # Ensure the OpenCV window stays responsive
        cv2.waitKey(1)


def client():
    """Main client function to handle user inputs."""
    global current_frame_index, status

    # Set up client socket connection to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8000))

    # Start threads for receiving frames and displaying video
    threading.Thread(target=receive_frames, args=(client_socket,), daemon=True).start()
    threading.Thread(target=display_video, daemon=True).start()

    # Handle user inputs for controlling playback
    while True:
        command = input("Enter command (play/pause/rewind): ").strip()
        if command == "pause":
            status = "pause"
        elif command == "play":
            status = "play"
        elif command == "rewind":
            with lock:
                status = "rewind"
        elif command == "ai":
            with lock:
                import subprocess
                subprocess.run(["python", "C:\\Users\\hp\\Desktop\\KoraState\\football_analysis-main\\football_analysis-main\\main.py"])


        time.sleep(0.1)  # Prevent command input flooding


if __name__ == "__main__":
    client()
