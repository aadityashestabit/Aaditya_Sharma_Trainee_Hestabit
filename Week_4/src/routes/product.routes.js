import express from "express";
import { ProductController } from "../controllers/product.controller.js";
import { authenticate } from "../middlewares/auth.middleware.js";

const router = express.Router();

router.post("/", authenticate, ProductController.create);
router.get("/", authenticate, ProductController.getAll);
router.get("/:id",authenticate, ProductController.getOne);
router.patch("/:id", authenticate,ProductController.update);
router.delete("/:id",authenticate, ProductController.delete);

export default router;