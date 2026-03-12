import User from "../models/user.model.js";

export class UserRepository {
  static async create(data) {
    return await User.create(data);
  }

  static async findByEmail(email) {
    return await User.findOne({ email , isDeleted:false}).select("+password");
  }


  static async findById(id) {
  return await User.findOne({
    _id: id,
    isDeleted: false
  });
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
      returnDocument: "after",
      runValidators: true,
    });
  }

  static async softDelete(id) {

  return User.findByIdAndUpdate(
   id,
   {
    isDeleted: true,
    deletedAt: new Date()
   },
   { returnDocument: "after" }
  );

 }
}