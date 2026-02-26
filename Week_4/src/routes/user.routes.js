import express from "express";
import { UserController } from "../controllers/user.controller.js";
import { authenticate } from "../middlewares/auth.middleware.js";

const router = express.Router();


router.post("/create", UserController.create);       
router.post("/login", UserController.login);   

// Admin Routes 
router.get("/", authenticate, UserController.getAll);        
router.get("/:id", authenticate, UserController.getOne);    
router.patch("/:id", authenticate, UserController.update);   
router.delete("/:id", authenticate, UserController.delete);  

export default router;