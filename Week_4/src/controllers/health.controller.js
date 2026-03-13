export class HealthController {
  static check(req, res) {
    res.status(200).json({
      success: true,
      message: "API is running",
      uptime: process.uptime(),
      timestamp: new Date()
    });
  }
}