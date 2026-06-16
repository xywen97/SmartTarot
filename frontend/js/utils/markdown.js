/**
 * 简单的 Markdown 渲染器
 */

/**
 * 将 Markdown 转换为 HTML
 */
export function markdownToHtml(markdown) {
  let html = markdown;

  // 标题
  html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
  html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
  html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');

  // 粗体
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

  // 斜体
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');

  // 列表项
  html = html.replace(/^\- (.*$)/gim, '<li>$1</li>');
  html = html.replace(/^\* (.*$)/gim, '<li>$1</li>');

  // 包装连续的 li 标签
  html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');

  // 段落（将连续的非标签文本包装为 p）
  html = html.split('\n\n').map(para => {
    para = para.trim();
    if (!para) return '';
    if (para.startsWith('<h') || para.startsWith('<ul') || para.startsWith('<li')) {
      return para;
    }
    return `<p>${para}</p>`;
  }).join('\n');

  return html;
}

/**
 * 流式追加并渲染 Markdown
 */
export class MarkdownRenderer {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.buffer = '';
  }

  append(text) {
    this.buffer += text;
    this.render();
  }

  render() {
    this.container.innerHTML = markdownToHtml(this.buffer);
    this.container.scrollTop = this.container.scrollHeight;
  }

  clear() {
    this.buffer = '';
    this.container.innerHTML = '';
  }

  getText() {
    return this.buffer;
  }
}
