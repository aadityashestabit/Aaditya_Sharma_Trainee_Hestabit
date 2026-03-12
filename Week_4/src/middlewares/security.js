import express from "express";
import helmet from "helmet";
import cors from "cors";
import rateLimit from "express-rate-limit";
import hpp from "hpp";
// import { xss } from "express-xss-sanitizer";

export const SecurityMiddleware = (app) => {
  try {

    // Security headers
    app.use(helmet());

    // CORS
    app.use(cors({
      origin: ["http://localhost:3000"],
      methods: ["GET", "POST", "PUT", "PATCH", "DELETE"],
      credentials: true
    }));

    // Rate limiting
    const limiter = rateLimit({
      windowMs: 15 * 60 * 1000,
      max: 100,
      standardHeaders: true,
      legacyHeaders: false
    });

    app.use("/api", limiter);

    // Prevent parameter pollution
    app.use(hpp());

    // Payload size limit
    app.use(express.json({ limit: "10kb" }));

  } catch (error) {
    console.error("Security middleware initialization failed:");
    console.error(error.message);
    throw error;
  }
};