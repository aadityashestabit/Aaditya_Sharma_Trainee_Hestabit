# Week 3 - NEXTJS and TAILWINDCSS

## Day 1 (Create Next App)

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

## 1️⃣ Side Bar Item

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

## 2️⃣ Side Bar Help

|**Side Bar Help**|
| ----------- |
| ![Side Bar Help](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/SidebarHelp.png)|

This component is used inside the Sidebar component for displaying documentation/help information.

---

## 3️⃣ Side Bar

|**Side Bar**|
| ----------- |
| ![Side Bar](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Sidebar.png)|

This is the main Sidebar component of the project.

- Modular
- Reusable
- Used inside `layout.js` to maintain consistent layout across pages

---

## 4️⃣ Navbar

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

# Day 2 (Component Modularity)

Focused on creating reusable UI cards and dashboard elements.

---

## 1️⃣ Stat Card

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

## 2️⃣ Promo Banner

|**Promo Banner**|
| ----------- |
| ![Promo Banner](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Promobanner.png)|

This component is used to display promotional or highlighted information on the dashboard.

---

## 3️⃣ Rocket Component

|**Rocket Component**|
| ----------- |
| ![Rocket Component](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Rocket.png)|

This component visually represents performance growth or progress.

---

## 4️⃣ Active Users Card

|**Active Users Card**|
| ----------- |
| ![Active Users Card](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Activeuserscard.png)|

Displays user activity metrics in a structured dashboard card format.

---

## 5️⃣ Sales Overview Card

|**Sales Overview Card**|
| ----------- |
| ![Sales Overview Card](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Salesoverview.png)|

This component displays graphical sales performance and insights.

---

## 6️⃣ Projects Card

|**Projects Card**|
| ----------- |
| ![Projects Card](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Projects.png)|

This component shows project tracking information in a clean card layout.

---

# Summary

During Week 3:

- Learned core concepts of Next.js routing and rendering.
- Understood SSR and SSG.
- Built modular and reusable components using Tailwind CSS.
- Followed structured UI design implementation.
- Improved component reusability and layout architecture.

---
