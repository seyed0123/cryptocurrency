const webpack = require('webpack');

module.exports = function override(config, env) {
  // Change devtool to source-map instead of eval
  if (process.env.NODE_ENV === 'development') {
    config.devtool = 'source-map';
  }

  // Add your own webpack config modifications here
  config.devServer = {
    ...config.devServer,
    headers: {
      // Remove frame-ancestors from meta and add it here in the header
      'Content-Security-Policy': `
        default-src 'self';
        script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://*.infura.io;
        style-src 'self' 'unsafe-inline';
        connect-src 'self' https://*.infura.io wss://*.infura.io https://api.coingecko.com https://*.walletconnect.org wss://*.walletconnect.org https://*.walletconnect.com wss://*.walletconnect.com https://ethereum-api.xyz https://*.ethereum-api.xyz https://*.blocknative.com wss://*.blocknative.com;
        img-src 'self' data: https: http:;
        font-src 'self' data:;
        object-src 'none';
        base-uri 'self';
        form-action 'self';
      `.replace(/\s+/g, ' ').trim()
    }
  };

  // Disable minimization in development
  if (process.env.NODE_ENV === 'development') {
    config.optimization = {
      ...config.optimization,
      minimize: false,
      minimizer: []
    };
  }

  // Add ProvidePlugin to inject Buffer globally
  config.plugins = [
    ...config.plugins,
    new webpack.ProvidePlugin({
      Buffer: ['buffer', 'Buffer'],
    }),
    new webpack.ProvidePlugin({
      process: 'process/browser',
    })
  ];

  // Add fallbacks for crypto-related modules
  config.resolve.fallback = {
    ...config.resolve.fallback,
    "crypto": require.resolve("crypto-browserify"),
    "stream": require.resolve("stream-browserify"),
    "assert": require.resolve("assert/"),
    "http": require.resolve("stream-http"),
    "https": require.resolve("https-browserify"),
    "os": require.resolve("os-browserify/browser"),
    "url": require.resolve("url/")
  };

  return config;
}; 