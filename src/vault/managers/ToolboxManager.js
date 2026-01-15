/**
 * ToolboxManager - Manages the toolbox content area
 */
export class ToolboxManager {
    constructor() {
        this.items = [];
    }

    setContent(html) {
        console.log(`[ToolboxManager] Setting content`);
        const area = document.getElementById('toolbox-area');
        if (area) {
            area.innerHTML = html;
            if (window.lucide) window.lucide.createIcons();
        }
    }

    addItem(html) {
        console.log(`[ToolboxManager] Adding item`);
        const area = document.getElementById('toolbox-area');
        if (area) {
            // If it's the default text, clear it first
            if (area.querySelector('.default-text')) {
                area.innerHTML = '';
            }

            const div = document.createElement('div');
            div.className = 'toolbox-item';

            // Allow html content (inline styles in plugin content are still respected, but container is standardized)
            div.innerHTML = html;
            area.appendChild(div);

            if (window.lucide) window.lucide.createIcons();
        }
    }
}
