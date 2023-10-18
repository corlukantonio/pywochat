module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  transform: {
    '^.+\\.m?js$': 'babel-jest',
  },
  moduleFileExtensions: ['js', 'mjs'],
  moduleNameMapper: {},
  setupFilesAfterEnv: ['./setupTests.js'],
};
