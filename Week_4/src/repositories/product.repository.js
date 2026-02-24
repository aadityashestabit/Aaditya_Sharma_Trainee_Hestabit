import Product from "../models/product.model.js";

export class ProductRepository {
  static async create(data) {
    return await Product.create(data);
  }

  static async findById(id) {
    return await Product.findById(id);
  }

  static async findAll(filter = {}) {
    return await Product.find(filter);
  }

  static async updateById(id, data) {
    return await Product.findByIdAndUpdate(id, data, {
      new: true,
      runValidators: true,
    });
  }

  static async deleteById(id) {
    return await Product.findByIdAndDelete(id);
  }


  // Find with query 
  static async findWithQuery({ filter, options }) {
    const { sort, skip, limit } = options;

    const [products, total] = await Promise.all([
      Product.find(filter)
        .sort(sort)
        .skip(skip)
        .limit(limit),

      Product.countDocuments(filter),
    ]);

    return { products, total };
  }
}