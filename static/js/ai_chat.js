// AI Chat Widget Logic
document.addEventListener('DOMContentLoaded', () => {
    const widget = {
        toggle: document.getElementById('aiChatToggle'),
        window: document.getElementById('aiChatWindow'),
        close: document.getElementById('aiChatClose'),
        messages: document.getElementById('aiChatMessages'),
        input: document.getElementById('aiChatInputField'),
        sendBtn: document.getElementById('aiChatSend'),
        isOpen: false,

        init() {
            if (!this.toggle) return;

            this.toggle.addEventListener('click', () => this.toggleChat());
            this.close.addEventListener('click', () => this.toggleChat());
            this.sendBtn.addEventListener('click', () => this.sendMessage());

            this.input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') this.sendMessage();
            });
        },

        toggleChat() {
            this.isOpen = !this.isOpen;
            this.window.style.display = this.isOpen ? 'flex' : 'none';
            if (this.isOpen) {
                this.input.focus();
                this.scrollToBottom();
            }
        },

        scrollToBottom() {
            this.messages.scrollTop = this.messages.scrollHeight;
        },

        addMessage(text, sender) {
            const div = document.createElement('div');
            div.className = `ai-message ${sender}-message`;

            // Convert newlines to <br> for AI responses
            if (sender === 'ai') {
                div.innerHTML = text.replace(/\n/g, '<br>');
            } else {
                div.textContent = text;
            }

            this.messages.appendChild(div);
            this.scrollToBottom();
        },

        addTypingIndicator() {
            const div = document.createElement('div');
            div.className = 'ai-typing';
            div.id = 'aiTyping';
            div.innerHTML = '<span></span><span></span><span></span>';
            this.messages.appendChild(div);
            this.scrollToBottom();
        },

        removeTypingIndicator() {
            const el = document.getElementById('aiTyping');
            if (el) el.remove();
        },

        async sendMessage() {
            const text = this.input.value.trim();
            if (!text) return;

            // User message
            this.addMessage(text, 'user');
            this.input.value = '';

            // AI processing
            this.addTypingIndicator();

            try {
                const response = await fetch('/ai/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });

                const data = await response.json();
                this.removeTypingIndicator();

                if (data.success) {
                    this.addMessage(data.response, 'ai');
                } else {
                    this.addMessage('Sorry, I encountered an error: ' + (data.error || 'Unknown error'), 'ai');
                }
            } catch (error) {
                this.removeTypingIndicator();
                this.addMessage('Connection error. Please check your internet.', 'ai');
                console.error(error);
            }
        }
    };

    widget.init();
});
