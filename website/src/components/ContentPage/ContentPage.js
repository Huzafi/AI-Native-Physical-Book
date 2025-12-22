import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import { useLocation } from '@docusaurus/router';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './ContentPage.module.css';

const ContentPage = ({ children, title, description }) => {
  const location = useLocation();
  const { siteConfig } = useDocusaurusContext();

  return (
    <Layout
      title={title || "AI-Native Book"}
      description={description || siteConfig.tagline}
      wrapperClassName={styles.contentPageWrapper}
    >
      <main className={clsx('container', styles.contentPageMain)}>
        <div className={styles.contentContainer}>
          {children}
        </div>
      </main>
    </Layout>
  );
};

export default ContentPage;