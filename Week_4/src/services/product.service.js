import { ProductRepository } from "../repositories/product.repository.js";

export class ProductService {
  static async createProduct(data, userId) {
    data.createdBy = userId;
    return await ProductRepository.create(data);
  }

  static async getProductById(id) {
    const product = await ProductRepository.findById(id);
    if (!product) {
      throw new Error("Product not found");
    }
    return product;
  }

  static async getAllProducts(query) {
    const filter = {};

    if (query.category) filter.category = query.category;
    if (query.brand) filter.brand = query.brand;
    if (query.minPrice && query.maxPrice) {
      filter.price = {
        $gte: query.minPrice,
        $lte: query.maxPrice,
      };
    }

    return await ProductRepository.findAll(filter);
  }

  static async updateProduct(id, data) {
    const updated = await ProductRepository.updateById(id, data);
    if (!updated) {
      throw new Error("Product not found");
    }
    return updated;
  }

  static async deleteProduct(id) {
    const deleted = await ProductRepository.deleteById(id);
    if (!deleted) {
      throw new Error("Product not found");
    }
    return deleted;
  }



  // pagination support 
  static async getAllProducts(query) {
    const {
      page = 1,
      limit = 10,
      sort = "-createdAt",
      search,
      category,
      brand,
      minPrice,
      maxPrice,
    } = query;

    // Pagination
    const pageNumber = parseInt(page);
    const limitNumber = parseInt(limit);
    const skip = (pageNumber - 1) * limitNumber;

    // Filtering
    const filter = { isActive: true };

    if (category) filter.category = category;
    if (brand) filter.brand = brand;

    if (minPrice || maxPrice) {
      filter.price = {};
      if (minPrice) filter.price.$gte = Number(minPrice);
      if (maxPrice) filter.price.$lte = Number(maxPrice);
    }

    // Searching
    if (search) {
      filter.$or = [
        { title: { $regex: search, $options: "i" } },
        { description: { $regex: search, $options: "i" } },
      ];
    }

    const options = {
      sort,
      skip,
      limit: limitNumber,
    };

    const { products, total } =
      await ProductRepository.findWithQuery({ filter, options });

    return {
      products,
      pagination: {
        total,
        page: pageNumber,
        limit: limitNumber,
        totalPages: Math.ceil(total / limitNumber),
      },
    };
  }
}