// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'preface',
      label: 'Preface',
    },
    {
      type: 'doc',
      id: 'toc',
      label: 'Table of Contents',
    },
    {
      type: 'category',
      label: 'Part I: Foundations of Intelligence',
      collapsed: true,
      items: [
        {
          type: 'doc',
          id: 'chapter-1/index',
          label: 'Chapter 1: Perception',
        },
        {
          type: 'doc',
          id: 'chapter-1/reasoning',
          label: 'Chapter 2: Reasoning',
        }
      ],
    },
    {
      type: 'category',
      label: 'Part II: Embodied Intelligence',
      collapsed: true,
      items: [
        {
          type: 'doc',
          id: 'chapter-2/index',
          label: 'Chapter 3: Physical AI & Humanoids',
        }
      ],
    },
    {
      type: 'category',
      label: 'Part III: Advanced Physical AI Technologies',
      collapsed: true,
      items: [
        {
          type: 'doc',
          id: 'chapter-3/index',
          label: 'Chapter 4: Advanced Physical AI Technologies',
        },
        {
          type: 'doc',
          id: 'chapter-3/advanced-sensor-technologies',
          label: 'Advanced Sensor Technologies',
        },
        {
          type: 'doc',
          id: 'chapter-3/advanced-actuation-systems',
          label: 'Advanced Actuation Systems',
        },
        {
          type: 'doc',
          id: 'chapter-3/neuromorphic-computing',
          label: 'Neuromorphic Computing',
        }
      ],
    },
    {
      type: 'category',
      label: 'Part IV: Humanoid Robotics and Applications',
      collapsed: true,
      items: [
        {
          type: 'doc',
          id: 'chapter-4/index',
          label: 'Chapter 5: Humanoid Robotics and Applications',
        },
        {
          type: 'doc',
          id: 'chapter-4/biomechanics-motion-analysis',
          label: 'Biomechanics and Motion Analysis',
        },
        {
          type: 'doc',
          id: 'chapter-4/humanoid-control-systems',
          label: 'Humanoid Control Systems',
        },
        {
          type: 'doc',
          id: 'chapter-4/humanoid-applications-industry',
          label: 'Applications in Industry',
        }
      ],
    },
    {
      type: 'doc',
      id: 'outline',
      label: 'Section Outline',
    },
  ],
};

module.exports = sidebars;