
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

# Week 3 - NEXTJS and TAILWINDCSS

## Create Next App

### Tasks Performed

1. Installed Next.js in my local system using `npm create-next-app@latest`.
2. Initialized Next.js in JavaScript with Tailwind CSS and ESLint.
3. Understood the folder structure of Next.js.

---

### New Learnings

- Next.js routing is done through folders — folder name becomes route name.  
  Example: `/Dashboard/page.js` becomes `https://xyz.com/dashboard`.

- For nested routing, nested directories are used.  
  Example: `/Product/Reviews` becomes `https://xyz.com/products/reviews`.

- Got introduced to:
  - Client Components
  - Server Components

- Learned about:
  - Image and Text Optimization using `Image` and `Link` components.
  - Server Side Rendering (SSR)
  - Static Site Generation (SSG)

---

## UI Implementation

Recreated the Sidebar from the reference Figma design.

---

# Components Made

---

## Side Bar Item

|**Side Bar Item**|
| ----------- |
| ![Side Bar Item](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/SidebarItem.png)|

This component is used inside the Sidebar component.  
It accepts the following props:

- `label`
- `href`
- `active`
- `icon`

---

## Side Bar Help

|**Side Bar Help**|
| ----------- |
| ![Side Bar Help](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/SidebarHelp.png)|

This component is used inside the Sidebar component for displaying documentation/help information.

---

## Side Bar

|**Side Bar**|
| ----------- |
| ![Side Bar](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Sidebar.png)|

This is the main Sidebar component of the project.

- Modular
- Reusable
- Used inside `layout.js` to maintain consistent layout across pages

---

## Navbar

|**Navbar**|
| ----------- |
| ![Navbar](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Navbar.png)|

This is the Navbar component.

It includes:

- Project routing structure display
- Search bar
- Sign-in button
- Settings icon
- Notification icon

This component was designed as a single structured component based on the UI requirement.

---

## Component Modularity

Focused on creating reusable UI cards and dashboard elements.

---

## Stat Card

|**Stat Card**|
| ----------- |
| ![Stat Card](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Statcard.png)|

This component represents a dashboard statistics card.

It is reusable and accepts dynamic values such as:
- Title
- Value
- Percentage change
- Icon

---

## Promo Banner

|**Promo Banner**|
| ----------- |
| ![Promo Banner](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Promobanner.png)|

This component is used to display promotional or highlighted information on the dashboard.

---

## Rocket Component

|**Rocket Component**|
| ----------- |
| ![Rocket Component](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Rocket.png)|

This component visually represents performance growth or progress.

---

## Active Users Card

|**Active Users Card**|
| ----------- |
| ![Active Users Card](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Activeuserscard.png)|

Displays user activity metrics in a structured dashboard card format.

---

## Sales Overview Card

|**Sales Overview Card**|
| ----------- |
| ![Sales Overview Card](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Salesoverview.png)|

This component displays graphical sales performance and insights.

---

## Projects Card

|**Projects Card**|
| ----------- |
| ![Projects Card](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Dashboard_project.png)|

This component shows project tracking information in a clean card layout.

---


## Next Js Routing and Layout System

Learned App based routing in next js and layout system along with nested layouts.

---
|**Profile Header**|
|------------------|
|![Profile Header](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Profile_header.png)|

This profile header is used in the profile page to show userprofile details

---

---

|**Profile Information**|
|-----------------------|
|![Profile Information](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Profile_information.png)|

---

---
|**Profile Settings**|
|--------------------|
|![Profile Settings](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Profile_settings.png)|
---

---
|**Conversations**|
|-----------------|
|![ Conversations](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Conversations.png)|
---

## Final Pages

These are the final pages made during Week3 with nextjs and tailwindcss

---
|**Dashboard (page 1)**|
|-----------------|
|![Dashboard page 1](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Dashboard_page_1.png)|
---

---
|**Dashboard (page 2)**|
|-----------------|
|![Dashboard page 2](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Dashboard_page_2.png)|
---

---
|**Tables (page 1)**|
|-----------------|
|![Tables page 1](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Tables_page_1.png)|
---

---
|**Tables (page 2)**|
|-----------------|
|![Tables Page 2](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Tables_page_2.png)|
---

---
|**Profile Page**|
|-----------------|
|![Profile Page](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Profile_page.png)|
---

---
|**SignIn Page**|
|-----------------|
|![SignIn Page](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Sign_in_page.png)|
---

---
|**SignUp Page**|
|-----------------|
|![SignUp Page](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Sign_up_page.png)|
---

