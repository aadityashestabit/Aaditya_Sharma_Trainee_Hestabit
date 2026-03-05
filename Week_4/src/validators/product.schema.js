import Joi from "joi";

export const productSchema = Joi.object({
  title: Joi.string().min(3).max(100).required(),
  price: Joi.number().positive().required(),
  description: Joi.string().max(500).required(),
  category: Joi.string().required(),
  brand: Joi.string().required(),
  stock: Joi.number().integer().min(0).required()
});