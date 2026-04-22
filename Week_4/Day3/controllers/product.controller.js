import { ProductService } from "../services/product.service.js";

export class ProductController {
  static async create(req, res, next) {
    try {
      const product = await ProductService.createProduct(
        req.body,
        req.user?.id
      );

      res.status(201).json({
        success: true,
        data: product,
      });
    } catch (err) {
      next(err);
    }
  }

  static async getOne(req, res, next) {
    try {
      const product = await ProductService.getProductById(req.params.id);

      res.status(200).json({
        success: true,
        data: product,
      });
    } catch (err) {
      next(err);
    }
  }

// controller with pagination support 
  static async getAll(req, res, next) {
  try {
    const result = await ProductService.getAllProducts(req.query);

    res.status(200).json({
      success: true,
      ...result,
    });
  } catch (err) {
    next(err);
  }
}

  static async update(req, res, next) {
    try {
      const updated = await ProductService.updateProduct(
        req.params.id,
        req.body
      );

      res.status(200).json({
        success: true,
        data: updated,
      });
    } catch (err) {
      next(err);
    }
  }

  static async delete(req, res, next) {
    try {
      await ProductService.deleteProduct(req.params.id);

      res.status(204).json({
        success: true,
        message: "Product deleted successfully",
      });
    } catch (err) {
      next(err);
    }
  }
}