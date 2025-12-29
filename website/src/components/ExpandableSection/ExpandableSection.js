import React, { useState } from 'react';
import clsx from 'clsx';
import styles from './ExpandableSection.module.css';

const ExpandableSection = ({ title, children, defaultOpen = false }) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  const toggleOpen = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className={clsx('expandable-section', styles.expandableSection)}>
      <button
        className={clsx('expandable-section-header', styles.header, {
          [styles.headerOpen]: isOpen,
        })}
        onClick={toggleOpen}
        aria-expanded={isOpen}
        aria-controls="expandable-section-content"
      >
        <span className={styles.title}>{title}</span>
        <span className={clsx('expandable-section-arrow', styles.arrow, {
          [styles.arrowOpen]: isOpen,
        })}>
          ▼
        </span>
      </button>
      <div
        id="expandable-section-content"
        className={clsx('expandable-section-content', styles.content, {
          [styles.contentOpen]: isOpen,
        })}
        style={{
          maxHeight: isOpen ? '1000px' : '0',
          overflow: 'hidden',
          opacity: isOpen ? 1 : 0,
        }}
      >
        <div className={styles.contentInner}>
          {children}
        </div>
      </div>
    </div>
  );
};

export default ExpandableSection;