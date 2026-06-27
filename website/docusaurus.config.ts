import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Argus Standards',
  tagline: 'One command. Every AI coding agent. Consistent engineering standards.',
  favicon: 'img/favicon.ico',

  url: 'https://pmurasky.github.io',
  baseUrl: '/argus/',

  organizationName: 'pmurasky',
  projectName: 'argus',
  trailingSlash: false,

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: '/',
          editUrl: 'https://github.com/pmurasky/argus/edit/main/website/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    navbar: {
      title: 'Argus Standards',
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docsSidebar',
          position: 'left',
          label: 'Docs',
        },
        {
          href: 'https://github.com/pmurasky/argus',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Get Started',
          items: [
            {label: 'Installation', to: '/installation'},
            {label: 'Quick Start', to: '/quick-start'},
            {label: 'Configuration', to: '/configuration'},
          ],
        },
        {
          title: 'Reference',
          items: [
            {label: 'Packs', to: '/packs/workflow/tdd'},
            {label: 'Platforms', to: '/platforms'},
            {label: 'CI Integration', to: '/ci-integration'},
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/pmurasky/argus',
            },
            {
              label: 'PyPI',
              href: 'https://pypi.org/project/argus-standards/',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Peter Murasky Jr. MIT License.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['bash', 'yaml', 'python'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
