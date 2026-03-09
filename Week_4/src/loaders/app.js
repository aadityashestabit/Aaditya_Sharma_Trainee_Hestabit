import express from "express";
import dotenv from "dotenv";
import { config } from "../config/index.js";
import logger from "../utils/logger.js";
import connectDB from "../loaders/db.js";
import userRoutes from "../routes/user.routes.js";
import emailRoutes from "../routes/email.routes.js";
import productRoutes from "../routes/product.routes.js";
import { errorHandler, notFound } from "../middlewares/error.middleware.js";
import { SecurityMiddleware } from "../middlewares/security.js";
import { tracingMiddleware } from "../utils/tracing.js";

const env = config.nodeEnv || "local";

dotenv.config({
  path: `.env.${env}`,
});

export default async function initApp() {
  const app = express();
  app.use(express.json());

  SecurityMiddleware(app);

  app.use(tracingMiddleware)



  // Routes
  app.use("/api/users", userRoutes);
  app.use("/api/products", productRoutes);
  app.use("/api", emailRoutes)

  // 404 Handler
  app.use(notFound);

  // Global Error Handle
  app.use(errorHandler);

  // Connect DB 
  await connectDB();

  const server = app.listen(config.port, () => {
    logger.info(`Server started on port ${config.port}`);
    logger.info(`Environment: ${config.nodeEnv}`);
  });

  // Graceful shutdown
  process.on("SIGTERM", () => {
    logger.info("SIGTERM received. Shutting down...");
    server.close(() => process.exit(0));
  });

  return app;
}