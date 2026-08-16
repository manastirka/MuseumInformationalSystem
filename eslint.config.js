const js = require('@eslint/js');
const globals = require('globals');

module.exports = [
  {
    ignores: [
      'node_modules/**',
      'playwright-report/**',
      'test-results/**',
      'coverage/**'
    ]
  },
  js.configs.recommended,
  {
    files: ['cypress/**/*.js', 'playwright/**/*.js', 'load/**/*.js', '*.config.js'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'commonjs',
      globals: {
        ...globals.node
      }
    },
    rules: {
      curly: ['error', 'all'],
      eqeqeq: ['error', 'always'],
      'no-console': ['warn', { allow: ['warn', 'error'] }],
      'no-unused-vars': ['error', { argsIgnorePattern: '^_' }]
    }
  },
  {
    files: ['cypress/**/*.js'],
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
        afterEach: 'readonly',
        beforeEach: 'readonly',
        cy: 'readonly',
        Cypress: 'readonly',
        describe: 'readonly',
        expect: 'readonly',
        it: 'readonly'
      }
    }
  },
  {
    files: ['playwright/**/*.js'],
    languageOptions: {
      sourceType: 'module',
      globals: {
        ...globals.node,
        test: 'readonly',
        expect: 'readonly'
      }
    }
  },
  {
    files: ['load/**/*.js'],
    languageOptions: {
      sourceType: 'module',
      globals: {
        ...globals.node,
        __ENV: 'readonly'
      }
    }
  }
];
