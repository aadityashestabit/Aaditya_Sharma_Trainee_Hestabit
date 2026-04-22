import { AppError } from "../utils/AppError.js";
import logger from "../utils/logger.js";

export const errorHandler = (err, req, res, next) => {
  let statusCode = err.statusCode || 500;
  let message = err.message || "Internal Server Error";
  let code = err.code || "INTERNAL_ERROR";

  // Joi Validation Error
  if (err.isJoi) {
    statusCode = 400;
    message = err.details.map((d) => d.message).join(", ");
    code = "REQUEST_VALIDATION_ERROR";
  }

  // Mongoose CastError (invalid ObjectId)
  else if (err.name === "CastError") {
    statusCode = 400;
    message = `Invalid ${err.path}: ${err.value}`;
    code = "INVALID_ID";
  }

  // Duplicate Key
  else if (err.code === 11000) {
    statusCode = 409;
    const field = Object.keys(err.keyValue)[0];
    message = `${field} already exists`;
    code = "DUPLICATE_KEY";
  }

  // Mongoose Validation
  else if (err.name === "ValidationError") {
    statusCode = 422;
    message = Object.values(err.errors).map((e) => e.message).join(", ");
    code = "VALIDATION_ERROR";
  }

  // JWT Errors
  else if (err.name === "JsonWebTokenError") {
    statusCode = 401;
    message = "Invalid token";
    code = "INVALID_TOKEN";
  }

  else if (err.name === "TokenExpiredError") {
    statusCode = 401;
    message = "Token has expired";
    code = "TOKEN_EXPIRED";
  }

  logger.error(`[${code}] ${message}`, { stack: err.stack });

  res.status(statusCode).json({
    success: false,
    message,
    code,
    statusCode,
    timestamp: new Date().toISOString(),
    path: req.originalUrl,
  });
};



// 404 handler — for routes that don't exist
export const notFound = (req, res, next) => {
  next(new AppError(`Route ${req.originalUrl} not found`, 404, "NOT_FOUND"));
};