const path = require('path');

module.exports = {
  entry: {
    main: './js/handlers/searchInputHandler.js',
  },
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, 'dist'),
  },
  externals: {
    base64id: 'base64id',
    'socket.io': 'io', // Use the package name 'socket.io' and assign it to 'io'
  },
  devServer: {
    hot: true,
  },
  resolve: {
    fallback: {
      fs: false,
      path: require.resolve('path-browserify'),
      buffer: require.resolve('buffer/'),
      util: require.resolve('util/'),
      assert: require.resolve('assert/'),
      stream: require.resolve('stream-browserify'),
      zlib: require.resolve('browserify-zlib'),
      http: require.resolve('stream-http'),
      https: require.resolve('https-browserify'),
      http2: require.resolve('http2'),
      os: require.resolve('os-browserify/browser'),
      tty: require.resolve('tty-browserify'),
      process: require.resolve('process/browser'),
      timers: require.resolve('timers-browserify'),
      url: require.resolve('url/'),
      vm: require.resolve('vm-browserify'),
      querystring: require.resolve('querystring-es3'),
      crypto: require.resolve('crypto-browserify'),
      querystring: false,
      // net: require.resolve('net-browserify'),
      // tls: require.resolve('tls-browserify'),
      bufferutil: require.resolve('bufferutil'),
      'utf-8-validate': require.resolve('utf-8-validate'),
    },
  },
  mode: 'development',
  target: 'web',
};
