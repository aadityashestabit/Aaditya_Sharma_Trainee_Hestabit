
# Aaditya Sharma – Hestabit Trainee

## Week 1

This repository documents my daily tasks, learnings, and engineering experiments during my internship at **Hestabit**.

---

## 🟦 Day 1: System Reverse Engineering & Node.js Basics

### 🎯 Goal
To understand how a high-level language like **Node.js** interacts with the **Linux Operating System** to fetch low-level hardware and network information.

---

### 🛠️ Tasks Performed

1. **System Health Script (`sysinfo.js`)**
   - Built a Node.js utility using `child_process` and `os` modules.
   - Retrieved:
     - Hostname  
     - Available Disk Space  
     - Open Ports  
     - Default Gateway  
     - Logged-in Users  

2. **Performance Logging**
   - Integrated `process.cpuUsage()` and `process.resourceUsage()` to monitor script efficiency.
   - Stored outputs in **JSON format** under the `/logs` directory.

3. **Terminal Optimization**
   - Configured custom shell aliases in `.bashrc` to speed up common workflows:
     - `gs` → `git status`
     - `files` → `ls -lha`
     - `ports` → Show listening network ports

---

### 🧠 Key Learnings (The “Why”)

- **Observability**: System-level metrics are essential for monitoring server health.
- **Automation**: Scripts can replace repetitive manual terminal commands.
- **Data Serialization**: JSON is an efficient and standard format for structured logging.

---

### 📸 Proof of Work (Deliverables)

#### Script (`sysinfo.js`) and Terminal Output
![System Info Script Output](https://github.com/user-attachments/assets/01583611-8a09-4751-810a-75bfca3c38f2)

![Terminal Execution](https://github.com/user-attachments/assets/e7c42193-55b8-4dc4-b84e-a144f3aba42b)

---

#### logs/day1-sysmetrics.json
![JSON Logs](https://github.com/user-attachments/assets/049ab64c-10ab-4d76-8eb7-ea9ea897b6f0)

---

#### `.bashrc` Alias Configuration
![Bashrc Aliases](https://github.com/user-attachments/assets/3151ee86-3e6b-4742-a95d-95f6ad6eeda0)

---

### 📌 Summary
Day 1 focused on bridging the gap between **high-level scripting** and **low-level system behavior**, building a strong foundation in system observability, automation, and performance awareness.
