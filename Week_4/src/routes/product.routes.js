import express from "express";
import { ProductController } from "../controllers/product.controller.js";

const router = express.Router();

router.post("/", ProductController.create);
router.get("/", ProductController.getAll);
router.get("/:id", ProductController.getOne);
router.patch("/:id", ProductController.update);
router.delete("/:id", ProductController.delete);

export default router;