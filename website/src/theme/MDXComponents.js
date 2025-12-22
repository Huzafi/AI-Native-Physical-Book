import React from 'react';
import MDXComponents from '@theme-original/MDXComponents';
import ExpandableSection from '@site/src/components/ExpandableSection/ExpandableSection';
import VisualDiagrams from '@site/src/components/VisualDiagrams/VisualDiagrams';
import Callout from '@site/src/components/Callouts/Callouts';

// Custom MDX components for the AI-Native Book
export default {
  ...MDXComponents,
  ExpandableSection,
  VisualDiagrams,
  Callout,
  // Aliases for different callout types
  Note: (props) => <Callout type="note" {...props} />,
  Tip: (props) => <Callout type="tip" {...props} />,
  Caution: (props) => <Callout type="caution" {...props} />,
  Danger: (props) => <Callout type="danger" {...props} />,
  Success: (props) => <Callout type="success" {...props} />,
};