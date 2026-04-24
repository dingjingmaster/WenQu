// 全局状态
console.log('=== app.js 开始加载 ===');
console.log('anime.js 状态:', typeof anime !== 'undefined' ? '已加载' : '未加载');
console.log('particles.js 状态:', typeof particlesJS !== 'undefined' ? '已加载' : '未加载');

let selectedFiles = [];
let ws = null;
let processMessages = [];
let isProcessing = false;
let resultText = '';

// 初始化动画
function initAnimations() {
    // 检查 anime.js 是否加载
    if (typeof anime === 'undefined') {
        console.warn('anime.js 未加载，跳过所有动画初始化');
        return;
    }
    
    try {
        // 初始化粒子背景
        initParticles();
    } catch (e) {
        console.warn('粒子背景初始化失败:', e);
    }
    
    try {
        // Logo 字母动画
        initLogoAnimation();
    } catch (e) {
        console.warn('Logo 动画初始化失败:', e);
    }
    
    try {
        // 输入框聚焦动画
        initInputAnimation();
    } catch (e) {
        console.warn('输入框动画初始化失败:', e);
    }
}

// 初始化粒子背景
function initParticles() {
    // 检查 particlesJS 是否已加载
    if (typeof particlesJS === 'undefined') {
        console.warn('particles.js 未加载，跳过粒子背景初始化');
        return;
    }
    
    particlesJS('particles-js', {
        particles: {
            number: {
                value: 80,
                density: {
                    enable: true,
                    value_area: 800
                }
            },
            color: {
                value: ['#ffffff', '#667eea', '#764ba2']
            },
            shape: {
                type: 'circle',
                stroke: {
                    width: 0,
                    color: '#000000'
                }
            },
            opacity: {
                value: 0.5,
                random: true,
                anim: {
                    enable: true,
                    speed: 1,
                    opacity_min: 0.1,
                    sync: false
                }
            },
            size: {
                value: 3,
                random: true,
                anim: {
                    enable: true,
                    speed: 2,
                    size_min: 0.1,
                    sync: false
                }
            },
            line_linked: {
                enable: true,
                distance: 150,
                color: '#ffffff',
                opacity: 0.4,
                width: 1
            },
            move: {
                enable: true,
                speed: 2,
                direction: 'none',
                random: true,
                straight: false,
                out_mode: 'out',
                bounce: false,
                attract: {
                    enable: true,
                    rotateX: 600,
                    rotateY: 1200
                }
            }
        },
        interactivity: {
            detect_on: 'canvas',
            events: {
                onhover: {
                    enable: true,
                    mode: 'grab'
                },
                onclick: {
                    enable: true,
                    mode: 'push'
                },
                resize: true
            },
            modes: {
                grab: {
                    distance: 140,
                    line_linked: {
                        opacity: 1
                    }
                },
                bubble: {
                    distance: 400,
                    size: 40,
                    duration: 2,
                    opacity: 8,
                    speed: 3
                },
                repulse: {
                    distance: 200,
                    duration: 0.4
                },
                push: {
                    particles_nb: 4
                },
                remove: {
                    particles_nb: 2
                }
            }
        },
        retina_detect: true
    });
}

// Logo 动画
function initLogoAnimation() {
    const letters = document.querySelectorAll('.logo-letter');
    
    letters.forEach((letter, index) => {
        // 初始动画
        anime({
            targets: letter,
            translateY: [50, 0],
            opacity: [0, 1],
            delay: index * 100,
            duration: 800,
            easing: 'easeOutQuart'
        });
        
        // 悬停动画
        letter.addEventListener('mouseenter', () => {
            anime({
                targets: letter,
                scale: [1, 1.2],
                rotateY: [0, 360],
                duration: 600,
                easing: 'easeOutQuad'
            });
        });
    });
    
    // 副标题动画
    anime({
        targets: '.logo-subtitle',
        translateY: [20, 0],
        opacity: [0, 1],
        delay: 600,
        duration: 800,
        easing: 'easeOutQuad'
    });
}

// 输入框动画
function initInputAnimation() {
    const input = document.getElementById('userInput');
    
    input.addEventListener('focus', () => {
        anime({
            targets: '.input-wrapper',
            scale: [1, 1.02],
            duration: 300,
            easing: 'easeOutQuad'
        });
    });
    
    input.addEventListener('blur', () => {
        anime({
            targets: '.input-wrapper',
            scale: [1.02, 1],
            duration: 300,
            easing: 'easeOutQuad'
        });
    });
}

