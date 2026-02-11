const os = require("os");
const { execSync } = require("child_process");

// host name

const hostname = os.hostname();

// disk space

function getDiskSpace() {
  try {
    const commandOutput = execSync("df -k /").toString(); // we can use 3 flags for disk space -k , -h , -B1G but -k is most suitable

    const lines = commandOutput.split("\n");
    // line 0 - headers, line 1 - actual data
    const diskInfo = lines[1].split(/\s+/);
    const availableSpaceKB = parseInt(diskInfo[3], 10);
    const availableSpaceGB = availableSpaceKB / (1024 * 1024);

    //       console.log("Lines", lines);
    //       Lines [
    //   'Filesystem     1K-blocks     Used Available Use% Mounted on',
    //   '/dev/nvme0n1p2 490048472 20898180 444183688   5% /',
    //   ''
    // ]

    // console.log("Disk Info", diskInfo);
    // Disk Info [ '/dev/nvme0n1p2', '490048472', '20898180', '444183688', '5%', '/' ]

    return availableSpaceGB.toFixed(2) + "GB";
  } catch (error) {
    return "Error in finding Disk Space";
  }
}

// get open ports

function getOpenPorts() {
  try {
    const ports = execSync(
      "ss -tuln | awk 'NR>1 {print $5}' | cut -d: -f2 | sort | uniq | head -6",
    )
      .toString()
      .trim();
    if (ports) {
      return ports;
    } else {
      return "No open ports";
    }
  } catch (error) {
    return "Ports error";
  }
}

// get default gateway

function getDefaultGateway() {
  try {
    const gateway = execSync("ip route | grep default | awk '{print $3}'")
      .toString()
      .trim();
    return gateway;
  } catch (error) {
    return "Default Gateway error";
  }
}

function getLoggedInUserCount() {
  try {
    const users = execSync("who | wc -l").toString().trim();

    return users;
  } catch (error) {
    return "Logged in user count error";
  }
}

console.log("Hostname:", hostname);
console.log("Available Disk Space:", getDiskSpace());
console.log("Open Ports (Top 5):", getOpenPorts());
console.log("Default Gateway:", getDefaultGateway());
console.log("Logged-in Users Count:", getLoggedInUserCount());

//----------------Output-------------------------------->
// Disk Info [ '/dev/nvme0n1p2', '490048472', '20898180', '444183688', '5%', '/' ]
// Available Disk Space: 423.61GB
// Open Ports (Top 5): 27017
// 3306
// 33060
// 43574
// 53
// Default Gateway: 10.10.0.1
// Logged-in Users Count: 2
