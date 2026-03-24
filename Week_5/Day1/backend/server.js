import express from "express";

const app = express();

app.get("/", (req, res) => {
  res.send("Hello from Docker Container");
});

app.get("/api", (req, res) => {
  res.json({ message: "API running inside container" });
});

app.listen(3000, () => {
  console.log("Server running on port 3000");
});