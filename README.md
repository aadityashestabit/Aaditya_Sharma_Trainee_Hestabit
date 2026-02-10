
# Aaditya Sharma – Hestabit Trainee

## Week 1

Following are the task advancements for week 1 assigned tasks.

---

## Day 1 : System Reverse Engineering & Node.js Basics
### Tasks Performed

1. **System Health Script (`sysinfo.js`)**

2. **Performance Logging**

3. **Terminal Optimization**

### Deliverables

#### logs/day1-sysmetrics.json
![JSON Logs](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/logs.png)

---

#### `.bashrc` Alias Configuration
![Bashrc Aliases](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/bash-ss.png)

## Day 2 : Node CLI and Concurrency

### Tasks Performed

Built a CLI tool that :-\
    1. Count total number of **Lines**, **Characters**, **Words**.\
    2. Remove duplicate lines upon adding --unique flag.\
    3. Logs `cpuUsage` and `memoryUsageinMB` to `/logs`

--- 

### Deliverables

1. `stats.js` containing CLI logic.
2. `/logs` containing log report of CLI.
3. Output files containing unique lines.

---

## Day 3 : Git Mastery (RESET, REVERT, CHERRYPICK, STASH)

### Tasks Performed

1. Setup repository with 10 commits, explicitly introduced syntax error in commit 5.
2. Used git bisect to detect breaking commit using `git bisect bad` and `git bisect good`.
3. Created a release branch named `release/v0.1` using `git switch release/v0.1`.
4. Used **cherrypick** to bring important changes from `main` branch to `release/v0.1`.
5. Used **stash** to pick selected commits and switched branches from `main` to `release/v0.1` and commited in `main` branch.

#### Documentation

1. Bisect Command Logs 