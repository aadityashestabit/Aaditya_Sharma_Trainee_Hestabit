import { UserService } from "../services/user.service.js";

export class UserController {

  static async start(req,res,next){
    try {
      res.status(201).json({
        success:true,
        data:"Server Running"
      })
    } catch (error) {
      next(error)
    }
  }
  static async create(req, res, next) {
    try {
      const user = await UserService.createUser(req.body);

      res.status(201).json({
        success: true,
        data: user,
      });
    } catch (err) {
      next(err);
    }
  }

  static async login(req, res, next) {
  try {
    const { email, password } = req.body;

    const user = await UserService.login(email, password);

    res.status(200).json({
      success: true,
      message: "Login successful",
      data: user,
    });
  } catch (err) {
    next(err);
  }
}

  static async getAll(req, res, next) {
    try {
      const result = await UserService.getAllUsers(req.query);

      res.status(200).json({
        success: true,
        ...result,
      });
    } catch (err) {
      next(err);
    }
  }

  static async getOne(req, res, next) {
    try {
      const user = await UserService.getUserById(req.params.id);

      res.status(200).json({
        success: true,
        data: user,
      });
    } catch (err) {
      next(err);
    }
  }

  static async update(req, res, next) {
    try {
      const updated = await UserService.updateUser(
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
      await UserService.deleteUser(req.params.id);

      res.status(204).json({
        success: true,
        message: "User deleted successfully",
      });
    } catch (err) {
      next(err);
    }
  }
}