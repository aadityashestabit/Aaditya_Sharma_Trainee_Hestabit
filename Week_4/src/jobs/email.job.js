import { Queue } from "bullmq";
import connection from "../config/redis.js";

export const emailQueue = new Queue("emailQueue", { // created queue named email queue 
  connection
});

export const addEmailJob = async (data) => {

  await emailQueue.add( // adding jobs to queue 
    "sendEmail",
    data,
    {
      attempts: 3,
      backoff: {
        type: "exponential",
        delay: 2000
      },
      removeOnComplete:1000, // remove job if the job get seccesfully executed 1000 times
      removeOnFail:1000
    }
  );
};