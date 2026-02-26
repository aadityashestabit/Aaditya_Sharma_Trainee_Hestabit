import "./src/config/index.js";
import initApp from "./src/loaders/app.js";

initApp().catch((err) => {
  console.error("Failed to start server:", err);
  process.exit(1);
});