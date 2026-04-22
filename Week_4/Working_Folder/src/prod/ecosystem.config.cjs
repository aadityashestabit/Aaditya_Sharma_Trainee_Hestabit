module.exports = {
  apps: [
    {
      name: "product-api",
      script: "server.js",
      instances: "max",
      exec_mode: "cluster",

      env: {
        NODE_ENV: "local"
      },

      env_production: {
        NODE_ENV: "production"
      }
    }
  ]
};