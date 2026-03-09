import express from "express";
import { addEmailJob } from "../jobs/email.job.js";

const router = express.Router();

router.post("/send-email", async (req, res) => {

  const { to, subject, body } = req.body;

  await addEmailJob({ to, subject, body });

  res.json({
    message: "Email job added to queue"
  });
});

export default router;