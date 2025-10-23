# Markdown Documentation Tasks

## Overview

This document tracks tasks related to maintaining and improving Markdown documentation style and consistency across the repository.

## Current Status

### Completed
- ✅ Created style guide (`decisions.md`)
- ✅ Standardized `ansible.md` formatting
  - Fixed heading capitalization (Title Case)
  - Removed nested details blocks
  - Standardized details/summary structure
  - Fixed typos (SNIPETS→Snippets, cofigure→configure, ansibel_password→ansible_password)
  - Added consistent syntax highlighting
  - Unified Vault Lookups section structure
- ✅ Standardized `argo-cd.md` formatting
  - Fixed heading capitalization (Title Case)
  - Standardized all details/summary blocks
  - Fixed typo (BULD→Build)
  - Corrected syntax highlighting (bash→dockerfile for Dockerfile)
  - Consistent structure across all sections
- ✅ Added `.task/` to `.gitignore`

## Pending Tasks

### High Priority

- [ ] **Review and standardize all Markdown files in `/docs`**
  - [x] `ansible.md` ✅ Completed 2025-10-23
  - [x] `argo-cd.md` ✅ Completed 2025-10-23
  - [ ] `argo-events.md`
  - [ ] `argo-workflows.md`
  - [ ] `certificates.md`
  - [ ] `cilium.md`
  - [ ] `cloud.md`
  - [ ] `containerization.md`
  - [ ] `crossplane.md`
  - [ ] `dagger.md`
  - [ ] `elastic.md`
  - [ ] `flux.md`
  - [ ] `git.md`
  - [ ] `github.md`
  - [ ] `gitlab.md`
  - [ ] `golang-operator.md`
  - [ ] `golang.md`
  - [ ] `helm.md`
  - [ ] `hugo.md`
  - [ ] `kcl.md`
  - [ ] `kubernetes.md`
  - [ ] `kustomize.md`
  - [ ] `linux.md`
  - [ ] `minio.md`
  - [ ] `packer.md`
  - [ ] `proxmox.md`
  - [ ] `python.md`
  - [ ] `rancher.md`
  - [ ] `react.md`
  - [ ] `README.md`
  - [ ] `redis.md`
  - [ ] `taskfile.md`
  - [ ] `tekton.md`
  - [ ] `terraform.md`
  - [ ] `vault.md`
  - [ ] `velero.md`
  - [ ] `yq.md`

### Medium Priority

- [ ] **Add markdownlint configuration**
  - [ ] Create `.markdownlint.json`
  - [ ] Configure rules to match style guide
  - [ ] Add to CI/CD pipeline (optional)

- [ ] **Update README.md**
  - [ ] Add link to style guide
  - [ ] Document markdown conventions
  - [ ] Add contribution guidelines

- [ ] **Create templates**
  - [ ] New documentation template
  - [ ] Tool/technology documentation template
  - [ ] Tutorial template

### Low Priority

- [ ] **Automation**
  - [ ] Script to check heading capitalization
  - [ ] Script to validate details block structure
  - [ ] Pre-commit hooks for markdown validation

- [ ] **Documentation**
  - [ ] Add examples gallery
  - [ ] Create before/after comparison
  - [ ] Document common patterns

## Standardization Checklist

For each Markdown file, verify:

### Structure
- [ ] Main title (H1) is simple and clear
- [ ] Section titles (H2) use Title Case
- [ ] Subsection titles (H3+) use Title Case
- [ ] Major sections use `<details><summary><b>Title</b></summary>` structure
- [ ] No nested `<details>` blocks (use `###` for subsections inside)
- [ ] Consistent section ordering (Installation → Usage → Advanced → Troubleshooting)

### Formatting
- [ ] All code blocks have language identifiers (```bash, ```yaml, etc.)
- [ ] Inline code uses backticks (`command`, `file.yaml`)
- [ ] Lists use `-` for bullets consistently
- [ ] No extra whitespace before `</details>`
- [ ] Bold used for emphasis (`**important**`)
- [ ] Italic used for placeholders (`_<your-value>_`)

### Content
- [ ] No ALL CAPS in headings (except acronyms like EDA, K8s)
- [ ] Descriptive link text (not "click here")
- [ ] Comments in code blocks use proper syntax
- [ ] Examples are complete and runnable
- [ ] Typos corrected
- [ ] Grammar checked

### Consistency
- [ ] Heading style matches other docs
- [ ] Code block style matches other docs
- [ ] Section naming matches conventions
- [ ] Overall structure similar to exemplar docs (e.g., `ansible.md`)

## Migration Strategy

### Phase 1: Critical Documentation (Week 1-2)
Focus on most-accessed files:
1. `kubernetes.md`
2. `terraform.md`
3. `helm.md`
4. `flux.md`
5. `argo-cd.md`

