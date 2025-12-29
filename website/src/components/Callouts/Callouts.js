import React from 'react';
import clsx from 'clsx';
import styles from './Callouts.module.css';

const Callout = ({ type = 'note', title, children }) => {
  const calloutClasses = clsx(
    'callout',
    styles.callout,
    styles[`callout${type.charAt(0).toUpperCase() + type.slice(1)}`]
  );

  const icon = getIconForType(type);

  return (
    <div className={calloutClasses}>
      <div className={styles.calloutHeader}>
        <span className={styles.calloutIcon}>{icon}</span>
        <span className={styles.calloutTitle}>{title || capitalizeFirstLetter(type)}</span>
      </div>
      <div className={styles.calloutContent}>
        {children}
      </div>
    </div>
  );
};

const getIconForType = (type) => {
  switch (type) {
    case 'note':
      return 'ℹ️';
    case 'tip':
      return '💡';
    case 'caution':
      return '⚠️';
    case 'danger':
      return '🚫';
    case 'success':
      return '✅';
    default:
      return '📌';
  }
};

const capitalizeFirstLetter = (string) => {
  return string.charAt(0).toUpperCase() + string.slice(1);
};

export default Callout;