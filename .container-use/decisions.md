# Markdown Documentation Style Guide - Decisions

## Overview

This document outlines the style and formatting decisions for all Markdown documentation in this repository.

## Heading Capitalization

**Decision**: Use **Title Case** for all headings (H2 and below)

**Rationale**: 
- Provides consistent, professional appearance
- Improves readability and scannability
- Aligns with technical documentation best practices

**Examples**:
```markdown
✅ Good:
## Event-Driven Ansible (EDA)
### Installation Elasticsearch Source Plugin
<details><summary><b>Custom Inventory with Molecule</b></summary>

❌ Bad:
## EVENT-DRIVEN ANSIBLE (EDA)
### INSTALLATION ELASTICSEARCH SOURCE PLUGIN
<details><summary><b>CUSTOM INVENTORY W/ MOLECULE</b></summary>
```

**Exceptions**:
- H1 titles: Can be simple (e.g., `# Ansible`, `# Terraform`)
- Acronyms: Keep as-is (EDA, K8s, CI/CD, SSH)
- Code/command references: Keep lowercase (e.g., `kubectl`, `ansible-playbook`)

## Use of Details/Summary Blocks

**Decision**: Use collapsible `<details><summary>` blocks for all major sections and code examples

**Rationale**:
- Improves document navigation and reduces scrolling
- Allows users to expand only relevant sections
- Keeps main document structure clean and organized
- Better for long documents with multiple examples

**Structure**:
```markdown
## Main Section

<details><summary><b>Descriptive Title in Title Case</b></summary>

### Subsection (if needed)

Content, explanations, code blocks...

</details>
```

**Guidelines**:
1. **One details block per major topic/example**
2. **Use bold (`<b>`) for summary text**
3. **No extra whitespace before `</details>`**
4. **Subsections inside details use `###` headings**
5. **No nested details blocks** (keep flat structure)

**Examples**:
```markdown
✅ Good:
<details><summary><b>Install Kubernetes Tools</b></summary>

```bash
brew install kubectl helm
```

</details>

❌ Bad (nested details):
<details><summary><b>Main Topic</b></summary>

<details><summary><b>Subtopic</b></summary>
...
</details>

</details>

❌ Bad (extra whitespace):
</details>

 </details>
```

## Syntax Highlighting

**Decision**: Always specify language identifier for code blocks

**Rationale**:
- Enables proper syntax highlighting
- Improves code readability
- Makes examples easier to understand and copy

**Supported Languages**:
```markdown
```bash        # Shell commands
```yaml        # YAML files (Ansible, K8s, etc.)
```python      # Python code
```go          # Go code
```dockerfile  # Dockerfiles
```json        # JSON data
```terraform   # Terraform/HCL
```markdown    # Markdown examples
```

**Examples**:
```markdown
✅ Good:
```bash
kubectl get pods -n kube-system
```

```yaml
---
- hosts: localhost
  tasks:
    - debug:
        msg: "Hello World"
```

❌ Bad (no language):
```
kubectl get pods
```

❌ Bad (wrong language):
```python
kubectl get pods
```
```

## Code Block Formatting

**Decision**: Use consistent formatting within code blocks

**Guidelines**:
1. **Comments**: Use native language comment syntax
2. **Indentation**: Maintain consistent indentation (2 or 4 spaces)
3. **Line length**: Keep reasonable (< 100 chars when possible)
4. **Blank lines**: Use sparingly, only for logical separation

**Examples**:
```markdown
✅ Good:
```bash
# Install dependencies
brew install kubectl helm

# Verify installation
kubectl version --client
helm version
```

❌ Bad:
```bash
brew install kubectl helm #install dependencies
kubectl version --client#verify
```
```

## Section Naming Conventions

**Decision**: Use descriptive, consistent section names

**Patterns**:
- Installation/Setup: `Installation`, `Setup`, `Prerequisites`
- Examples: `Example <Description>`, `<Topic> Examples`
- Configuration: `Configuration Options`, `Configuration Reference`
- Troubleshooting: `Troubleshooting`, `Common Issues`
- Advanced: `Advanced Topics`, `Advanced Usage`

**Examples**:
```markdown
✅ Good:
## Installation
<details><summary><b>Example Installation</b></summary>

## Task Snippets
<details><summary><b>Loop Over Dict</b></summary>

## Troubleshooting
<details><summary><b>Common Installation Issues</b></summary>

❌ Bad:
## INSTALL
<details><summary><b>INSTALL EXAMPLE</b></summary>

## TASK-SNIPPETS
<details><summary><b>loop over dict</b></summary>
```

