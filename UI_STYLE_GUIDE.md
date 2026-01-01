# Tailor UI Style Guide

Design principles and patterns for building consistent, minimal UIs across the Tailor project.

## Core Philosophy

**Ultra Minimal, Dense, Developer-First**
- Dark theme with subtle accents
- No dependencies (no frameworks, no external CSS)
- Monospace fonts preferred
- Fast to load, fast to understand
- Testing UIs prioritize functionality over polish

## Design Principles

### 1. **Minimalism First**
- Remove everything unnecessary
- Use browser defaults where possible
- Add styling only when it improves usability

### 2. **Consistency**
- Reuse patterns across different UIs
- Standard spacing, sizing, typography
- Predictable interaction patterns

### 3. **Accessibility**
- Semantic HTML
- Proper labels and ARIA where needed
- Keyboard navigation support
- Readable contrast ratios

## Typography

### Fonts
```css
font-family: 'JetBrains Mono', 'Fira Code', monospace, system-ui;  /* Primary */
font-family: monospace;  /* Fallback */
```
**Note:** Monospace fonts are preferred for developer UIs. System will fallback to available fonts.

### Scale (Dense)
```css
h1: 1.3rem    /* Page title */
h2: 1.1rem    /* Section headers */
body: 0.9rem  /* Default text */
small: 0.85rem /* Labels, metadata */
code: 0.8rem  /* Monospace content */
```

### Line Height
```css
line-height: 1.4;  /* Dense for developers */
```

## Colors

### Base Palette (Dark Mode)
```css
--bg: #0a0a0a;          /* Primary background */
--bg-elevated: #1a1a1a; /* Inputs, cards */
--bg-hover: #1a1a1a;    /* Interactive hover */

--text: #e0e0e0;        /* Primary text */
--text-muted: #888;     /* Labels, secondary */
--text-dim: #555;       /* Timestamps, metadata */

--border: #222;         /* Subtle borders */
--border-strong: #333;  /* Input borders */

--accent: #00d4ff;      /* Primary accent (cyan) */
--accent-dim: rgba(0,212,255,0.3); /* Accent subtle */
```

### Semantic Colors
```css
--success: #00ff88;     /* Success text */
--success-bg: #0d2818;  /* Success background */
--error: #ff6666;       /* Error text */
--error-bg: #2a0d0d;    /* Error background */
```

