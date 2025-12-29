import React from 'react';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

import styles from './Footer.module.css';

const Footer = () => {
  const { siteConfig } = useDocusaurusContext();

  return (
    <footer className={styles.footer}>
      <div className={styles.footerContainer}>
        {/* Main Footer Content */}
        <div className={styles.footerContent}>
          {/* Left Section - Product Info */}
          <div className={styles.footerSection}>
            <h3 className={styles.footerTitle}>
              {siteConfig.title}
            </h3>
            <p className={styles.footerTagline}>
              {siteConfig.tagline}
            </p>
            <p className={styles.footerDescription}>
              An AI-native, book-first reading experience with intelligent assistance and knowledge discovery.
            </p>
          </div>

          {/* Middle Section - Documentation Links */}
          <div className={styles.footerSection}>
            <h4 className={styles.footerHeading}>Documentation</h4>
            <ul className={styles.footerLinks}>
              <li className={styles.footerLinkItem}>
                <Link to={useBaseUrl('/docs/intro')} className={styles.footerLink}>
                  Introduction
                </Link>
              </li>
              <li className={styles.footerLinkItem}>
                <Link to={useBaseUrl('/docs/chapter-1/perception')} className={styles.footerLink}>
                  Book Chapters
                </Link>
              </li>
              <li className={styles.footerLinkItem}>
                <Link to={useBaseUrl('/docs/chapter-2/human-robot-interaction')} className={styles.footerLink}>
                  CLI Tools
                </Link>
              </li>
              <li className={styles.footerLinkItem}>
                <Link to={useBaseUrl('/docs/chapter-3/neuromorphic-computing')} className={styles.footerLink}>
                  AI Agents
                </Link>
              </li>
              <li className={styles.footerLinkItem}>
                <Link to={useBaseUrl('/docs/chapter-4/humanoid-applications-industry')} className={styles.footerLink}>
                  Roadmap
                </Link>
              </li>
            </ul>
          </div>

          {/* Right Section - Community & Project Links */}
          <div className={styles.footerSection}>
            <h4 className={styles.footerHeading}>Community</h4>
            <ul className={styles.footerLinks}>
              <li className={styles.footerLinkItem}>
                <a
                  href="https://github.com/Huzafi/AI-Native-Physical-Book/tree/001-ai-book-docusaurus"
                  target="_blank"
                  rel="noopener noreferrer"
                  className={styles.footerLink}
                >
                  GitHub
                </a>
              </li>
              <li className={styles.footerLinkItem}>
                <a
                  href="https://discord.gg/docusaurus"
                  target="_blank"
                  rel="noopener noreferrer"
                  className={styles.footerLink}
                >
                  Discord
                </a>
              </li>
              <li className={styles.footerLinkItem}>
                <a
                  href="https://twitter.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className={styles.footerLink}
                >
                  Twitter
                </a>
              </li>
              <li className={styles.footerLinkItem}>
                <a
                  href="https://medium.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className={styles.footerLink}
                >
                  Blog
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className={styles.bottomBar}>
          <div className={styles.bottomContent}>
            <p className={styles.copyright}>
              &copy; {new Date().getFullYear()} {siteConfig.title}. All rights reserved.
            </p>
            <p className={styles.builtWith}>
              <span className={styles.aiIndicator}>Agentic AI Powered</span>
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;