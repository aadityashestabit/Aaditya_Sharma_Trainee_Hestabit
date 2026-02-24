import User from "../models/user.model.js";

export class UserRepository {
  static async create(data) {
    return await User.create(data);
  }

  static async findByEmail(email) {
    return await User.findOne({ email }).select("+password");
  }

  static async findById(id) {
    return await User.findById(id);
  }

  static async findWithQuery({ filter, options }) {
    const { sort, skip, limit } = options;

    const [users, total] = await Promise.all([
      User.find(filter)
        .sort(sort)
        .skip(skip)
        .limit(limit),

      User.countDocuments(filter),
    ]);

    return { users, total };
  }

  static async updateById(id, data) {
    return await User.findByIdAndUpdate(id, data, {
      new: true,
      runValidators: true,
    });
  }

  static async deleteById(id) {
    return await User.findByIdAndDelete(id);
  }
}