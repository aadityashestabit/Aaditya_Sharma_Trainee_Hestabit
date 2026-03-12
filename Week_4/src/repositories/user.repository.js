import User from "../models/user.model.js";

export class UserRepository {

  static async create(data) {
    return await User.create(data);
  }

  static async findByEmail(email) {
    return await User.findOne({
      email,
      isDeleted: false
    }).select("+password");
  }

  static async findById(id) {
    return await User.findOne({
      _id: id,
      isDeleted: false
    });
  }

  static async findAllActive() {
    return await User.find({
      isDeleted: false,
      isActive: true
    });
  }

  static async updateById(id, data) {
    return await User.findOneAndUpdate(
      { _id: id, isDeleted: false },
      data,
      {
        returnDocument: "after",
        runValidators: true
      }
    );
  }

  static async softDelete(id) {
    return await User.findOneAndUpdate(
      { _id: id, isDeleted: false },
      {
        isDeleted: true,
        deletedAt: new Date()
      },
      { returnDocument: "after" }
    );
  }

}