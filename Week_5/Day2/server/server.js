import express from "express";
import mongoose from "mongoose";

const app = express();

mongoose.connect(process.env.MONGO_URL)
.then(()=>console.log("Mongo connected"))
.catch(err=>console.log(err));

app.get("/api", (req,res)=>{
    res.json({message:"Backend API working"});
});

app.listen(3000, ()=>{
    console.log("Server running on port 3000");
});