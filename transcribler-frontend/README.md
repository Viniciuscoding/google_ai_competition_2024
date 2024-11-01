# Transcribler Frontend Client Setup
To get started in our frontend environment, please install the following:
- [Node.js (LTS)](https://nodejs.org/en)
  - Compatible with any OS (Windows, Mac, Linux)
- [Visual Studio Code](https://code.visualstudio.com/)
  - Our preferred IDE, but you can use another if you are more familiar/comfortable
- [Github Desktop](https://desktop.github.com/download/)
  - Our preferred version control software, but you can use CLI if you are more familiar/comfortable

## Steps
1. Install the above programs
    - To verify you have Node.js properly installed, open your terminal and perform the command `node --version`, which should return your current running version of Node.
2. Clone this repository and switch to the `react-frontend` branch
    - With CLI: `git clone https://github.com/Viniciuscoding/google_ai_competition_2024.git`
    - On GitHub Desktop: Add > Clone a repository > URL > https://github.com/Viniciuscoding/google_ai_competition_2024.git > Clone
3. Open the repository in Visual Studio Code
4. Open your terminal, and perform the following commands:
    - `cd transcribler`: This changes to our frontend's directory
    - `npm i`: This updates and installs all the Node packages to your local machine
    - `npm run dev`: This starts an instance of our Vite frontend environment on your local machine
5. You can now view our frontend on `http://localhost:5173/`. To view changes in real-time after editing, simply save `Ctrl + S` your code. 



# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh
