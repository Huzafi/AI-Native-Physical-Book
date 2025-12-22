# Content Authoring Workflow and Tools for AI-Native Book

## Overview
This document outlines the content authoring workflow and tools for the AI-Native Book with Docusaurus project. It provides guidelines for creating, editing, and managing book content.

## Content Structure

### Directory Structure
```
website/
├── docs/                    # All book content
│   ├── intro.mdx           # Introduction chapter
│   ├── chapter-1/          # First chapter directory
│   │   ├── section-1.mdx   # First section
│   │   ├── section-2.mdx   # Second section
│   │   └── ...
│   ├── chapter-2/          # Second chapter directory
│   │   ├── section-1.mdx
│   │   └── ...
│   └── ...
├── src/
│   ├── components/         # Reusable components
│   └── css/               # Custom styles
├── static/                # Static assets (images, etc.)
└── docusaurus.config.js   # Docusaurus configuration
```

### Content File Naming Convention
- Use kebab-case: `understanding-ai-concepts.mdx`
- Include chapter/section numbers if needed: `01-introduction.mdx`
- Keep names descriptive but concise

## Content Creation Workflow

### 1. Planning Phase
Before creating content:

1. **Outline Creation**:
   - Define chapter objectives
   - Identify key concepts to cover
   - Plan section breakdown
   - Consider interactive elements needed

2. **Content Strategy**:
   - Determine target audience level
   - Identify prerequisite knowledge
   - Plan examples and use cases
   - Consider translation requirements

### 2. Writing Phase

1. **Create the MDX File**:
   ```bash
   # Create new content file
   touch website/docs/chapter-name/section-name.mdx
   ```

2. **Add Frontmatter**:
   ```md
   ---
   title: Section Title
   description: Brief description of the section content
   tags: [ai, machine-learning, concepts]
   sidebar_position: 1
   ---
   ```

3. **Write Content**:
   - Use proper heading hierarchy (h1, h2, h3, etc.)
   - Include relevant code examples
   - Add interactive elements where appropriate
   - Use consistent terminology

### 3. Review Phase
1. Check content for accuracy
2. Verify proper formatting and structure
3. Test interactive elements
4. Review for accessibility
5. Validate cross-references

### 4. Publishing Phase
1. Update sidebar navigation
2. Run build to verify no errors
3. Test locally before deployment
4. Commit and push changes

## Content Authoring Tools

### 1. Markdown/MDX Guidelines

#### Basic Formatting
```md
# Chapter Title (h1 - only one per page)
## Section Title (h2)
### Subsection Title (h3)

**Bold text** and *italic text*

[Link text](/path/to/page)

![Alt text](/path/to/image.png)
```

#### Code Blocks
```md
// Code with syntax highlighting
import React from 'react';

function Component() {
  return <div>Hello World</div>;
}
```

#### Admonitions (Callouts)
```md
:::note
This is a note admonition.
:::

:::tip
This is a tip admonition.
:::

:::caution
This is a caution admonition.
:::

:::danger
This is a danger admonition.
:::
```

#### Interactive Elements
```md
<!-- Expandable section -->
<details>
<summary>Detailed Explanation</summary>

More detailed content here...

</details>

<!-- Using custom components -->
<ExpandableSection title="Advanced Concepts">
Detailed content that can be expanded/collapsed
</ExpandableSection>
```

### 2. Image Guidelines
- Store images in `static/img/` directory
- Use descriptive filenames
- Include alt text for accessibility
- Optimize images for web (compress where possible)

### 3. Cross-References
```md
[Link to another page](./relative-path.mdx)
[Link to specific section](./page.mdx#section-id)
```

## Authoring Best Practices

### 1. Writing Style
- Use clear, concise language
- Write for the target audience level
- Maintain consistent terminology
- Use active voice when possible
- Break up long paragraphs

### 2. Accessibility
- Include descriptive alt text for images
- Use proper heading hierarchy
- Ensure sufficient color contrast
- Use semantic HTML elements
- Test with screen readers when possible

### 3. SEO Considerations
- Write descriptive titles and meta descriptions
- Use relevant keywords naturally
- Include internal links to related content
- Optimize image file names and alt text

### 4. Internationalization (i18n)
- Consider translation requirements
- Use simple sentence structures
- Avoid idioms and culture-specific references
- Plan for text expansion/reduction in translations

## Content Management

### 1. Version Control Workflow
```bash
# Create a new branch for content work
git checkout -b content/new-chapter

# Add and commit your changes
git add website/docs/new-content.mdx
git commit -m "Add new chapter: Understanding AI Concepts"

# Push and create a pull request
git push origin content/new-chapter
```

### 2. Sidebar Navigation
Update `website/sidebars.js` to include new content:

```js
module.exports = {
  docs: [
    {
      type: 'category',
      label: 'Chapter 1: Introduction',
      items: [
        'intro',
        'chapter-1/section-1',
        'chapter-1/section-2',
      ],
    },
    // Add new chapters here
  ],
};
```

### 3. Content Indexing
After adding new content, run the indexing script:

```bash
cd backend
python -m scripts.index_content
```

## Quality Assurance

### 1. Content Checklist
- [ ] Title and metadata are complete
- [ ] Content follows proper structure
- [ ] All links are functional
- [ ] Images load correctly
- [ ] Code examples are accurate
- [ ] Interactive elements work properly
- [ ] Content is accessible
- [ ] Grammar and spelling are correct

### 2. Technical Validation
```bash
# Build the site to check for errors
cd website
npm run build

# Test locally
npm start
```

### 3. Preview and Test
- Review content in different browsers
- Test on mobile devices
- Verify all interactive elements work
- Check search functionality with new content

## Translation Preparation

### 1. Content Structure for Translation
- Use simple, clear language
- Avoid complex sentence structures
- Minimize culture-specific references
- Consider text expansion in other languages

### 2. Translation Markers
```md
<!-- TRANSLATION_NOTE: This concept may need explanation in other languages -->
```

## Automation Tools

### 1. Content Validation Script
Create a script to validate content:

```bash
#!/bin/bash
# validate-content.sh

# Check for broken links
npx markdown-link-check "**/*.mdx"

# Check for missing alt text in images
grep -r "!\[.*\](.*)" website/docs/ --include="*.mdx"

# Check for proper heading structure
# (Implementation would depend on specific validation needs)
```

### 2. Build Process Integration
Add content validation to the build process:

```json
{
  "scripts": {
    "validate-content": "node scripts/validate-content.js",
    "build": "npm run validate-content && docusaurus build",
  }
}
```

## Team Collaboration

### 1. Content Review Process
- Assign content reviewers for each chapter
- Use pull requests for content changes
- Establish review timelines
- Document feedback and revisions

### 2. Style Guide
Maintain a consistent style across all content:
- Terminology consistency
- Formatting standards
- Voice and tone guidelines
- Example and code style

## Maintenance

### 1. Regular Updates
- Review content for accuracy periodically
- Update outdated information
- Refresh examples and references
- Improve based on user feedback

### 2. Content Audit
- Verify all links and references
- Check search functionality
- Review analytics for content usage
- Assess translation needs

## Troubleshooting

### Common Issues
1. **Content not appearing**: Check sidebar configuration
2. **Broken links**: Verify relative paths are correct
3. **Build errors**: Check for syntax errors in MDX files
4. **Images not loading**: Verify paths in static directory

### Quick Fixes
- Clear Docusaurus cache: `npx docusaurus clear`
- Rebuild: `npm run build`
- Check logs for specific error messages

---

**Document Version**: 1.0
**Last Updated**: [Current Date]
**Next Review**: [Date + 3 months]