import React from 'react';
import Head from '@docusaurus/Head';
import { useLocation } from '@docusaurus/router';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import useBaseUrl from '@docusaurus/useBaseUrl';

const SEOHead = ({ title, description, image, pathname, type = 'article' }) => {
  const location = useLocation();
  const { siteConfig } = useDocusaurusContext();
  const baseUrl = useBaseUrl('/');

  // Use provided values or fallback to defaults
  const seoTitle = title || siteConfig.title;
  const seoDescription = description || siteConfig.tagline;
  const seoImage = image || `${baseUrl}img/docusaurus-social-card.jpg`;
  const seoUrl = `${siteConfig.url}${pathname || location.pathname}`;

  return (
    <Head>
      {/* Standard SEO */}
      <title>{seoTitle}</title>
      <meta name="description" content={seoDescription} />

      {/* Open Graph / Facebook */}
      <meta property="og:type" content={type} />
      <meta property="og:url" content={seoUrl} />
      <meta property="og:title" content={seoTitle} />
      <meta property="og:description" content={seoDescription} />
      <meta property="og:image" content={seoImage} />

      {/* Twitter */}
      <meta property="twitter:card" content="summary_large_image" />
      <meta property="twitter:url" content={seoUrl} />
      <meta property="twitter:title" content={seoTitle} />
      <meta property="twitter:description" content={seoDescription} />
      <meta property="twitter:image" content={seoImage} />

      {/* Additional SEO */}
      <link rel="canonical" href={seoUrl} />
      <meta name="keywords" content="AI, artificial intelligence, book, education, machine learning, deep learning" />
      <meta name="author" content="AI-Native Book Authors" />

      {/* Schema.org for Google */}
      <script type="application/ld+json">
        {JSON.stringify({
          "@context": "https://schema.org",
          "@type": type === 'website' ? "WebSite" : "Article",
          "name": seoTitle,
          "description": seoDescription,
          "url": seoUrl,
          "author": {
            "@type": "Organization",
            "name": "AI-Native Book"
          },
          "publisher": {
            "@type": "Organization",
            "name": "AI-Native Book",
            "logo": {
              "@type": "ImageObject",
              "url": `${siteConfig.url}/img/logo.svg`
            }
          },
          "datePublished": new Date().toISOString(),
          "image": seoImage
        })}
      </script>
    </Head>
  );
};

export default SEOHead;