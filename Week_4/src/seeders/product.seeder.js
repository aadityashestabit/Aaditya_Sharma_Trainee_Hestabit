import mongoose from "mongoose";
import dotenv from "dotenv";
import path from "path";
import { fileURLToPath } from "url";
import Product from "../models/product.model.js";


const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
dotenv.config({
  path: path.resolve(__dirname, "../../.env.local"),
});

const products = [
  {
    title: "iPhone 15 Pro",
    description: "Latest Apple flagship smartphone",
    category: "electronics",
    price: 129999,
    brand: "Apple",
    stock: 50,
    minPrice: 120000,
    maxPrice: 140000,
  },
  {
    title: "Samsung Galaxy S24",
    description: "Premium Android smartphone",
    category: "electronics",
    price: 99999,
    brand: "Samsung",
    stock: 40,
    minPrice: 90000,
    maxPrice: 110000,
  },
  {
    title: "MacBook Air M3",
    description: "Lightweight performance laptop",
    category: "laptops",
    price: 149999,
    brand: "Apple",
    stock: 25,
    minPrice: 140000,
    maxPrice: 160000,
  },
  {
    title: "Nike Air Max",
    description: "Comfortable sports shoes",
    category: "fashion",
    price: 8999,
    brand: "Nike",
    stock: 100,
    minPrice: 7000,
    maxPrice: 10000,
  },
];



// seeder logic 

const seedProducts = async () => {
  try {
    await mongoose.connect(process.env.DB_URI);

  
    await Product.deleteMany();

 
    await Product.create(products);

    console.log("Products seeded successfully");

    process.exit();
  } catch (error) {
    console.error("Seeder error", error);
    process.exit(1);
  }
};

seedProducts();