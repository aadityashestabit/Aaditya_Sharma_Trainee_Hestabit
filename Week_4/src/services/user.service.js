  import jwt from "jsonwebtoken";
  import { config } from "../config/index.js";
  import { UserRepository } from "../repositories/user.repository.js";
  import { AppError } from "../utils/AppError.js";

  export class UserService {
    static async createUser(data) {
      return await UserRepository.create(data);
    }

    static async getUserById(id) {
      const user = await UserRepository.findById(id);
      if (!user) {
        throw new AppError("User not found", 404, "USER_NOT_FOUND");
      }
      return user;
    }

    static async login(email, password) {
      const user = await UserRepository.findByEmail(email);
      if (!user) {
        throw new AppError("Invalid credentials", 401, "INVALID_CREDENTIALS");
      }

      const isMatch = await user.comparePassword(password);
      if (!isMatch) {
        throw new AppError("Invalid credentials", 401, "INVALID_CREDENTIALS");
      }

      // Generate JWT token
      const token = jwt.sign(
        { id: user._id, email: user.email },
        config.jwtSecret,
        { expiresIn: "7d" },
      );

      const userObj = user.toObject();
      delete userObj.password;

      return { user: userObj, token };
    }

    static async getAllUsers() {
      const filter = {
        isDeleted: false,
        isActive: true,
      };

      const users = await UserRepository.findAllActive(filter);

      return users;
    }

    static async updateUser(id, data) {
      const updated = await UserRepository.updateById(id, data);
      if (!updated) {
        throw new AppError("User not found", 404, "USER_NOT_FOUND");
      }
      return updated;
    }

    static async deleteUser(id) {
      const deleted = await UserRepository.softDelete(id);
      if (!deleted) {
        throw new AppError("User not found", 404, "USER_NOT_FOUND");
      }
      return deleted;
    }
  }
