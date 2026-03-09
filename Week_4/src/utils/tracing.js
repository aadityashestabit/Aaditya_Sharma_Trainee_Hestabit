import { v4 as uuidv4 } from "uuid";

export const tracingMiddleware = (req, res, next) => {

  const requestId = req.headers["x-request-id"] || uuidv4();

  req.requestId = requestId;

  res.setHeader("X-Request-ID", requestId);

  next();
};