import "./src/config/index.js";
import express from "express";
import { config } from "./src/config/index.js";
import initApp from "./src/loaders/app.js"
import userRoutes from "./src/routes/user.routes.js"
import productRoutes from "./src/routes/product.routes.js"

const app = express();
app.use(express.json())
app.use("/",userRoutes)
app.use("/api/users",userRoutes)
app.use("/api/products",productRoutes)

initApp()

app.listen(config.port, () => {
  console.log(`Server running on port ${config.port}`);
});