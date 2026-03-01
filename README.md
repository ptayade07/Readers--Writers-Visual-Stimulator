# 🧵 Readers–Writers Synchronization Visual Simulator

An interactive Operating Systems project that demonstrates the classic **Readers–Writers synchronization problem** using Python threading and semaphores, with a real-time GUI visualization built using Tkinter.

This simulator visually represents concurrent reader and writer threads accessing shared data while maintaining proper synchronization and mutual exclusion.

---

## 📌 Project Overview

The Readers–Writers problem is a classic concurrency challenge in Operating Systems that deals with synchronizing access to a shared resource.

This project simulates:

- Multiple reader threads
- Multiple writer threads
- Shared data access
- Semaphore-based synchronization
- Real-time activity logging
- GUI-based visualization of concurrent execution

---

## 🎯 Objectives

- Demonstrate mutual exclusion using semaphores
- Prevent race conditions
- Allow multiple readers to read simultaneously
- Ensure writers get exclusive access
- Safely update GUI from background threads

---

## 🛠️ Built With

- Python 3.x
- Tkinter (GUI Framework)
- Python `threading` module
- Semaphore-based synchronization

No external libraries required.

---

## ⚙️ How It Works

The implementation uses two semaphores:

- `mutex` → Protects access to `read_count`
- `rw_mutex` → Controls access to shared data

### Synchronization Logic

- Multiple readers can read at the same time.
- Writers require exclusive access.
- The first reader locks writers out.
- The last reader releases writer access.
- Writers block both readers and other writers while writing.

Thread-safe UI updates are handled using:

```python
root.after()
