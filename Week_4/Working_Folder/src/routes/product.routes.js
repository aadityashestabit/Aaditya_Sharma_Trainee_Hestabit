import express from "express";
import { ProductController } from "../controllers/product.controller.js";
import { authenticate } from "../middlewares/auth.middleware.js";
import { validate } from "../middlewares/validate.js";
import { productSchema } from "../validators/product.schema.js";

const router = express.Router();

router.post("/", authenticate, validate(productSchema), ProductController.create);
router.get("/", authenticate, ProductController.getAll);
router.get("/:id",authenticate, ProductController.getOne);
router.patch("/:id", authenticate, validate(productSchema), ProductController.update);
router.delete("/:id",authenticate, ProductController.delete);

export default router;