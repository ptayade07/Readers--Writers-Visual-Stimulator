📗 Readers–Writers Synchronization Simulator
A high-fidelity, real-time visualization of the classic Readers-Writers Problem in operating systems. This simulator demonstrates thread synchronization, concurrency control, and semaphore-based locking mechanisms using a modern, dark-themed Python GUI.

🚀 Overview
The Readers–Writers problem is a classic synchronization challenge where multiple threads (Readers and Writers) share a single resource. This application simulates the First Readers-Writers Problem, which prevents "reader starvation" by allowing multiple readers to access the data simultaneously while ensuring writers have exclusive access.

Features
Real-time Thread Tracking: Watch Reader and Writer blocks change states dynamically as they acquire locks.

Synchronized Visuals: Graphical connecting lines show the flow of data between shared memory and active threads.

Detailed Activity Log: A live console tracking every lock acquisition, data update, and semaphore release.

Thread-Safe UI: Built using threading.Semaphore and thread-safe Tkinter callbacks to prevent race conditions during visualization.

Modern Aesthetics: Styled with a "Sleek Dark" theme using a custom color palette.

🛠️ Tech Stack
Language: Python 3.x

Library: Tkinter (GUI), Threading (Concurrency)

Synchronization: Semaphores (mutex and rw_mutex)

🧠 The Logic Behind the Simulation
The simulator implements the standard semaphore-based solution:

Readers:

Can read simultaneously.

The first reader locks the shared resource (rw_mutex).

The last reader to finish releases the resource.

Writers:

Require exclusive access.

Must wait for all readers and other writers to finish before starting.

Mutex: Ensures the read_count variable is updated safely by only one reader at a time.

🚦 Getting Started
Prerequisites
Python installed on your machine.

The tkinter library (standard with most Python installations).

Installation & Execution
Clone the repository:

Bash
git clone https://github.com/yourusername/readers-writers-simulator.git
Navigate to the folder:

Bash
cd readers-writers-simulator
Run the script:

Bash
python main.py
📸 Interface Guide
Central Circle: Represents the shared data (Critical Section).

Top Blocks (Green): Represent Reader threads.

Bottom Blocks (Red): Represent Writer threads.

Right Panel: Contains the "Shared Data" counter, live system status, and a scrollable activity log.

📄 License
This project is open-source and available under the MIT License.
