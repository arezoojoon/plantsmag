/**
 * PM2 Ecosystem Configuration for PlantsMag SEO Engine
 *
 * Start with:  pm2 start ecosystem.config.cjs
 * Monitor:     pm2 monit
 * Logs:        pm2 logs plantsmag-seo
 */
module.exports = {
  apps: [
    {
      name: 'plantsmag-seo',
      script: 'seo-automation-cron.js',
      watch: false,
      max_restarts: 10,
      restart_delay: 30000,
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      env: {
        NODE_ENV: 'production',
      },
    },
  ],
};
