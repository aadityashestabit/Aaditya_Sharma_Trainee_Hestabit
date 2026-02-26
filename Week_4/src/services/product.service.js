import { ProductRepository } from "../repositories/product.repository.js";
import { encodeCursor, decodeCursor } from "../utils/cursor.js";

export class ProductService {
  static async createProduct(data, userId) {
    data.createdBy = userId;
    return await ProductRepository.create(data);
  }

  static async getProductById(id) {
    const product = await ProductRepository.findById(id);
    if (!product) {
      throw new AppError("Product not found", 404, "PRODUCT_NOT_FOUND");
    }
    return product;
  }

  static async updateProduct(id, data) {
    const updated = await ProductRepository.updateById(id, data);
    if (!updated) {
      throw new AppError("Product not found", 404, "PRODUCT_NOT_FOUND");
    }
    return updated;
  }

  static async deleteProduct(id) {
    const deleted = await ProductRepository.deleteById(id);
    if (!deleted) {
      throw new AppError("Product not found", 404, "PRODUCT_NOT_FOUND");
    }
    return deleted;
  }

  static async getAllProducts(query) {
    
    // Extracting Query Params with Defaults
   
    let limit = query.limit;
    let cursor = query.cursor;
    let sort = query.sort;
    let order = query.order;
    let direction = query.direction;
    let search = query.search;
    let category = query.category;
    let brand = query.brand;
    let minPrice = query.minPrice;
    let maxPrice = query.maxPrice;

    limit = parseInt(limit);

    if (isNaN(limit)) {
      limit = 10; 
    }

    if (limit < 0) {
      limit = 10;
    }

    if (limit === 0) {
      return {
        products: [],
        nextCursor: null,
        prevCursor: null,
      };
    }

    if (limit > 100) {
      limit = 100;
    }

    if (!sort) sort = "_id";
    if (!order) order = "desc";
    if (!direction) direction = "next";

    const limitNumber = parseInt(limit);

    let sortOrder;
    if (order === "asc") {
      sortOrder = 1;
    } else {
      sortOrder = -1;
    }

    
    // BASE FILTER
    
    const filter = {
      isActive: true,
      isDeleted: { $ne: true },
    };

    
    // CATEGORY FILTER
    
    if (category) {
      filter.category = category;
    }

    
    // BRAND FILTER
    
    if (brand) {
      filter.brand = brand;
    }

    
    // PRICE RANGE FILTER
    
    if (minPrice || maxPrice) {
      filter.price = {};

      if (minPrice) {
        filter.price.$gte = Number(minPrice);
      }

      if (maxPrice) {
        filter.price.$lte = Number(maxPrice);
      }
    }

    
    // SEARCH FILTER
    
    if (search) {
      filter.$or = [
        { title: { $regex: search, $options: "i" } },
        { description: { $regex: search, $options: "i" } },
      ];
    }

    
    // Validate Sort Field
   
    const allowedSortFields = ["_id", "price", "createdAt"];

    let sortField;

    if (allowedSortFields.includes(sort)) {
      sortField = sort;
    } else {
      sortField = "_id";
    }

  
    // Decode Cursor
   
    let cursorData = null;

    if (cursor) {
      cursorData = decodeCursor(cursor);
    }

    
    // Call Repository
    
    let products = await ProductRepository.findWithAdvancedCursor({
      filter,
      sortField,
      sortOrder,
      limit: limitNumber,
      cursorData,
      direction,
    });

   
    // Generate Next Cursor
    
    let nextCursor = null;
    let prevCursor = null;

    if (products.length > 0) {
      const lastProduct = products[products.length - 1];
      const firstProduct = products[0];

      nextCursor = encodeCursor({
        value: lastProduct[sortField],
        id: lastProduct._id,
      });

      prevCursor = encodeCursor({
        value: firstProduct[sortField],
        id: firstProduct._id,
      });
    }

    return {
      products,
      nextCursor,
      prevCursor,
    };
  }
}
