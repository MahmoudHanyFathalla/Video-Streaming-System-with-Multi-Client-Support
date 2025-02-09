# Video Streaming System with Multi-Client Support

## Overview
This project is a **real-time video streaming system** that allows multiple clients to connect to a central server, which streams video frames efficiently. It supports key playback controls like **play, pause, and rewind**, ensuring a seamless viewing experience.

The system is designed using **multi-threading** and **socket programming**, enabling smooth data transmission and concurrent handling of multiple clients. The video data is encoded in **JPEG format** and transmitted via **TCP sockets**, ensuring reliability.

## Features
- **Multi-client Support**: Multiple clients can connect to the server and receive video frames concurrently.
- **Thread-safe Buffering**: Uses `deque` with thread locking to ensure proper frame storage.
- **Playback Controls**: Clients can control playback (play, pause, rewind) independently.
- **Real-time Streaming**: Frames are broadcasted in real-time while maintaining efficient memory usage.
- **Synchronization Mechanism**: Ensures smooth frame transitions across multiple clients.

## Technologies Used
### Programming Languages:
- **Python** (Primary Language)

### Libraries:
- **OpenCV (`cv2`)** – For video capture, processing, and encoding.
- **Socket (`socket`)** – For network communication between server and clients.
- **Threading (`threading`)** – For concurrent execution of tasks.
- **NumPy (`numpy`)** – For efficient frame handling.
- **Deque (`collections.deque`)** – For managing frame buffers efficiently.

## Architecture & Data Structures
The project follows a **client-server architecture**, where the server is responsible for:
- **Reading video frames** from a file.
- **Encoding frames** into JPEG format.
- **Transmitting frames** over a TCP connection.
- **Handling multiple client connections** via multi-threading.

Each **client** receives video frames, decodes them, and displays the stream. It also manages a **frame buffer** using `deque`, allowing control over playback.

### Key Data Structures:
1. **Frame Buffer (`deque`)**:
   - Stores up to `300` frames.
   - Supports real-time playback, pause, and rewind.
   - Thread-safe implementation using `threading.Lock()`.

2. **Client Dictionary (`clients` in server)**:
   - Keeps track of connected clients.
   - Stores playback states for each client.

## Multi-threading & Multi-client Handling
The project extensively uses multi-threading to achieve concurrency:
- **Server Side**:
  - **Main Thread**: Accepts client connections.
  - **Broadcast Thread**: Continuously sends frames to all clients.
  - **Client Handler Threads**: Each client has its own thread to handle commands.

- **Client Side**:
  - **Frame Reception Thread**: Receives frames from the server.
  - **Display Thread**: Renders the frames in real-time.
  - **Main Thread**: Handles user input for playback control.

## How It Works
### Server (`server.py`):
1. Loads the video file and captures frames using OpenCV.
2. Converts each frame to a **JPEG** format for efficient transmission.
3. Sends frames to all connected clients.
4. Handles client requests for **play, pause, and rewind**.
5. Continuously updates the frame index, restarting the video when needed.

### Client (`clint.py`):
1. Connects to the server using a TCP socket.
2. Receives and stores frames in a **thread-safe buffer (`deque`)**.
3. Displays frames using OpenCV.
4. Listens for user commands (`play`, `pause`, `rewind`).

## Commands & Controls
Clients can issue the following commands:
- **play**: Starts/resumes video playback.
- **pause**: Freezes the current frame.
- **rewind**: Plays frames in reverse order.
- **ai**: Executes an external AI-based football analysis script.

## Setup & Execution
### Prerequisites:
Ensure you have Python and the required dependencies installed:
```sh
pip install opencv-python numpy
```

### Running the Server:
```sh
python server.py
```

### Running the Client:
```sh
python clint.py
```

## Future Improvements
- **Adaptive Bitrate Streaming**: Optimize frame size based on network conditions.
- **Frame Synchronization**: Improve buffering to reduce delays.
- **GUI-based Controls**: Enhance user experience with a graphical interface.
- **Cloud Streaming**: Deploy the server on a cloud platform for wider accessibility.

## Conclusion
This project provides an efficient real-time video streaming solution using **multi-threading, socket programming, and OpenCV**. It demonstrates how to handle multiple clients concurrently while maintaining smooth playback and user interaction.

---
Developed by **Mahmoud Hany**
