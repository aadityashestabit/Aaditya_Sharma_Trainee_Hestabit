// We are creating our own custom Error type called AppError
// "extends Error" means AppError is based on the built-in JavaScript Error
// Think of it like: AppError is a Error, but with extra information added

export class AppError extends Error {

  // constructor runs automatically when you do: new AppError(...)
  // It receives 3 pieces of information:
  //   message    → what went wrong         e.g. "Product not found"
  //   statusCode → which HTTP code to send e.g. 404, 400, 500
  //   code       → a short label for error e.g. "PRODUCT_NOT_FOUND"

  constructor(message, statusCode, code) {

    // Step 1: Call the parent Error class first
    // super(message) is like saying: "Hey built-in Error, do your job with this message"
    // This sets up this.message and this.stack automatically for us
    // NOTE: In JavaScript, you MUST call super() before using "this" in a child class
    super(message);

    // Step 2: Store the HTTP status code on this error
    // e.g. 404 = Not Found, 400 = Bad Request, 401 = Unauthorized
    // Now when we catch this error, we know which status code to send back
    this.statusCode = statusCode;

    // Step 3: Store the short error code label
    // If no code is provided, fall back to a default "APP_ERROR"
    // e.g. "PRODUCT_NOT_FOUND", "INVALID_TOKEN", "DUPLICATE_EMAIL"
    this.code = code || "APP_ERROR";

    // Step 4: Mark this as an "operational" error
    // Operational = we expected this could happen (user not found, wrong password)
    // Non-operational = unexpected bug (null reference, database crash)
    // We use this flag later in the error handler to decide what to show the user
    this.isOperational = true;

    // Step 5: Clean up the stack trace
    // By default, the stack trace includes AppError itself, which is noise
    // This line removes AppError from the trace so it points to where the
    // error was actually THROWN in your code, not where AppError was defined
    Error.captureStackTrace(this, this.constructor);
  }
}