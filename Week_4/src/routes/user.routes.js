import express from "express";
import { UserController } from "../controllers/user.controller.js";

const router = express.Router();

// PUBLIC ROUTES

router.post("/", UserController.create);       
router.post("/login", UserController.login);   

// Admin Routes 
router.get("/", UserController.getAll);        
router.get("/:id", UserController.getOne);    
router.patch("/:id", UserController.update);   
router.delete("/:id", UserController.delete);  

export default router;