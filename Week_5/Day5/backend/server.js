import express from "express";

const app = express();

app.get("/api", (req, res) => {
  res.json({
    message: "Backend running in Docker"
  });
});

app.listen(3000, () => {
  console.log("Server running on port 3000");
});