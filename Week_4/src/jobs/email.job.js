import { Queue } from "bullmq";
import connection from "../config/redis.js";

export const emailQueue = new Queue("emailQueue", {
  connection
});

export const addEmailJob = async (data) => {

  await emailQueue.add(
    "sendEmail",
    data,
    {
      attempts: 3,
      backoff: {
        type: "exponential",
        delay: 2000
      },
      removeOnComplete:true, // remove job if the job get seccesfully executed 
      removeOnFail:false
    }
  );
};