const fs = require("fs");
const path = require("path");

// Check  logs exist 
const logDir = path.join(__dirname, "logs");
if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir);
}

// Capture metrics
const cpuUsage = process.cpuUsage();
const resourceUsage = process.resourceUsage();

const metrics = {
  timestamp: new Date().toISOString(),
  cpuUsage,
  resourceUsage
};

// Write to file
const logFile = path.join(logDir, "day1-sysmetrics.json");
fs.writeFileSync(logFile, JSON.stringify(metrics, null, 2));

console.log("System metrics logged to /logs/day1-sysmetrics.json");