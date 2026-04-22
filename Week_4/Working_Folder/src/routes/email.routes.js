import express from "express";
import { addEmailJob } from "../jobs/email.job.js";
import logger from "../utils/logger.js";

const router = express.Router();

router.post("/send-email", async (req, res) => {

  const { to, subject, body } = req.body;

  await addEmailJob({ to, subject, body });

  res.json({
    message: "Email job added to queue"
  });

  logger.info({
    message: "Incoming request",
    method: req.method,
    path: req.originalUrl,
    requestId: req.requestId
  });
});

export default router;