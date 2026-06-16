/**
 * 加载状态
 */
import { MarkdownRenderer } from '../utils/markdown.js';

// 创建全局 Markdown 渲染器
let markdownRenderer = null;

function getRenderer() {
  if (!markdownRenderer) {
    markdownRenderer = new MarkdownRenderer('reading-output');
  }
  return markdownRenderer;
}

/**
 * 显示加载状态
 */
export function showLoading(message = '正在解读中...') {
  const output = document.getElementById('reading-output');
  output.innerHTML = `
    <div class="loading">
      <div class="spinner"></div>
      <p><span class="loading-sparkle">✨</span>${message}<span class="loading-sparkle">✨</span></p>
    </div>
  `;
}

/**
 * 隐藏加载状态
 */
export function hideLoading() {
  const output = document.getElementById('reading-output');
  const loading = output.querySelector('.loading');
  if (loading) {
    loading.remove();
  }
}

/**
 * 显示错误
 */
export function showError(message) {
  const output = document.getElementById('reading-output');
  output.innerHTML = `<div class="error-message">❌ ${message}</div>`;
}

/**
 * 清空输出
 */
export function clearOutput() {
  const output = document.getElementById('reading-output');
  output.innerHTML = '';
  getRenderer().clear();
}

/**
 * 重置为空状态
 */
export function resetOutput() {
  const output = document.getElementById('reading-output');
  output.innerHTML = `
    <div class="empty-state">
      <div class="empty-state-icon">🔮</div>
      <div class="empty-state-text">AI 解读将在这里显示</div>
    </div>
  `;
}

/**
 * 追加文本（使用 Markdown 渲染）
 */
export function appendText(text) {
  const output = document.getElementById('reading-output');

  // 如果是空状态或加载状态，先清空
  if (output.querySelector('.empty-state') || output.querySelector('.loading')) {
    output.innerHTML = '';
  }

  // 使用 Markdown 渲染器
  getRenderer().append(text);
}

/**
 * 获取当前文本内容
 */
export function getOutputText() {
  return getRenderer().getText();
}
