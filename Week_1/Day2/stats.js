const fs = require("fs/promises");
const path = require("path");

// Metrics
function getExecutionTime(start) {
  const end = process.hrtime.bigint();
  return Number(end - start) / 1_000_000; // ms
}

function getMemoryMB() {
  return process.memoryUsage().heapUsed / 1024 / 1024;
}

// Count functions
function countLines(data) {
  return data.split("\n").length;
}

function countWords(data) {
  return data.trim().split(/\s+/).length;
}

function countChars(data) {
  return data.length;
} // stats.js
const { Worker } = require("worker_threads");
const fs = require("fs/promises");
const path = require("path");

async function main() {
  const args = process.argv.slice(2);
  const unique = args.includes("--unique");

  const tasks = [];

  for (let i = 0; i < args.length; i++) {
    const flag = args[i];
    const file = args[i + 1];

    if (
      (flag === "--lines" || flag === "--words" || flag === "--chars") &&
      file
    ) {
      tasks.push({ flag, file });
      i++;
    }
  }

  // Spawn worker threads
  const workerPromises = tasks.map(
    (task) =>
      new Promise((resolve, reject) => {
        const worker = new Worker("./worker.js", {
          workerData: {
            filePath: task.file,
            flag: task.flag,
            unique,
          },
        });

        worker.on("message", resolve);
        worker.on("error", reject);
        worker.on("exit", (code) => {
          if (code !== 0) reject(new Error(`Worker stopped with ${code}`));
        });
      }),
  );

  const results = await Promise.allSettled(workerPromises);

  await fs.mkdir("logs", { recursive: true });
  await fs.mkdir("output", { recursive: true });

  const logFile = `logs/performance-${Date.now()}.json`;
  await fs.writeFile(logFile, JSON.stringify(results, null, 2));

  console.log("\nResults:");
  console.log(results);

  console.log("\nPerformance log written to:", logFile);
}

main().catch(console.error);
