module.exports = {
  PORT: process.env.PORT || 3001,
  PYTHON_API_URL: process.env.PYTHON_API_URL || 'http://localhost:8000',
  SERVICE_KEY: process.env.SERVICE_KEY || 'notify-svc-key',
  RETRY_ATTEMPTS: 3,
  TIMEOUT_MS: 5000,
};
