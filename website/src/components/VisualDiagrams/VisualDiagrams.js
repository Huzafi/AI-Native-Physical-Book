import React from 'react';
import clsx from 'clsx';
import styles from './VisualDiagrams.module.css';

const VisualDiagrams = ({ type, data, title, caption }) => {
  // This component can render different types of diagrams based on the 'type' prop
  // For now, we'll implement a basic visualization framework

  const renderDiagram = () => {
    switch (type) {
      case 'flowchart':
        return <Flowchart data={data} />;
      case 'comparison':
        return <ComparisonChart data={data} />;
      case 'timeline':
        return <Timeline data={data} />;
      default:
        return <div className={styles.defaultDiagram}>Diagram type not supported: {type}</div>;
    }
  };

  return (
    <div className={clsx('visual-diagram-container', styles.visualDiagramContainer)}>
      {title && <h4 className={styles.title}>{title}</h4>}
      <div className={styles.diagram}>
        {renderDiagram()}
      </div>
      {caption && <p className={styles.caption}>{caption}</p>}
    </div>
  );
};

// Basic flowchart component
const Flowchart = ({ data }) => {
  return (
    <div className="mermaid">
      {data && typeof data === 'string' ? data : 'graph TD;\n    A[Start] --> B{Decision};\n    B -->|Yes| C[Action];\n    B -->|No| D[End];'}
    </div>
  );
};

// Basic comparison chart component
const ComparisonChart = ({ data }) => {
  if (!data || !Array.isArray(data) || data.length === 0) {
    return <div>No comparison data provided</div>;
  }

  return (
    <div className={styles.comparisonChart}>
      {data.map((item, index) => (
        <div key={index} className={styles.comparisonItem}>
          <h5>{item.title}</h5>
          <div className={styles.barContainer}>
            <div
              className={styles.bar}
              style={{ width: `${item.value}%` }}
            >
              {item.value}%
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

// Basic timeline component
const Timeline = ({ data }) => {
  if (!data || !Array.isArray(data) || data.length === 0) {
    return <div>No timeline data provided</div>;
  }

  return (
    <div className={styles.timeline}>
      {data.map((item, index) => (
        <div key={index} className={styles.timelineItem}>
          <div className={styles.timelineDot}></div>
          <div className={styles.timelineContent}>
            <h5>{item.title}</h5>
            <p>{item.description}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default VisualDiagrams;