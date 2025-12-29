// @ts-check
// @type JSDoc annotations allow editor autocompletion and type checking
// (when paired with @ts-check).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical-AI & Humanoids Book 📘',
  tagline: 'A book-first reading experience with AI assistance',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://ai-native-book-green.vercel.app/',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'Hackathon_claude', // Usually your GitHub org/user name.
  projectName: 'Hackathon-AI-Book', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl: 'https://github.com/Huzafi/AI-Native-Physical-Book/tree/001-ai-book-docusaurus/website',
          showLastUpdateAuthor: false,
          showLastUpdateTime: false,
        },
        blog: false, // Disable blog if not needed
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'AI-Native Book',
        logo: {
          alt: 'AI-Native Book Logo',
          src: 'img/logo.svg',
        },
        items: [
          {type: 'docSidebar', sidebarId: 'tutorialSidebar', position: 'left', label: 'Book'},
          {href: 'https://github.com/Huzafi/AI-Native-Physical-Book/tree/001-ai-book-docusaurus', label: 'GitHub', position: 'right'},
          {type: 'search', position: 'right', className: 'header-search'},
          {href: '#', label: 'Sign In', position: 'right', className: 'header-signin'},
          {href: '#', label: 'Sign Up', position: 'right', className: 'header-signup'},
        ],
      },
      docs: {
        sidebar: {
          hideable: false,
          autoCollapseCategories: false,
        },
      },
      footer: {
        style: 'dark',
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;