const { parentPort, workerData } = require("worker_threads");
const fs = require("fs/promises");
const path = require("path");

function getExecutionTime(start) {
  const end = process.hrtime.bigint();
  return Number(end - start) / 1_000_000;
}

function getMemoryMB() {
  return process.memoryUsage().heapUsed / 1024 / 1024;
}

function countLines(data) {
  return data.split("\n").length;
}

function countWords(data) {
  return data.trim().split(/\s+/).length;
}

function countChars(data) {
  return data.length;
}

(async () => {
  const start = process.hrtime.bigint();
  const { filePath, flag, unique } = workerData;

  const data = await fs.readFile(filePath, "utf-8");

  let result;
  if (flag === "--lines") result = countLines(data);
  if (flag === "--words") result = countWords(data);
  if (flag === "--chars") result = countChars(data);

  // Unique lines logic
  if (unique) {
    const uniqueLines = [...new Set(data.split("\n"))];
    const outPath = path.join("output", `unique-${path.basename(filePath)}`);
    await fs.writeFile(outPath, uniqueLines.join("\n"));
  }

  parentPort.postMessage({
    file: path.basename(filePath),
    result,
    executionTimeMs: Number(getExecutionTime(start).toFixed(2)),
    memoryMB: Number(getMemoryMB().toFixed(2)),
  });
})();
