import express from "express";
import dotenv from "dotenv";
import { config } from "../config/index.js";
import logger from "../utils/logger.js";
import connectDB from "../loaders/db.js";
import userRoutes from "../routes/user.routes.js";
import productRoutes from "../routes/product.routes.js";
import { errorHandler, notFound } from "../middlewares/error.middleware.js";

const env = config.nodeEnv || "local";
dotenv.config({
  path: `.env.${env}`,
});

export default async function initApp() {
  const app = express();

  app.use(express.json());

  
  app.use("/", userRoutes);
  app.use("/api/users", userRoutes);
  app.use("/api/products", productRoutes);
  
  
  app.use(notFound);
  
  // Global error handler — must be LAST, has 4 params
  app.use(errorHandler);
 
 
  // Connect DB
  await connectDB();


  const server = app.listen(config.port, () => {
    logger.info(`Server started on port ${config.port}`);
    logger.info(`Environment: ${config.nodeEnv}`)
  });

  process.on("SIGTERM", () => {
    logger.info("SIGTERM received. Shutting down...");
    server.close(() => process.exit(0));
  });

  return app
}