## File Organization

**Decision**: Organize content from simple to complex, general to specific

**Recommended Order**:
1. **Overview/Introduction** (if needed)
2. **Prerequisites/Requirements**
3. **Installation/Setup**
4. **Basic Usage/Examples**
5. **Configuration/Options**
6. **Advanced Topics**
7. **Troubleshooting**
8. **References/Links**

**Within Sections**:
- Simple examples before complex ones
- Common use cases before edge cases
- Quick start before detailed explanations

## Lists and Formatting

**Decision**: Use consistent list formatting

**Guidelines**:
1. **Unordered lists**: Use `-` for bullets
2. **Ordered lists**: Use `1.` notation (auto-numbering)
3. **Nested lists**: Indent with 2 spaces
4. **List spacing**: No blank lines between items (unless item is multi-paragraph)

**Examples**:
```markdown
✅ Good:
- First item
- Second item
  - Nested item
  - Another nested item
- Third item

1. First step
2. Second step
3. Third step

❌ Bad:
* First item

* Second item

- Third item
```

## Inline Code and Emphasis

**Decision**: Use consistent inline formatting

**Guidelines**:
1. **Inline code**: Use backticks for commands, filenames, variables
2. **Bold**: Use `**text**` for emphasis or important terms
3. **Italic**: Use `_text_` sparingly (paths, placeholders)

**Examples**:
```markdown
✅ Good:
Run the `kubectl get pods` command to list all pods.
The configuration file is located at `~/.kube/config`.
Set the **GITHUB_TOKEN** environment variable.
Replace _<your-token>_ with your actual token.

❌ Bad:
Run the kubectl get pods command to list all pods.
The configuration file is located at ~/.kube/config.
Set the GITHUB_TOKEN environment variable.
```

## Links and References

**Decision**: Use descriptive link text, avoid "click here"

**Guidelines**:
1. **External links**: Full URL or descriptive text
2. **Internal links**: Use relative paths
3. **Reference-style links**: For repeated links
4. **Link text**: Descriptive, not generic

**Examples**:
```markdown
✅ Good:
See the [Ansible documentation](https://docs.ansible.com)
Refer to [Installation Guide](#installation)
For more details, see the [KCL module README](../kcl/README.md)

❌ Bad:
Click [here](https://docs.ansible.com)
See [this link](#installation)
[Link](../kcl/README.md)
```

## Version and Date Information

**Decision**: Include version/date information where relevant

**Guidelines**:
1. **Tool versions**: Specify in examples when version-specific
2. **Last updated**: Add date to major documentation updates (optional)
3. **Compatibility**: Note supported versions

**Examples**:
```markdown
✅ Good:
```bash
# Install Kubernetes 1.28+
kubectl version --client
```

**Requirements**:
- Ansible 2.15 or higher
- Python 3.9+

❌ Bad:
```bash
# Install Kubernetes
kubectl version
```
```

## Consistency Across Repository

**Decision**: All Markdown files should follow the same style

**Enforcement**:
1. Use this guide as reference for all documentation
2. Review existing files and update to match style
3. Apply style guide to new documentation
4. Use linting tools where possible (markdownlint)

**Migration Plan**:
- Gradually update existing files
- Prioritize frequently-accessed documentation
- Document changes in commits (e.g., `docs: standardize markdown formatting`)

## Review Checklist

Before committing Markdown documentation, verify:

- [ ] All headings use Title Case (H2+)
- [ ] Major sections use `<details><summary>` blocks
- [ ] All code blocks have language identifiers
- [ ] No nested `<details>` blocks
- [ ] No extra whitespace before `</details>`
- [ ] Inline code uses backticks
- [ ] Lists use consistent formatting (`-` for bullets)
- [ ] Links have descriptive text
- [ ] Section names follow naming conventions
- [ ] Content organized logically (simple → complex)

## Tools and Automation

**Recommended Tools**:
- **markdownlint**: Automated Markdown linting
- **prettier**: Auto-formatting (with Markdown plugin)
- **VS Code extensions**: Markdown All in One, markdownlint

**Configuration** (`.markdownlint.json`):
```json
{
  "MD013": false,
  "MD033": false,
  "MD041": false
}
```
