import { Worker } from "bullmq";
import connection from "../config/redis.js";
import logger from "../utils/logger.js";

const worker = new Worker(
  "emailQueue",
  async (job) => {

    logger.info(`Processing email job ${job.id}`);

    const { to, subject, body } = job.data;

    console.log(`Sending email to ${to}`);

    await new Promise(r => setTimeout(r, 2000));

    return "Email sent";
  },
  { connection }
);

worker.on("completed", job => {
  logger.info(`Job completed ${job.id}`);
});

worker.on("failed", (job, err) => {
  logger.error(`Job failed ${job.id}`, err);
});