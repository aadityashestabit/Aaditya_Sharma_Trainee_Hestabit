import winston from "winston";
import fs from "fs";
import path from "path";

const { combine, timestamp, printf, errors } = winston.format;


const logDir = path.join(process.cwd(), "src", "logs");

if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir, { recursive: true });
}

// Log format - 2026-02-24 16:40:25 [INFO]: Server started on port 3000
const logFormat = printf(({ level, message, timestamp, stack, }) => {
  return `${timestamp} [${level.toUpperCase()}]: ${
    stack || message
  }}`;
});

const logger = winston.createLogger({
  level: "info",
  format: combine(timestamp({ format: "YYYY-MM-DD HH:mm:ss" }),errors({ stack: true }), logFormat ),
  transports: [
    new winston.transports.Console(),

    new winston.transports.File({
      filename: path.join(logDir, "combined.log"),
    }),

    new winston.transports.File({
      filename: path.join(logDir, "error.log"),
      level: "error",
    }),
  ],
});

if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.simple(),
  }));
}

export default logger;