module.exports = {
  plugins: [
    {
      name: 'preset-default',
      params: {
        overrides: {
          cleanupIDs: false,
          removeUnusedNS: false,
          removeUselessDefs: false,
          removeEditorsNSData: false,
        },
      },
    },
  ],
};
