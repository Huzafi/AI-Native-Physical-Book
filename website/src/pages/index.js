import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();

  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <div className={styles.heroContent}>
          <div className={styles.heroText}>
            <Heading as="h1" className="hero__title">
              {siteConfig.title}
            </Heading>

            <p className="hero__subtitle">
              {siteConfig.tagline}
            </p>

            <div className={styles.buttons}>
              <Link
                className="button button--primary button--lg"
                to="/docs/intro"
              >
                Start Reading
              </Link>
              <Link
                className="button button--secondary button--lg"
                to="/docs"
              >
                Explore the Book
              </Link>
            </div>
          </div>
          <div className={styles.heroImage}>
            <div className={styles.bookCover}>
              <div className={styles.bookSpine}></div>
              <div className={styles.bookCoverFront}>
                <div className={styles.bookTitle}>AI-Native<br/>Book</div>
                <div className={styles.bookAuthor}>Advanced Concepts</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

function BookFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          <div className="col col--4">
            <div className={`${styles.featureCard} text--center padding-horiz--md`}>
              <div className={styles.featureIcon}>📚</div>
              <Heading as="h3">Book-First Experience</Heading>
              <p>
                Designed from the ground up as a book-like interface with
                structured chapters and a smooth reading flow.
              </p>
            </div>
          </div>

          <div className="col col--4">
            <div className={`${styles.featureCard} text--center padding-horiz--md`}>
              <div className={styles.featureIcon}>🤖</div>
              <Heading as="h3">AI Assistance</Heading>
              <p>
                Optional AI assistant that answers questions strictly
                from the book's content to deepen understanding.
              </p>
            </div>
          </div>

          <div className="col col--4">
            <div className={`${styles.featureCard} text--center padding-horiz--md`}>
              <div className={styles.featureIcon}>🌐</div>
              <Heading as="h3">Multiple Languages</Heading>
              <p>
                Read in multiple languages with optional translations
                and summaries for better accessibility.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function BookPreview() {
  return (
    <section className={styles.bookPreview}>
      <div className="container">
        <div className="row">
          <div className="col col--12">
            <div className={styles.previewHeader}>
              <Heading as="h2" className={styles.previewTitle}>Preview Chapter</Heading>
              <p className={styles.previewSubtitle}>Explore a sample from our content</p>
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col col--8 col--offset-2">
            <div className={styles.previewContent}>
              <div className={styles.previewPage}>
                <h3 className={styles.previewChapter}>Chapter 1: Introduction to AI Concepts</h3>
                <p className={styles.previewText}>
                  Artificial Intelligence has revolutionized the way we interact with technology.
                  From simple rule-based systems to complex neural networks, AI continues to evolve
                  and reshape our understanding of machine capabilities.
                </p>
                <p className={styles.previewText}>
                  This book explores the fundamental concepts that underpin modern AI systems,
                  providing both theoretical foundations and practical applications. Each chapter
                  builds upon previous knowledge to create a comprehensive understanding of AI technologies.
                </p>
                <div className={styles.previewHighlight}>
                  <strong>Key Topics:</strong> Machine Learning, Neural Networks, Natural Language Processing,
                  Computer Vision, Ethics in AI
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  const { siteConfig } = useDocusaurusContext();

  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="A book-first reading experience enhanced with AI assistance"
    >
      <HomepageHeader />
      <main>
        <BookPreview />
        <BookFeatures />
      </main>
    </Layout>
  );
}