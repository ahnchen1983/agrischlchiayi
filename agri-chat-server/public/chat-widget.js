/**
 * Agri-Chat Web Component
 * 右下角浮窗，可嵌入任何網站
 */

class AgriChat extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.isOpen = false;
    this.messages = [];
    this.apiUrl =
      this.getAttribute('api-url') || 'https://agri-chat.onrender.com';
  }

  connectedCallback() {
    this.render();
    this.setupEventListeners();
  }

  render() {
    const style = `
      :host {
        --primary-color: #2ecc71;
        --secondary-color: #27ae60;
        --text-color: #333;
        --bg-color: #fff;
        --border-color: #ddd;
      }

      .chat-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 380px;
        max-width: calc(100vw - 20px);
        height: 600px;
        max-height: 80vh;
        display: flex;
        flex-direction: column;
        background: var(--bg-color);
        border-radius: 12px;
        box-shadow: 0 5px 40px rgba(0, 0, 0, 0.16);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        z-index: 999999;
        opacity: 0;
        transform: scale(0.95) translateY(20px);
        transition: all 0.3s ease;
        pointer-events: none;
      }

      .chat-container.open {
        opacity: 1;
        transform: scale(1) translateY(0);
        pointer-events: all;
      }

      .chat-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        padding: 20px;
        border-radius: 12px 12px 0 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }

      .chat-header h3 {
        margin: 0;
        font-size: 18px;
        font-weight: 600;
      }

      .chat-header p {
        margin: 4px 0 0;
        font-size: 12px;
        opacity: 0.9;
      }

      .close-btn {
        background: rgba(255, 255, 255, 0.3);
        border: none;
        color: white;
        cursor: pointer;
        font-size: 24px;
        width: 32px;
        height: 32px;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: background 0.2s;
      }

      .close-btn:hover {
        background: rgba(255, 255, 255, 0.5);
      }

      .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 20px;
        background: #fafafa;
        display: flex;
        flex-direction: column;
        gap: 12px;
      }

      .message {
        display: flex;
        gap: 8px;
        margin-bottom: 8px;
      }

      .message.user {
        justify-content: flex-end;
      }

      .message-content {
        max-width: 70%;
        padding: 12px 16px;
        border-radius: 12px;
        word-wrap: break-word;
        font-size: 14px;
        line-height: 1.4;
      }

      .message.bot .message-content {
        background: white;
        border: 1px solid var(--border-color);
        color: var(--text-color);
      }

      .message.user .message-content {
        background: var(--primary-color);
        color: white;
        border-radius: 12px 0 12px 12px;
      }

      .message-sources {
        font-size: 12px;
        margin-top: 8px;
        padding: 8px;
        background: #f0f8f4;
        border-left: 3px solid var(--primary-color);
        border-radius: 4px;
      }

      .message-sources a {
        color: var(--secondary-color);
        text-decoration: none;
        display: block;
        margin: 4px 0;
      }

      .message-sources a:hover {
        text-decoration: underline;
      }

      .chat-input {
        padding: 16px;
        border-top: 1px solid var(--border-color);
        display: flex;
        gap: 8px;
      }

      .chat-input input {
        flex: 1;
        border: 1px solid var(--border-color);
        border-radius: 6px;
        padding: 10px 12px;
        font-size: 14px;
        font-family: inherit;
        outline: none;
        transition: border-color 0.2s;
      }

      .chat-input input:focus {
        border-color: var(--primary-color);
      }

      .chat-input button {
        background: var(--primary-color);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 16px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 600;
        transition: background 0.2s;
      }

      .chat-input button:hover {
        background: var(--secondary-color);
      }

      .chat-input button:disabled {
        background: #ccc;
        cursor: not-allowed;
      }

      .toggle-btn {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 56px;
        height: 56px;
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        border: none;
        border-radius: 50%;
        color: white;
        font-size: 24px;
        cursor: pointer;
        box-shadow: 0 2px 12px rgba(46, 204, 113, 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 999998;
        transition: all 0.3s ease;
        opacity: 1;
        transform: scale(1);
      }

      .toggle-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 4px 16px rgba(46, 204, 113, 0.4);
      }

      .toggle-btn.hidden {
        opacity: 0;
        pointer-events: none;
        transform: scale(0.8);
      }

      .loading {
        display: inline-block;
        width: 12px;
        height: 12px;
        background: var(--primary-color);
        border-radius: 50%;
        animation: pulse 1.5s infinite;
      }

      @keyframes pulse {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 1; }
      }

      @media (max-width: 480px) {
        .chat-container {
          width: calc(100vw - 20px);
          height: calc(100vh - 20px);
          max-height: 100vh;
        }
      }
    `;

    this.shadowRoot.innerHTML = `
      <style>${style}</style>

      <button class="toggle-btn" title="打開農業知識助手">
        🌾
      </button>

      <div class="chat-container">
        <div class="chat-header">
          <div>
            <h3>嘉義農業助手</h3>
            <p>由國本學堂知識庫驅動</p>
          </div>
          <button class="close-btn" title="關閉">✕</button>
        </div>

        <div class="chat-messages"></div>

        <div class="chat-input">
          <input type="text" placeholder="提問農業相關問題..." />
          <button type="submit">發送</button>
        </div>
      </div>
    `;
  }

  setupEventListeners() {
    const toggleBtn = this.shadowRoot.querySelector('.toggle-btn');
    const closeBtn = this.shadowRoot.querySelector('.close-btn');
    const container = this.shadowRoot.querySelector('.chat-container');
    const input = this.shadowRoot.querySelector('.chat-input input');
    const submitBtn = this.shadowRoot.querySelector('.chat-input button');

    toggleBtn.addEventListener('click', () => this.toggle());
    closeBtn.addEventListener('click', () => this.toggle());

    const sendMessage = async () => {
      const message = input.value.trim();
      if (!message) return;

      // 新增用戶訊息到 UI
      this.addMessage(message, 'user');
      input.value = '';
      submitBtn.disabled = true;

      // 新增 Loading 指示
      this.addMessage('思考中...', 'bot', true);

      try {
        const response = await fetch(`${this.apiUrl}/api/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message }),
        });

        if (!response.ok) {
          throw new Error(`API 錯誤: ${response.statusText}`);
        }

        const data = await response.json();

        // 移除 Loading 訊息
        const messages = this.shadowRoot.querySelectorAll('.message.bot');
        messages[messages.length - 1].remove();

        // 新增 AI 回答
        this.addMessage(data.answer, 'bot');
      } catch (error) {
        console.error('❌ 錯誤:', error);

        // 移除 Loading 訊息
        const messages = this.shadowRoot.querySelectorAll('.message.bot');
        if (messages.length > 0) {
          messages[messages.length - 1].remove();
        }

        this.addMessage(
          `無法連接到服務器。請確保 API URL 正確。\n\n錯誤: ${error.message}`,
          'bot',
        );
      } finally {
        submitBtn.disabled = false;
        input.focus();
      }
    };

    submitBtn.addEventListener('click', sendMessage);
    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });
  }

  toggle() {
    this.isOpen = !this.isOpen;
    const container = this.shadowRoot.querySelector('.chat-container');
    const toggleBtn = this.shadowRoot.querySelector('.toggle-btn');

    if (this.isOpen) {
      container.classList.add('open');
      toggleBtn.classList.add('hidden');
      this.shadowRoot.querySelector('.chat-input input').focus();
    } else {
      container.classList.remove('open');
      toggleBtn.classList.remove('hidden');
    }
  }

  addMessage(text, role, isLoading = false) {
    const messagesDiv = this.shadowRoot.querySelector('.chat-messages');

    const messageEl = document.createElement('div');
    messageEl.className = `message ${role}`;

    if (isLoading) {
      messageEl.innerHTML = `
        <div class="message-content">
          <span class="loading"></span> ${text}
        </div>
      `;
    } else {
      // 分離內容和來源
      const [mainContent, sourcesPart] = text.split('**相關文檔：**');

      messageEl.innerHTML = `
        <div class="message-content">
          ${mainContent.trim()}
        </div>
        ${
          sourcesPart
            ? `<div class="message-sources">
                <strong>📚 相關文檔：</strong>
                ${sourcesPart
                  .split('\n')
                  .filter((line) => line.startsWith('- ['))
                  .map((line) => {
                    const match = line.match(/- \[(.*?)\]\((.*?)\)/);
                    if (match) {
                      return `<a href="${match[2]}" target="_blank">📖 ${match[1]}</a>`;
                    }
                    return '';
                  })
                  .join('')}
              </div>`
            : ''
        }
      `;
    }

    messagesDiv.appendChild(messageEl);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }
}

// 註冊 Web Component
customElements.define('agri-chat', AgriChat);
