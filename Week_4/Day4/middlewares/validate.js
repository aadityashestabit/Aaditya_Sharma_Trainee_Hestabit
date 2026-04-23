export const validate = (schema) => (req, res, next) => {
  try {
    const { error, value } = schema.validate(req.body, {
      abortEarly: false,
      stripUnknown: true
    });

    if (error) {
      return res.status(400).json({
        success: false,
        message: "Validation failed",
        errors: error.details.map(err => err.message)
      });
    }

    req.body = value;
    next();

  } catch (error) {
    next(error);
  }
};