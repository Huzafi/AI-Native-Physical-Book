import React, { useState, useEffect } from 'react';
import { useLocation } from '@docusaurus/router';
import { translate } from '@docusaurus/Translate';
import clsx from 'clsx';
import LanguageSelector from '../LanguageSelector/LanguageSelector';
import { getContentWithFallback } from '../../utils/translationService';
import styles from './TranslationToggle.module.css';

const TranslationToggle = ({ contentId, title, content }) => {
  const [currentLanguage, setCurrentLanguage] = useState('en');
  const [availableLanguages, setAvailableLanguages] = useState(['en']);
  const [translatedContent, setTranslatedContent] = useState({ title, content });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasTranslation, setHasTranslation] = useState(false);
  const location = useLocation();

  // Extract content ID from the URL if not provided
  useEffect(() => {
    let isMounted = true; // To prevent state updates on unmounted components

    const extractContentId = () => {
      if (contentId) return contentId;

      // Extract from URL path - assuming format like /docs/chapter-1/perception
      const pathParts = location.pathname.split('/').filter(part => part);
      if (pathParts.length >= 2 && pathParts[0] === 'docs') {
        // Combine path parts to form content ID
        return pathParts.slice(1).join('-');
      }
      return null;
    };

    const loadContent = async () => {
      const extractedContentId = extractContentId();
      if (!extractedContentId) return;

      setIsLoading(true);
      setError(null);

      try {
        const result = await getContentWithFallback(
          extractedContentId,
          title,
          content,
          currentLanguage
        );

        if (isMounted) {
          setTranslatedContent({
            title: result.title,
            content: result.content
          });
          setHasTranslation(result.hasTranslation);
        }
      } catch (err) {
        if (isMounted) {
          setError(err.message);
          console.error('Error loading content with fallback:', err);
          // Still show original content on error
          setTranslatedContent({ title, content });
          setHasTranslation(false);
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    };

    loadContent();

    return () => {
      isMounted = false;
    };
  }, [currentLanguage, contentId, title, content, location.pathname]);

  const handleLanguageChange = (languageCode) => {
    setCurrentLanguage(languageCode);
  };

  return (
    <div className={styles.translationContainer}>
      <div className={styles.translationHeader}>
        <LanguageSelector
          currentLanguage={currentLanguage}
          onLanguageChange={handleLanguageChange}
        />

        {isLoading && (
          <div className={styles.loadingIndicator}>
            {translate({ id: 'translation.loading', message: 'Loading translation...' })}
          </div>
        )}

        {error && (
          <div className={styles.errorIndicator}>
            {translate({ id: 'translation.error', message: 'Error loading translation' })}: {error}
          </div>
        )}

        {!hasTranslation && currentLanguage !== 'en' && !isLoading && (
          <div className={styles.fallbackIndicator}>
            {translate({
              id: 'translation.fallback',
              message: 'Translation not available, showing original content'
            })}
          </div>
        )}
      </div>

      <div className={clsx(styles.translationContent, {
        [styles.rtl]: currentLanguage === 'ur'
      })}>
        {translatedContent.content}
      </div>
    </div>
  );
};

export default TranslationToggle;