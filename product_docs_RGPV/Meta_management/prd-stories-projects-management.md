# Managing PRD, User Stories, and GitHub Projects

## Product Requirements Document (PRD) and User Stories

### Recommendation:
Store these documents in both repositories, but with different levels of detail.

1. Private Repository:
   - Full, detailed PRD
   - Complete set of user stories
   - Any sensitive or proprietary information

2. Public Repository:
   - Simplified version of the PRD (remove sensitive details)
   - General user stories (omit any that reveal proprietary features)

### Implementation:
1. Create a `docs` folder in each repository:
   ```
   private_resume_generator/
   ├── docs/
   │   ├── PRD.md
   │   └── UserStories.md
   └── ...

   public_resume_generator/
   ├── docs/
   │   ├── PRD.md
   │   └── UserStories.md
   └── ...
   ```

2. Maintain two versions of each document:
   - Full versions in the private repository
   - Sanitized versions in the public repository

## GitHub Projects

### Recommendation:
Set up GitHub Projects in your private repository.

### Rationale:
1. Privacy: Keeps your full project planning and progress private.
2. Flexibility: Allows you to reference both public and private issues/code.
3. Comprehensive View: Provides a complete overview of your project.

### Implementation:
1. Go to your private repository on GitHub.
2. Click on the "Projects" tab.
3. Click "New project".
4. Choose a template (e.g., Kanban).
5. Set up columns: "To Do", "In Progress", "Review", "Done".
6. Add issues and notes to your project board.

### Managing Public Aspects:
- For features or issues that are safe to be public, create them in your public repository.
- You can still reference these public issues in your private GitHub Project.

## Best Practices:
1. Regular Review: Periodically review public documents to ensure no sensitive information is exposed.
2. Consistency: Keep the structure of documents similar between repositories for easier management.
3. Clear Labeling: In the public repo, clearly state that it's a partial representation of the project.
4. Version Control: Use Git to track changes in your documentation, just like your code.
