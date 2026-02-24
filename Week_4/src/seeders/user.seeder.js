import mongoose from "mongoose";
import dotenv from "dotenv";
import User from "../models/user.model.js";

dotenv.config({ path: ".env.local" });

const users = [];

for (let i = 1; i <= 40; i++) {
  users.push({
    name: `User ${i}`,
    email: `user${i}@example.com`,
    password: "password123", 
    about: `This is user ${i}`,
    role: i === 1 ? "admin" : "user", 
    isActive: true,
  });
}

const seedUsers = async () => {
  try {
    await mongoose.connect(process.env.DB_URI);

    await User.deleteMany(); 

    await User.create(users); 

    console.log("Users seeded successfully");
    process.exit();
  } catch (error) {
    console.error("Seeder error", error);
    process.exit(1);
  }
};

seedUsers();