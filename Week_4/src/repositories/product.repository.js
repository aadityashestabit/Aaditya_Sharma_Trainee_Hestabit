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
    const product = await Product.findById(id);

    if(!product){
      return null;
    }

    product.isDeleted = true;
    product.deletedAt = new Date();
    product.isActive = false

    await product.save();


    return product;


  }


  // advanced cursor with next and previous

  static async findWithAdvancedCursor({
  filter,
  sortField,
  sortOrder,
  limit,
  cursorData,
  direction,
}) {
  let cursorQuery = {};

  // comparison 
  
  let comparisonOperator;

  if (direction === "next") {
    if (sortOrder === 1) {
      comparisonOperator = "$gt";   // ascending → next means greater than
    } else {
      comparisonOperator = "$lt";   // descending → next means smaller than
    }
  } else {
    // direction === "prev"
    if (sortOrder === 1) {
      comparisonOperator = "$lt";   // ascending → previous means smaller
    } else {
      comparisonOperator = "$gt";   // descending → previous means greater
    }
  }

  
  // Build cursor query
  
  if (cursorData) {
    cursorQuery = {
      $or: [
        { [sortField]: { [comparisonOperator]: cursorData.value } },
        {
          [sortField]: cursorData.value,
          _id: { [comparisonOperator]: cursorData.id },
        },
      ],
    };
  }

 
  // Combine filter + cursor query
  
  let finalFilter;

  if (cursorData) {
    finalFilter = { $and: [filter, cursorQuery] };
  } else {
    finalFilter = filter;
  }

  
  // Execute query
  
  let products = await Product.find(finalFilter)
    .sort({ [sortField]: sortOrder, _id: sortOrder })
    .limit(limit);

  
  // Reverse if previous direction
  
  if (direction === "prev") {
    products = products.reverse();
  }

  return products;
}
}
