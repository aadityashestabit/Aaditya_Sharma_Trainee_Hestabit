import express from "express"
import dotenv from "dotenv"
import {config} from "../config/index.js"
import logger from "../utils/logger.js"
import connectDB from "../loaders/db.js"

const env = config.nodeEnv || "local";
dotenv.config({
  path: `.env.${env}`,
});

export default async function initApp() {
  const app = express();

  app.use(express.json());

  await connectDB();

  const server = app.listen(config.port, () => {
    logger.info(`Server started on port ${config.port}`);
  });

  process.on("SIGTERM", () => {
    logger.info("SIGTERM received. Shutting down...");
    server.close(() => process.exit(0));
  });
}

