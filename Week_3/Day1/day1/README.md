# Week 3 - NEXTJS and TAILWINDCSS 

## Day1 (Create next app)

1. Installed next js in my local system using `npm create-next-app@latest`.
2. Initialized next js in javascript with tailwind and ESlint.
3. Understood folder structure of next js.

### New learnings
* Next js routing is done through folders - folder name become route name example `/Dashboard/page.js` become `https://xyz.com/dashboard`.
* For nested routing, nested directories are used `/Product/Reviews` becomes `https://xyz.com/products/reviews`.
* Got introduced with client components and server components.
* Image and Text optimization with `Image`, `Link` tags.
* Server side rendering(SSR).
* Static Site Generation(SSG).

## Tasks Performed

Made Side bar of the given reference figma design :- `https://www.figma.com/proto/JdoKvxwRE44a4h3bnpu3ZX/Purity-UI-Dashboard---Chakra-UI-Dashboard--Community-?node-id=29-2&t=bm1QziJKazGeZkad-0&scaling=min-zoom&content-scaling=fixed&page-id=0%3A1`

### Components made

1. **Side bar item**

![Side Bar Item](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/SidebarItem.png)

This component is used by the side bar component with the following parameters - `label`, `href`, `active`, `icon`.

2. **Side bar help**

![Side bar help](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/SidebarHelp.png)

This component is used by Sidebar component for displaying documentation.

3. **Side Bar**

![Side Bar](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Sidebar.png)

This is the main sidebar for the project which is modular and can be reused in the layout.js for repeated use in the webpages.

4. **Navbar**

![Navbar](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Navbar.png)

This is the nav bar component. This component is singular and not made with multiple components because of the project ui design.

It shows project routing structure along with a search bar, signin, settings and notification icon.

---

## Day 2 (Component modularity)

### Tasks Performed

#### Components made

**Stat Card**
![Stat Card](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Statcard.png)

**Promo Banner**
![Promo Banner](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Promobanner.png)

**Rocket Component**
![Rocket Component](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Rocket.png)

**Active Users Cards**
![Active Users](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Activeuserscard.png)

**Sales Overview Card**
![Sales Overview](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Salesoverview.png)

**Projects Card**
![Projects Card](https://github.com/aadityashestabit/Aaditya_Sharma_Trainee_Hestabit/blob/main/images/Projects.png)