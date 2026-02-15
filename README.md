
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

## Tasks Performed

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

## Tasks Performed

1. Setup repository with 10 commits, explicitly introduced syntax error in commit 5.
2. Used git bisect to detect breaking commit using `git bisect bad` and `git bisect good`.
3. Created a release branch named `release/v0.1` using `git switch release/v0.1`.
4. Used **cherrypick** to bring important changes from `main` branch to `release/v0.1`.
5. Used **stash** to pick selected commits and switched branches from `main` to `release/v0.1` and commited in `main` branch.

### Documentation

1. **Bisect Command Logs**\
![Bisect logs](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/bisect_logs.png)
2. **Cherry-pick Result**
Cherry pick result is documented in `cherry-pich-report.md`.
3. Stash Scenario
    * Created stash on `main` branch and switched branches, did some commit in `release/v0.1` then switched branch to `main` and ran `git stash pop` to apply and drop stash.

---
### Deliverables

1. bisect-log.txt
2. cherry-pick-report.md
3. stash-proof.txt

---

## Day 4 - HTTP / API Forensics (cURL + POSTMAN)

## Tasks Performed

1. Used cURL to fetch Github API by -
`curl -v https://api.github.com/users/octocat`
2. Extracted and logged (in curl-header.txt)
    * Rate Limit Remaining
    * ETag
    * Server Header
3. Pagination Fetch - fetched `https://api.github.com/users/octocat/repos?page=1&per_page=5` from cURL and documented analysis in `pagination-analysis.md`.
4. Created **POSTMAN** collection testing
    * GET - Github User
    * GET - repos with 3 pages.
5. Built HTTP Server with -
    * /ping request
    * /headers - return request headers
    * /count - maintain server hit counter in memory

---
### Deliverables

1. curl-headers.txt
2. pagination-analysis.md
3. POSTMAN exported collection.json
4. server.js

---

## Day 5 - Automation and MINI-CI Pipeline

### Tasks Performed

1. Built script `healthcheck.sh` to ping the server every **10 seconds** and log failures to `/logs/health.log`.
2. Pre-Commit validation using husky, ensured :-
    * .env does not exist in git
    * Ensure JS is formatted
    * Ensure log files are ignored
3. Made `checksum.sha1` to hash `healthcheck.sh` and store its 40 character long hash.
4. Bundled :-
    * src/
    * logs/
    * docs/
    * checksum.sha1 in `bundle-20260206-191233.zip`
5. Built a cron job to run `healthcheck.sh` every 5 mins using `*/5 * * * * /Desktop/Aaditya_Sharma_Trainee_Hestabit/Week_1/Day5/scripts/healthcheck.sh`

---

### Deliverables\

1. healthcheck.sh file
2. Husky pre-commit hook screenshot
3. bundle-20260206-191233.zip
4. checksums.sha1
5. Screenshot of scheduled cron job

---

### Attachments

![Husky pre-commit screenshot](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/husky-pre-commit.png)

![Cron Job](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/cron-job.png)

#### Husky Failed

![Husky Fail](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/husky-precommit.png)
---

## Week 2 - Frontend Fundamentals

## Day 1 (HTML5 + Semantics)

### Tasks Performed
1. Built a blog page webite using only semantic HTML tags and no use of css and javascript
2. Used the following HTML tags
    * `<header>`
    * `<footer>`
    * `<nav>`
    * `<main>`
    * `<section>`
    * `<article>`
---

### Attachments 

![HTML Page](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/HTML_Blog_Page.png)
---

## Day 2 (CSS Layout Mastery)

### Tasks Performed

1. Made a modern responsive layout using grid and flexbox.
2. Made a modern layout with sidebar and seperate sections for header hooter and main content 
---

### Attachments

![CSS Layout](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/CSS_Layout.png)

---

## Day 3 (Javascript ES6 + DOM Manipulation)

### Tasks Performed

1. Built an interactive faq section using `html`, `css` and `javascript`.
2. Faq contained dropdown for the selected layer of the faq section.
---

### Attachments

![FAQ Accordition](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/FAQ.png)

---

## Day 4 (JS Utilities + LocalStorage MINI-PROJECT)

### Tasks Performed

1. Made a To Do List with local Storage support.
2. To Do list support following operations
    * Add
    * Delete
    * Edit
    * Persist after delete
3. Through local storage the todo list items persist in the same stage as left before refresh.
4. Error handling using try catch.

---

### Attachments

![Todo App](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Todo%20List.png)

---

## Day 5 (Capstone UI + JS Project)

### Tasks Performed

1. Capstone project with `html`, `css`, `javascript`.
2. Built a **product listing page** which fetch product details from api and return the details of the product which are then listed on the page.
3. Product API - `https://dummyjson.com/products`.
4. Search functionality is also added to render products on search.
5. Sorting functionality is also added to sort prices from high -> low.

---

### Attachments

![Capstone Product home](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Product_Webpage.png)

![Capstone Product Listing Page](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Product_Webpage_Listing.png)

---