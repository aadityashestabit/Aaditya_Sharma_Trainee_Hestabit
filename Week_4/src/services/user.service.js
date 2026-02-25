import jwt from "jsonwebtoken";
import { config } from "../config/index.js";
import { UserRepository } from "../repositories/user.repository.js";

export class UserService {
  static async createUser(data) {
    return await UserRepository.create(data);
  }

  static async getUserById(id) {
    const user = await UserRepository.findById(id);
    if (!user) throw new Error("User not found");
    return user;
  }

  static async login(email, password) {
    const user = await UserRepository.findByEmail(email);
    if (!user) throw new Error("Invalid credentials");

    const isMatch = await user.comparePassword(password);
    if (!isMatch) throw new Error("Invalid credentials");

    // ✅ Generate JWT token
    const token = jwt.sign(
      { id: user._id, email: user.email },
      config.jwtSecret,
      { expiresIn: "7d" }
    );

    return { user, token };
  }

  static async getAllUsers(query) {
    const {
      page = 1,
      limit = 10,
      sort = "-createdAt",
      search,
      role,
      isActive,
    } = query;

    const pageNumber = parseInt(page);
    const limitNumber = parseInt(limit);
    const skip = (pageNumber - 1) * limitNumber;

    const filter = {};

    if (role) filter.role = role;
    if (isActive !== undefined) filter.isActive = isActive === "true";

    // Text search (indexed)
    if (search) {
      filter.$text = { $search: search };
    }

    const options = {
      sort,
      skip,
      limit: limitNumber,
    };

    const { users, total } =
      await UserRepository.findWithQuery({ filter, options });

    return {
      users,
      pagination: {
        total,
        page: pageNumber,
        limit: limitNumber,
        totalPages: Math.ceil(total / limitNumber),
      },
    };
  }

  static async updateUser(id, data) {
    const updated = await UserRepository.updateById(id, data);
    if (!updated) throw new Error("User not found");
    return updated;
  }

  static async deleteUser(id) {
    const deleted = await UserRepository.deleteById(id);
    if (!deleted) throw new Error("User not found");
    return deleted;
  }
}