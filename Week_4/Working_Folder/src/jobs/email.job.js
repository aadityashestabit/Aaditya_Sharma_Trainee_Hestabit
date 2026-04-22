import { Queue } from "bullmq";
import connection from "../config/redis.js";

let emailQueue;

try {
  emailQueue = new Queue("emailQueue", { // created queue named email queue
    connection
  });
} catch (error) {
  console.error("Queue initialization failed:");
  console.error(error.message);
  process.exit(1);
}

export const addEmailJob = async (data) => {
  try {
    await emailQueue.add( // adding jobs to queue
      "sendEmail",
      data,
      {
        attempts: 3,
        backoff: {
          type: "exponential",
          delay: 2000
        },
        removeOnComplete: 1000, // remove job if the job get successfully executed 1000 times
        removeOnFail: 1000
      }
    );
  } catch (error) {
    console.error("Failed to add email job:");
    console.error(error.message);
    throw error;
  }
};

export { emailQueue };