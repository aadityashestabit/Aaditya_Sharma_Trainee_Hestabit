import { Redis } from "ioredis";

let connection;

try {
  connection = new Redis({
    host: "127.0.0.1",
    port: 6379,
    maxRetriesPerRequest: null,
  });
} catch (error) {
  console.error("Redis connection initialization failed:");
  console.error(error.message);
  process.exit(1);
}

export default connection;