## Final Project Project Structure

```
.
└── Next-js-tailwindcss-project/
    ├── .next
    ├── components/
    │   ├── auth/
    │   │   ├── AuthFooter.jsx
    │   │   ├── AuthNavbar.jsx
    │   │   ├── AuthRightPanel.jsx
    │   │   └── LoginForm.jsx
    │   ├── dashboard/
    │   │   ├── ActiveUsersCard.jsx
    │   │   ├── ActiveUsersChart.jsx
    │   │   ├── Promobanner.jsx
    │   │   ├── RocketCard.jsx
    │   │   ├── SalesOverviewChart.jsx
    │   │   └── Statcard.jsx
    │   ├── profile/
    │   │   ├── Conversation.jsx
    │   │   ├── ConversationTile.jsx
    │   │   ├── PlatformSettings.jsx
    │   │   ├── ProfileAvatar.jsx
    │   │   ├── ProfileHeader.jsx
    │   │   ├── ProfileInformation.jsx
    │   │   ├── ProfileNavbar.jsx
    │   │   ├── ProfileTabs.jsx
    │   │   └── SettingSection.jsx
    │   ├── signup/
    │   │   └── RegisterCard.jsx
    │   ├── ui/
    │   │   ├── AuthorRow.jsx
    │   │   ├── AuthorsTable.jsx
    │   │   ├── Footer.jsx
    │   │   ├── Navbar.jsx
    │   │   ├── ProjectsTable.jsx
    │   │   ├── Sidebar.jsx
    │   │   ├── Sidebarhelp.jsx
    │   │   ├── SidebarItem.jsx
    │   │   └── ToggleSwitch.jsx
    │   └── ui
    ├── node_modules
    ├── public
    ├── src/
    │   └── app/
    │       ├── dashboard/
    │       │   ├── page.jsx
    │       │   └── layout.jsx
    │       ├── profile/
    │       │   ├── page.jsx
    │       │   └── layout.jsx
    │       ├── sign-in/
    │       │   ├── page.jsx
    │       │   └── layout.jsx
    │       ├── sign-up/
    │       │   ├── page.jsx
    │       │   └── layout.jsx
    │       ├── tables/
    │       │   ├── page.jsx
    │       │   └── layout.jsx
    │       ├── globals.css
    │       ├── layout.js
    │       └── page.js
    ├── .gitignore
    ├── eslint.config.mjs
    ├── jsconfig.json
    ├── next.config.mjs
    ├── package-lock.json
    ├── package.json
    ├── postcss.config.mjs
    └── README.md
```

---

## Project Link

https://aaditya-sharma-trainee-hestabit.vercel.app/

# Summary

During Week 3:

- Learned core concepts of Next.js routing and rendering.
- Understood SSR and SSG.
- Built modular and reusable components using Tailwind CSS.
- Followed structured UI design implementation.
- Improved component reusability and layout architecture.

---

# Week 4 - BACKEND SYSTEMS & PRODUCTION ENGINEERING

## Week 4 - Folder Structure

```
.
├── node_modules
├── src
│   ├── config
│   │   ├── index.js
│   │   └── redis.js
│   ├── controllers
│   │   ├── product.controller.js
│   │   └── user.controller.js
│   ├── jobs
│   │   └── emai.job.js
│   ├── loaders
│   │   ├── app.js
│   │   └── db.js
│   ├── logs
│   │   ├── combined.log
│   │   └── error.log
│   ├── middlewares
│   │   ├── auth.middleware.js
│   │   ├── error.middleware.js
│   │   ├── role.middleware.js
│   │   ├── security.js
│   │   └── validate.js
│   ├── models
│   │   ├── product.model.js
│   │   └── user.model.js
│   ├── repositories
│   │   ├── product.repository.js
│   │   └── user.repository.js
│   ├── routes
│   │   ├── email.routes.js
│   │   ├── product.routes.js
│   │   └── user.routes.js
│   ├── seeders
│   │   ├── product.seeder.js
│   │   └── user.seeder.js
│   ├── services
│   │   ├── product.service.js
│   │   └── user.service.js
│   ├── utils
│   │   ├── AppError.js
│   │   ├── cursor.js
│   │   ├── logger.js
│   │   └── tracing.js
│   ├── validators
│   │   ├── product.schema.js
│   │   └── user.schema.js
│   └── workers
│       └── email.worker.js
├── .env.dev
├── .env.local
├── .env.prod
├── .gitignore
├── NodeJs-Backend.postman_collection.json
├── package-lock.json
├── package.json
└── server.js
```
