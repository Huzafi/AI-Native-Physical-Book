import React from 'react';
import clsx from 'clsx';
import styles from './Highlight.module.css';

const Highlight = ({ text, query, className }) => {
  if (!text || !query) {
    return <span className={className}>{text}</span>;
  }

  // Escape special regex characters in the query
  const escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const regex = new RegExp(`(${escapedQuery})`, 'gi');

  const parts = text.split(regex);

  return (
    <span className={clsx(styles.highlightContainer, className)}>
      {parts.map((part, index) =>
        regex.test(part) ? (
          <mark key={index} className={styles.highlighted}>
            {part}
          </mark>
        ) : (
          <span key={index}>{part}</span>
        )
      )}
    </span>
  );
};

export default Highlight;