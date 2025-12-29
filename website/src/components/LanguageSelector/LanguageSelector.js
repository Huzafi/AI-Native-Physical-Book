import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import styles from './LanguageSelector.module.css';

const LanguageSelector = ({ onLanguageChange, currentLanguage = 'en' }) => {
  const [selectedLanguage, setSelectedLanguage] = useState(currentLanguage);
  const [showDropdown, setShowDropdown] = useState(false);

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'ur', name: 'اردو' }  // Urdu
  ];

  // Update selected language when prop changes
  useEffect(() => {
    setSelectedLanguage(currentLanguage);
  }, [currentLanguage]);

  const handleLanguageSelect = (languageCode) => {
    setSelectedLanguage(languageCode);
    setShowDropdown(false);

    // Notify parent component of language change
    if (onLanguageChange) {
      onLanguageChange(languageCode);
    }
  };

  const currentLanguageName = languages.find(lang => lang.code === selectedLanguage)?.name || 'English';

  return (
    <div className={styles.languageSelector}>
      <button
        className={styles.selectorButton}
        onClick={() => setShowDropdown(!showDropdown)}
        aria-label="Select language"
        aria-haspopup="true"
        aria-expanded={showDropdown}
      >
        <span className={styles.selectedLanguage}>{currentLanguageName}</span>
        <span className={clsx(styles.arrow, { [styles.arrowOpen]: showDropdown })}>▼</span>
      </button>

      {showDropdown && (
        <div className={styles.dropdown}>
          <ul className={styles.languageList}>
            {languages.map((language) => (
              <li key={language.code} className={styles.languageItem}>
                <button
                  className={clsx(styles.languageButton, {
                    [styles.active]: selectedLanguage === language.code
                  })}
                  onClick={() => handleLanguageSelect(language.code)}
                  dir={language.code === 'ur' ? 'rtl' : 'ltr'}
                >
                  {language.name}
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default LanguageSelector;