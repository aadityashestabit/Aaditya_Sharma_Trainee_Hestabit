import express from "express";
import dotenv from "dotenv";
import { config } from "../config/index.js";
import logger from "../utils/logger.js";
import connectDB from "./db.js";
import userRoutes from "../routes/user.routes.js";
import emailRoutes from "../routes/email.routes.js";
import productRoutes from "../routes/product.routes.js";
import { errorHandler, notFound } from "../middlewares/error.middleware.js";
import { SecurityMiddleware } from "../middlewares/security.js";
import { tracingMiddleware } from "../utils/tracing.js";
import healthRoutes from "../routes/health.routes.js";

const env = config.nodeEnv || "local";

try {
  dotenv.config({
    path: `.env.${env}`,
  });
} catch (error) {
  console.error("Failed to load environment file:", error.message);
  process.exit(1);
}

export default async function initApp() {
  try {
    const app = express();
    app.use(express.json());

    SecurityMiddleware(app);

    app.use(tracingMiddleware);

    // Routes
    app.use("/api/users", userRoutes);
    app.use("/api/products", productRoutes);
    app.use("/api", emailRoutes);
    app.use("/", healthRoutes);

    logger.info({
      message:`Routes Mounted`
    })

    // 404 Handler
    app.use(notFound);
    logger.info({
      message:`Not found error handler loaded`
    })

    // Global Error Handle
    app.use(errorHandler);
    logger.info({
      message:`Global error handler loaded`
    })


    // Connect DB
    await connectDB();
    logger.info({
      message:`Database connected`
    })

    const server = app.listen(config.port, () => {
      logger.info({
        message: `Server started on port ${config.port}`,
      });

      logger.info({
        message: `Environment: ${config.nodeEnv}`,
      });
    });

    // Graceful shutdown
    process.on("SIGTERM", () => {
      logger.info("SIGTERM received. Shutting down...");
      server.close(() => process.exit(0));
    });

    return app;

  } catch (error) {
    logger.error({
      message: "Application initialization failed",
      error: error.message,
    });
    process.exit(1);
  }
}