### Phase 2: Tool-Specific Documentation (Week 3-4)
Update tool-specific docs:
1. `dagger.md`
2. `tekton.md`
3. `vault.md`
4. `crossplane.md`
5. `kustomize.md`

### Phase 3: Supporting Documentation (Week 5-6)
Complete remaining files:
1. Cloud-related: `cloud.md`, `proxmox.md`
2. Language-specific: `golang.md`, `python.md`, `react.md`
3. Infrastructure: `cilium.md`, `certificates.md`, `minio.md`
4. Others: `git.md`, `github.md`, `gitlab.md`, `linux.md`

### Phase 4: Automation & Templates (Week 7+)
1. Implement linting rules
2. Create templates for new docs
3. Add CI/CD checks
4. Update contribution guidelines

## Common Issues Found

### Heading Issues
- ❌ `## INSTALLATION` → ✅ `## Installation`
- ❌ `<details><summary><b>CUSTOM INVENTORY W/ MOLECULE</b></summary>` → ✅ `<details><summary><b>Custom Inventory with Molecule</b></summary>`
- ❌ `### CLONE OR SWITCH TO EXISTING REMOTE BRANCH` → ✅ `### Clone or Switch to Existing Remote Branch`

### Structure Issues
- ❌ Nested details blocks → ✅ Single details block with `###` subsections
- ❌ Extra whitespace before `</details>` → ✅ No extra whitespace
- ❌ Content outside details blocks → ✅ Content wrapped in details

### Code Block Issues
- ❌ No language identifier → ✅ Always specify language (```bash, ```yaml)
- ❌ Incorrect syntax highlighting → ✅ Use correct language identifier
- ❌ Inconsistent indentation → ✅ Consistent 2 or 4 space indentation

### Typos & Errors
- `SNIPETS` → `Snippets`
- `cofigure` → `configure`
- `ansibel_password` → `ansible_password`
- `enviornment` → `environment`
- `prevoius` → `previous`
- `currenlty` → `currently`
- `BULD` → `Build`

## Common Fixes Applied

### In ansible.md
- Fixed 62+ heading capitalization issues
- Removed nested details blocks
- Standardized all code block language identifiers
- Fixed 7 typos
- Unified Vault Lookups section (removed 18 lines of redundant structure)

### In argo-cd.md
- Fixed 30+ heading capitalization issues
- Standardized all details/summary blocks
- Changed Dockerfile syntax highlighting from `bash` to `dockerfile`
- Fixed typo: "BULD ENV VAR" → "Build Environment Variables"
- Improved readability across all sections

## Progress Tracking

| File | Status | Last Updated | Notes |
|------|--------|--------------|-------|
| `ansible.md` | ✅ Complete | 2025-10-23 | Fully standardized, all issues fixed |
| `argo-cd.md` | ✅ Complete | 2025-10-23 | Title Case, syntax highlighting corrected |
| Other files | ⏳ Pending | - | Awaiting review |

## Review Process

1. **Read through** file to understand content
2. **Check structure** against style guide
3. **Fix headings** (Title Case, no ALL CAPS)
4. **Standardize details blocks** (one per major section)
5. **Add syntax highlighting** to all code blocks
6. **Remove nested details** (use `###` instead)
7. **Fix typos** and grammar
8. **Test examples** (if applicable)
9. **Commit changes** with descriptive message
10. **Update tracking table** above

## Commit Message Format

When updating documentation:

```
docs(<file>): <brief description>

- Fix heading capitalization
- Standardize details blocks
- Add syntax highlighting
- Fix typos: <list specific typos>
- Other improvements
```

Examples:
```
docs(ansible): fix errors and standardize structure

- Fix title and heading capitalization (Title Case)
- Fix typos: SNIPETS→Snippets, cofigure→configure
- Standardize details tags (remove extra whitespace)
- Improve heading consistency across all sections
```

```
docs(ansible): restructure Vault Lookups section to match document schema

- Wrap entire Vault Lookups section in single details/summary block
- Remove nested details tags for consistency
- Use bold headings (###) instead of nested details blocks
- Consistent with other sections in document
```

## Resources

- Style Guide: [decisions.md](./decisions.md)
- Markdown Syntax: [GitHub Markdown Guide](https://guides.github.com/features/mastering-markdown/)
- markdownlint: [Rules Reference](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
- VS Code Extension: [Markdown All in One](https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one)

## Questions & Decisions

### Open Questions
- Should we enforce max line length? (Current: No strict limit)
- Should we use reference-style links for external documentation? (Current: No)
- Should we add table of contents to long documents? (Current: Optional)

### Decided
- ✅ Title Case for all H2+ headings
- ✅ One details block per major topic (no nesting)
- ✅ Always specify language in code blocks
- ✅ Use `-` for unordered lists
- ✅ No extra whitespace in details blocks
- ✅ Subsections inside details use `###` headings
