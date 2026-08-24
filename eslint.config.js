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
    // `tests/ui/**` su isti obrazac kao playwright/**: Playwright spec-ovi koji
    // vrte pravi pregledac, samo se pokrecu kroz playwright-ui.config.js.
    files: ['playwright/**/*.js', 'tests/ui/**/*.js'],
    languageOptions: {
      sourceType: 'commonjs',
      globals: {
        ...globals.node,
        // Telo `page.evaluate(() => ...)` se izvrsava U PREGLEDACU, ne u
        // Node-u — `document`, `window` i `getComputedStyle` tamo postoje.
        // Bez ovoga ESLint ih prijavljuje kao no-undef, sto je bio razlog
        // sto je QA Lint padao na svakom push-u (124 greske, 17.08.2026).
        ...globals.browser,
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
