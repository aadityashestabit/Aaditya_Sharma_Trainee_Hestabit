import dotenv from "dotenv";
import path from "path";
import Joi from "joi";

const ENV = process.env.NODE_ENV || "local";

const envFileMap = {
  local: ".env.local",
  development: ".env.dev",
  production: ".env.prod",
};

const envFile = envFileMap[ENV];

dotenv.config({
  path: path.resolve(process.cwd(), envFile),
});

// Joi validation 
const envSchema = Joi.object({
  NODE_ENV: Joi.string()
    .valid("local", "development", "production")
    .required(),

  PORT: Joi.number().required(),

  DB_URI: Joi.string().required(),

  JWT_SECRET: Joi.string().min(10).required(),
}).unknown();

const { value, error } = envSchema.validate(process.env);

if (error) {
  console.error("Environment Validation Error:");
  console.error(error.message);
  process.exit(1); // Crash app 
}


console.log(`Loaded environment: ${ENV}`);
console.log(`Using file: ${envFile}`);

export const config = {
  port: process.env.PORT,
  dbUri: process.env.DB_URI,
  jwtSecret: process.env.JWT_SECRET,
  nodeEnv: process.env.NODE_ENV,
};