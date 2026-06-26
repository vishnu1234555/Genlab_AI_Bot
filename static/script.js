document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatHistory = document.getElementById('chat-history');
    const sendBtn = document.getElementById('send-btn');

    // Configure marked to sanitize and format nicely
    marked.setOptions({
        breaks: true,
        gfm: true,
    });

    function appendMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);

        const avatar = document.createElement('div');
        avatar.classList.add('avatar');
        avatar.textContent = sender === 'user' ? 'U' : 'AI';

        const bubble = document.createElement('div');
        bubble.classList.add('bubble');
        
        if (sender === 'user') {
            bubble.textContent = text;
        } else {
            // Parse markdown for AI responses
            bubble.innerHTML = marked.parse(text);
        }

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(bubble);
        
        chatHistory.appendChild(messageDiv);
        scrollToBottom();
    }

    function showTypingIndicator() {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'system', 'typing-msg');
        
        const avatar = document.createElement('div');
        avatar.classList.add('avatar');
        avatar.textContent = 'AI';

        const bubble = document.createElement('div');
        bubble.classList.add('bubble', 'typing-indicator');
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.classList.add('typing-dot');
            bubble.appendChild(dot);
        }

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(bubble);
        chatHistory.appendChild(messageDiv);
        scrollToBottom();
        
        return messageDiv;
    }

    function removeTypingIndicator(indicatorElement) {
        if (indicatorElement && indicatorElement.parentNode) {
            indicatorElement.parentNode.removeChild(indicatorElement);
        }
    }

    function scrollToBottom() {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = userInput.value.trim();
        if (!message) return;

        // UI state update
        appendMessage('user', message);
        userInput.value = '';
        sendBtn.disabled = true;
        const typingIndicator = showTypingIndicator();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            removeTypingIndicator(typingIndicator);

            if (response.ok) {
                const data = await response.json();
                appendMessage('system', data.reply);
            } else {
                appendMessage('system', 'Sorry, I encountered an error while processing your request.');
                console.error("Server Error:", await response.text());
            }
        } catch (error) {
            removeTypingIndicator(typingIndicator);
            appendMessage('system', 'Network error. Make sure the server is running.');
            console.error('Fetch Error:', error);
        } finally {
            sendBtn.disabled = false;
            userInput.focus();
        }
    });
});
