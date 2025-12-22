import React from 'react';
import clsx from 'clsx';
import styles from './LoadingSpinner.module.css';

const LoadingSpinner = ({ size = 'medium', label = 'Loading...', showLabel = true }) => {
  const sizeClass = styles[`spinner${size.charAt(0).toUpperCase() + size.slice(1)}`];

  return (
    <div className={styles.loadingContainer}>
      <div className={clsx(styles.spinner, sizeClass)}>
        <div className={styles.spinnerElement}></div>
        <div className={styles.spinnerElement}></div>
        <div className={styles.spinnerElement}></div>
        <div className={styles.spinnerElement}></div>
      </div>
      {showLabel && <div className={styles.loadingLabel}>{label}</div>}
    </div>
  );
};

export default LoadingSpinner;