### Usage
- Dark backgrounds with light text
- Cyan accent (#00d4ff) for interactive elements
- Success = green, Error = red
- Minimal color usage overall

## Layout

### Container
```css
max-width: 900px;       /* Dense layout */
margin: 0 auto;         /* Center content */
padding: 15px;          /* Compact spacing */
```

### Spacing Scale (Dense)
```css
XS: 3px    /* Tight spacing */
S:  8px    /* Related elements */
M:  15px   /* Sections */
L:  30px   /* Major sections */
```

### Sections
```css
.section {
    margin-bottom: 15px;
    padding-bottom: 15px;
    border-bottom: 1px solid #222;
}
.section:last-child {
    border-bottom: none;
}
```

## Components

### Buttons
```css
button {
    padding: 6px 14px;
    border: 1px solid #00d4ff;
    background: #0a0a0a;
    color: #00d4ff;
    border-radius: 3px;
    cursor: pointer;
    font-size: 0.9rem;
}
button:hover {
    background: #1a1a1a;
    box-shadow: 0 0 8px rgba(0,212,255,0.3);
}
button:disabled {
    opacity: 0.3;
    cursor: not-allowed;
    border-color: #333;
    color: #555;
}
```

**Usage:**
- Primary action: Default button style
- Secondary actions: Same style (no hierarchy needed for testing UIs)
- Destructive: Add red border/text if needed

### Form Elements
```css
input, textarea, select {
    width: 100%;
    padding: 6px 8px;
    background: #1a1a1a;
    border: 1px solid #333;
    border-radius: 3px;
    color: #e0e0e0;
    font-family: inherit;
    font-size: 0.9rem;
}
input:focus {
    outline: none;
    border-color: #00d4ff;
}
```

### Labels
```css
label {
    display: block;
    margin-bottom: 3px;
    font-size: 0.85rem;
    color: #888;
}
```

### Status Indicators
```css
.status {
    padding: 6px 8px;
    background: #1a1a1a;
    border: 1px solid #333;
    border-radius: 3px;
    font-size: 0.85rem;
}
.status.connected { 
    background: #0d2818; 
    border-color: #00d4ff; 
    color: #00ff88; 
}
.status.error { 
    background: #2a0d0d; 
    border-color: #ff4444; 
    color: #ff6666; 
}
```

### Log/Console Output
```css
.log {
    font-family: monospace;
    font-size: 0.8rem;
    max-height: 350px;
    overflow-y: auto;
    background: #0f0f0f;
    padding: 8px;
    border: 1px solid #222;
    border-radius: 3px;
}
```

## Interaction Patterns

### Connection Status
- Always show connection state clearly
- Use background color for at-a-glance status
- Disable actions when disconnected

### Form Submission
- Support Enter key on text inputs
- Clear inputs after successful submission (when appropriate)
- Show feedback immediately

### Logging
- Show timestamps for all log entries
- Use different text colors for different log types
- Auto-scroll to latest entry
- Provide clear log button

## File Structure

### Minimal Single-File Pattern
For testing/utility UIs, use single HTML file:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tool Name</title>
    <style>
        /* Inline CSS - all styles in one place */
    </style>
</head>
<body>
    <!-- HTML content -->
    <script>
        // Inline JS - all logic in one place
    </script>
</body>
</html>
```

**Benefits:**
- Single file = easy to distribute
- No build process
- Open directly in browser
- Self-contained

## JavaScript Patterns

### Minimal WebSocket Client
```javascript
let ws = null;
let id = 0;
const pending = new Map();

function connect(port) {
    ws = new WebSocket(`ws://localhost:${port}`);
    ws.onopen = () => { /* update UI */ };
    ws.onmessage = (e) => {
        const data = JSON.parse(e.data);
        // Handle response/event
        if (data.id && pending.has(data.id)) {
            pending.get(data.id)(data);
            pending.delete(data.id);
        }
    };
}

function req(method, params = {}) {
    const msg = { jsonrpc: "2.0", id: ++id, method, params };
    ws.send(JSON.stringify(msg));
    return new Promise(resolve => pending.set(id, resolve));
}
```

### State Management
- Keep it simple: global variables are fine for testing UIs
- Update DOM directly
- No reactive frameworks needed

## Common Layouts

### Vertical Sections
Single column, stacked sections (default for most testing UIs)

```
┌─────────────────────┐
│ Title               │
├─────────────────────┤
│ Connection          │
├─────────────────────┤
│ Input Form          │
├─────────────────────┤
│ Actions             │
├─────────────────────┤
│ Output/Log          │
└─────────────────────┘
```

### Split View
For UIs needing side-by-side content

```css
.split {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}
```

## Anti-Patterns

❌ **Avoid:**
- CSS frameworks (Bootstrap, Tailwind, etc.)
- JavaScript frameworks (React, Vue, etc.)
- External dependencies
- Build steps
- Animations for testing UIs
- Overly complex state management
- Custom fonts from CDN
- Excessive styling

✅ **Prefer:**
- Vanilla HTML/CSS/JS
- System fonts
- Single-file architecture
- Direct DOM manipulation
- Browser defaults
- Inline styles and scripts

## Testing UI Checklist

Before finalizing a testing UI:

- [ ] Works without build process
- [ ] Single HTML file (or minimal files)
- [ ] Uses system fonts only
- [ ] No external dependencies
- [ ] Clear connection status
- [ ] Disabled states for unavailable actions
- [ ] Keyboard shortcuts for common actions
- [ ] Log/console for debugging
- [ ] Responsive (works at different widths)
- [ ] Accessible (keyboard navigation, labels)

## Examples

- `vault.html` - Minimal testing UI for vault WebSocket operations
- `index.html` - Simple launcher UI

## Future Considerations

If Tailor grows beyond testing UIs to production UIs:

1. **Create separate style guide** for production UIs
2. **Consider design system** (shared components, tokens)
3. **Add branding** (colors, logo, typography)
4. **Polish interactions** (transitions, animations)
5. **Accessibility audit** (WCAG compliance)

For now, keep it minimal and functional.
