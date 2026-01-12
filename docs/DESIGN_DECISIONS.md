# Design Decisions Log

This document tracks key architectural decisions, their context, and their status.

## 001. Plugin UI HTML/CSS Injection

**Date:** 2026-01-12
**Status:** ✅ Decided

### Context
We investigated the extent of control plugins have over the application's UI, specifically regarding HTML structure and CSS styling, to determine if they can (and should) be allowed to edit the page directly.

### Current Implementation
The application allows plugins to return raw HTML content via commands (e.g., `get_ui`), which the frontend (`vault.html`) injects into the DOM.
- **Mechanism:** Javascript `innerHTML` and `Range.createContextualFragment`.
- **Scope:** Global. Plugins are injected into the main document flow.

### Implications
1.  **Global CSS Editing:** A plugin can inject a `<style>` tag. Because there is no encapsulation (like Shadow DOM), these styles apply globally to the entire application.
2.  **Script Execution:** Plugins can inject `<script>` tags which are executed with the same privileges as the main application.

### Decision Analysis

| Strategy | Pros | Cons |
| :--- | :--- | :--- |
| **Fully Open** (Current) | Maximum flexibility. Plugins can implement themes, global hotkeys, and complex interactive UIs without friction. | **High Risk** in an open ecosystem. Malicious plugins can break the layout or compromise security. |
| **Shadow DOM** | Isolates plugin CSS. Prevents plugins from breaking the app's layout styles. | More complex implementation. Harder for plugins to "thematically" integrate. |

### Conclusion
**Decision:** Keep the current **Fully Open** architecture.
**Rationale:** Plugins will be vetted and approved by the core team before distribution. Therefore, we prioritize maximum flexibility and creative control for plugin developers over sandboxing. The security risk is mitigated by the review process.
