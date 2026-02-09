const http = require("http");

const server = http.createServer((req, res) => {
  if (req.url === "/ping") {
    // introduce bug intentionally on random ping
    const shouldFail = Math.random() < 0.5;

    if (shouldFail) {
      res.writeHead(500, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "Service unhealthy" }));
      return;
    }

    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ timeStamp: Date.now() }));
    return;
  }

  res.writeHead(404);
  res.end("Not found");
});

server.listen(3000, () => {
  console.log("Server running on port 3000");
});
