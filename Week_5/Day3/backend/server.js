import express from "express";

const app = express();

const PORT = 3000;

app.get("/api", (req, res) => {
  res.json({
    message: "Hello from backend",
    container: process.env.HOSTNAME
  });
});

app.listen(PORT, () => {
  console.log(`Server running on ${PORT}`);
});