// WebSocket 连接
function connectWebSocket() {
    console.log('=== connectWebSocket 被调用 ===');
    console.log('当前状态:', ws ? '已有连接' : '新连接');
    
    updateStatus('connecting');
    
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/agent`;
    
    console.log('WebSocket URL:', wsUrl);
    console.log('创建新的 WebSocket 实例...');
    
    ws = new WebSocket(wsUrl);
    
    console.log('WebSocket 实例已创建，readyState:', ws.readyState);
    
    ws.onopen = function() {
        console.log('WebSocket 连接成功!');
        updateStatus('connected');
        addProcessMessage('系统', 'WebSocket 连接成功', 'success');
        
        // 连接成功动画
        anime({
            targets: '.status-indicator',
            scale: [1, 1.2, 1],
            duration: 500,
            easing: 'easeOutQuad'
        });
    };
    
    ws.onmessage = function(event) {
        try {
            const data = JSON.parse(event.data);
            handleWebSocketMessage(data);
        } catch (e) {
            console.error('WebSocket 消息解析错误:', e);
        }
    };
    
    ws.onerror = function() {
        updateStatus('disconnected');
        addProcessMessage('系统', 'WebSocket 连接错误', 'error');
    };
    
    ws.onclose = function() {
        updateStatus('disconnected');
        if (isProcessing) {
            addProcessMessage('系统', 'WebSocket 连接关闭', 'warning');
        }
        // 3 秒后尝试重连
        setTimeout(connectWebSocket, 3000);
    };
}

// 处理 WebSocket 消息
function handleWebSocketMessage(data) {
    const { type, content } = data;
    
    if (type === 'thought') {
        // 模型思考过程
        addThoughtMessage('思考', content);
    } else if (type === 'log' || type === 'progress') {
        addProcessMessage('Agent', content, 'info');
    } else if (type === 'result') {
        // 收到最终结果
        resultText = content;
        
        // 自动折叠思考过程面板
        const thoughtSection = document.getElementById('thoughtSection');
        const thoughtContent = document.getElementById('thoughtContent');
        const thoughtArrow = document.getElementById('thoughtArrow');
        
        if (thoughtContent.style.maxHeight && thoughtContent.style.maxHeight !== '0') {
            thoughtContent.style.maxHeight = '0';
            thoughtArrow.classList.remove('rotated');
        }
        
        // 显示结果
        showResult(content);
        isProcessing = false;
        updateExecuteButton(false);
        addProcessMessage('系统', '任务执行完成', 'success');
        
        // 结果展示动画
        anime({
            targets: '#resultSection',
            scale: [0.9, 1],
            opacity: [0, 1],
            duration: 500,
            easing: 'easeOutQuad'
        });
    } else if (type === 'error') {
        addProcessMessage('错误', content, 'error');
        isProcessing = false;
        updateExecuteButton(false);
    }
}

// 添加思考过程消息
let thoughtMessages = [];
function addThoughtMessage(source, content) {
    const now = new Date();
    const time = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;
    
    thoughtMessages.push({
        source,
        content,
        time
    });
    
    const messagesDiv = document.getElementById('thoughtMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'thought-item';
    messageDiv.innerHTML = `
        <span class="thought-icon">💭</span>
        <span class="thought-text">${escapeHtml(content)}</span>
    `;
    messagesDiv.appendChild(messageDiv);
    
    // 消息进入动画
    if (typeof anime !== 'undefined') {
        anime({
            targets: messageDiv,
            translateX: [-20, 0],
            opacity: [0, 1],
            duration: 300,
            easing: 'easeOutQuad'
        });
    }
    
    // 自动滚动到底部
    const thoughtContent = document.getElementById('thoughtContent');
    if (thoughtContent) {
        thoughtContent.scrollTop = thoughtContent.scrollHeight;
    }
    
    // 显示思考面板
    const thoughtSection = document.getElementById('thoughtSection');
    if (thoughtSection) {
        thoughtSection.style.display = 'block';
    }
    
    // 更新思考计数
    updateThoughtCount();
    
    // 展开面板
    const thoughtArrow = document.getElementById('thoughtArrow');
    if (thoughtArrow && !thoughtArrow.classList.contains('rotated')) {
        toggleThoughtCollapse();
    }
}

// 添加过程消息
function addProcessMessage(source, content, type) {
    const now = new Date();
    const time = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;
    
    processMessages.push({
        source,
        content,
        type,
        time
    });
    
    const messagesDiv = document.getElementById('processMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `process-message ${type}`;
    messageDiv.innerHTML = `
        <span class="message-time">${time}</span>
        <span class="message-content">${escapeHtml(content)}</span>
    `;
    messagesDiv.appendChild(messageDiv);
    
    // 消息进入动画
    anime({
        targets: messageDiv,
        translateX: [-50, 0],
        opacity: [0, 1],
        duration: 400,
        easing: 'easeOutQuad'
    });
    
    // 自动滚动到底部
    const processContent = document.getElementById('processContent');
    processContent.scrollTop = processContent.scrollHeight;
    
    // 显示过程面板
    const processSection = document.getElementById('processSection');
    processSection.style.display = 'block';
    
    // 更新消息计数
    updateProcessCount();
    
    // 展开面板
    const processArrow = document.getElementById('processArrow');
    if (!processArrow.classList.contains('rotated')) {
        toggleProcessCollapse();
    }
}

// 更新思考计数
function updateThoughtCount() {
    const countSpan = document.getElementById('thoughtCount');
    if (countSpan) {
        countSpan.textContent = `${thoughtMessages.length} 条`;
    }
}

// 更新消息计数
function updateProcessCount() {
    const countSpan = document.getElementById('processCount');
    if (countSpan) {
        countSpan.textContent = `${processMessages.length} 条`;
    }
}

// 处理文件选择
function handleFileSelect(event) {
    const files = Array.from(event.target.files);
    
    files.forEach(file => {
        selectedFiles.push(file);
    });
    
    updateFileList();
}

// 更新文件列表显示
function updateFileList() {
    const fileListDiv = document.getElementById('fileList');
    fileListDiv.innerHTML = '';
    
    selectedFiles.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.innerHTML = `
            <span class="file-icon">📄</span>
            <span class="file-name">${escapeHtml(file.name)}</span>
            <button class="delete-btn" onclick="removeFile(${index})">×</button>
        `;
        fileListDiv.appendChild(fileItem);
        
        // 文件项进入动画
        anime({
            targets: fileItem,
            translateX: [-30, 0],
            opacity: [0, 1],
            delay: index * 50,
            duration: 300,
            easing: 'easeOutQuad'
        });
    });
}

// 删除文件
function removeFile(index) {
    const fileListDiv = document.getElementById('fileList');
    const fileItems = fileListDiv.querySelectorAll('.file-item');
    
    if (fileItems[index]) {
        // 删除动画
        anime({
            targets: fileItems[index],
            translateX: [0, 50],
            opacity: [1, 0],
            duration: 300,
            easing: 'easeInQuad',
            complete: function() {
                selectedFiles.splice(index, 1);
                updateFileList();
            }
        });
    } else {
        selectedFiles.splice(index, 1);
        updateFileList();
    }
}

// 执行处理
async function handleExecute() {
    const userInput = document.getElementById('userInput').value.trim();
    
    console.log('用户输入:', userInput);
    console.log('WebSocket 状态:', ws ? ws.readyState : 'null');
    
    if (!userInput && selectedFiles.length === 0) {
        alert('请输入问题或选择文件');
        return;
    }
    
    if (!ws || ws.readyState !== WebSocket.OPEN) {
        console.error('WebSocket 未连接!');
        alert('WebSocket 未连接，无法执行');
        return;
    }
    
    isProcessing = true;
    updateExecuteButton(true);
    processMessages = [];
    document.getElementById('processMessages').innerHTML = '';
    document.getElementById('resultSection').style.display = 'none';
    
    addProcessMessage('系统', '开始执行任务...', 'info');
    
    // 按钮点击动画
    anime({
        targets: '#executeBtn',
        scale: [0.95, 1],
        duration: 200,
        easing: 'easeOutQuad'
    });
    
    // 准备上传数据
    const formData = new FormData();
    formData.append('query', userInput);
    
    selectedFiles.forEach(file => {
        formData.append('files', file);
    });
    
    try {
        console.log('发送执行请求到 /api/agent/execute...');
        const response = await fetch('/api/agent/execute', {
            method: 'POST',
            body: formData
        });
        
        console.log('响应状态:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('响应数据:', data);
        
        if (data.success) {
            addProcessMessage('系统', '任务已提交，等待处理...', 'success');
        } else {
            throw new Error(data.message || '任务提交失败');
        }
    } catch (error) {
        console.error('执行失败:', error);
        addProcessMessage('错误', error.message, 'error');
        isProcessing = false;
        updateExecuteButton(false);
        alert('任务执行失败：' + error.message);
    }
}

// 更新执行按钮状态
function updateExecuteButton(processing) {
    const btn = document.getElementById('executeBtn');
    const btnText = document.getElementById('executeBtnText');
    const loader = document.getElementById('executeBtnLoader');
    
    if (processing) {
        btn.disabled = true;
        btnText.textContent = '执行中...';
        loader.style.display = 'inline-block';
        
        // 加载动画
        anime({
            targets: btn,
            scale: [1, 1.05, 1],
            duration: 1000,
            easing: 'easeInOutQuad',
            loop: true
        });
    } else {
        btn.disabled = false;
        btnText.textContent = '🚀 执行';
        loader.style.display = 'none';
        
        // 停止加载动画
        anime.remove(btn);
    }
}

// 显示结果（气泡对话形式）
function showResult(content) {
    const resultSection = document.getElementById('resultSection');
    const resultBody = document.getElementById('resultBody');
    
    // 获取用户问题
    const userInput = document.getElementById('userInput').value.trim();
    
    // 构建对话气泡 HTML
    let conversationHtml = '<div class="conversation-container">';
    
    // 用户问题气泡
    if (userInput) {
        conversationHtml += `
            <div class="message-bubble user-bubble">
                <div class="bubble-header">
                    <span class="bubble-icon">👤</span>
                    <span class="bubble-title">用户</span>
                </div>
                <div class="bubble-content">${escapeHtml(userInput)}</div>
            </div>
        `;
    }
    
    // Agent 答案气泡
    conversationHtml += `
        <div class="message-bubble agent-bubble">
            <div class="bubble-header">
                <span class="bubble-icon">🤖</span>
                <span class="bubble-title">Agent</span>
            </div>
            <div class="bubble-content">${renderMarkdown(content)}</div>
        </div>
    `;
    
    conversationHtml += '</div>';
    
    resultBody.innerHTML = conversationHtml;
    
    resultSection.style.display = 'block';
    
    // 滚动到结果区域
    setTimeout(() => {
        resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

// 简单的 Markdown 渲染
function renderMarkdown(text) {
    if (!text) return '';
    
    let html = text;
    
    // 代码块
    html = html.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code class="language-$1">$2</code></pre>');
    
    // 行内代码
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // 粗体
    html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    
    // 斜体
    html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    
    // 标题
    html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');
    
    // 列表
    html = html.replace(/^\- (.+)$/gm, '<li>$1</li>');
    html = html.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');
    
    // 段落
    html = html.replace(/\n\n/g, '</p><p>');
    html = '<p>' + html + '</p>';
    
    return html;
}

// 复制结果
async function copyResult() {
    try {
        await navigator.clipboard.writeText(resultText);
        
        // 复制成功动画
        const copyBtn = document.querySelector('.copy-button');
        anime({
            targets: copyBtn,
            scale: [1, 1.2, 1],
            backgroundColor: ['#667eea', '#4caf50', '#667eea'],
            duration: 500,
            easing: 'easeOutQuad'
        });
        
        alert('结果已复制到剪贴板');
    } catch (error) {
        alert('复制失败');
    }
}

// 折叠/展开思考过程面板
function toggleThoughtCollapse() {
    const thoughtContent = document.getElementById('thoughtContent');
    const thoughtArrow = document.getElementById('thoughtArrow');
    
    if (!thoughtContent || !thoughtArrow) return;
    
    if (thoughtContent.classList.contains('collapsed')) {
        thoughtContent.classList.remove('collapsed');
        thoughtArrow.classList.add('rotated');
        setTimeout(() => {
            thoughtContent.style.maxHeight = thoughtContent.scrollHeight + 'px';
        }, 10);
    } else {
        thoughtContent.style.maxHeight = '0';
        thoughtContent.classList.add('collapsed');
        thoughtArrow.classList.remove('rotated');
    }
}

// 折叠/展开过程面板
function toggleProcessCollapse() {
    const processContent = document.getElementById('processContent');
    const processArrow = document.getElementById('processArrow');
    
    if (!processContent || !processArrow) return;
    
    if (processContent.classList.contains('collapsed')) {
        processContent.classList.remove('collapsed');
        processArrow.classList.add('rotated');
        setTimeout(() => {
            processContent.style.maxHeight = processContent.scrollHeight + 'px';
        }, 10);
    } else {
        processContent.style.maxHeight = '0';
        processContent.classList.add('collapsed');
        processArrow.classList.remove('rotated');
    }
}

// 更新连接状态
function updateStatus(status) {
    const indicator = document.getElementById('statusIndicator');
    const statusText = document.getElementById('statusText');
    
    if (!indicator || !statusText) {
        console.warn('状态指示器元素不存在');
        return;
    }
    
    indicator.className = `status-indicator ${status}`;
    
    const statusMap = {
        connected: '已连接',
        connecting: '连接中...',
        disconnected: '未连接'
    };
    statusText.textContent = statusMap[status];
    
    // 状态变化动画
    if (typeof anime !== 'undefined') {
        anime({
            targets: indicator,
            scale: [1, 1.1, 1],
            duration: 300,
            easing: 'easeOutQuad'
        });
    }
}

// HTML 转义
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    console.log('=== DOMContentLoaded ===');
    console.log('开始初始化动画...');
    
    // 初始化动画
    initAnimations();
    
    console.log('开始连接 WebSocket...');
    // 连接 WebSocket
    connectWebSocket();
    
    console.log('自动聚焦到输入框...');
    // 自动聚焦到输入框
    const input = document.getElementById('userInput');
    if (input) {
        input.focus();
        console.log('输入框聚焦成功');
    } else {
        console.error('输入框元素不存在!');
    }
});
