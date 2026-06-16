/**
 * 前端配置
 */

/**
 * 根据当前页面地址自动推断 API 基础 URL
 * - 开发：前端 :8080 / :3000 → 后端 :5001（同 hostname，无需写死 IP）
 * - 生产：Nginx 同源反代 → 空字符串，走相对路径 /api/...
 */
function resolveApiBaseUrl() {
  const { protocol, hostname, port } = window.location;
  const devPorts = new Set(['8080', '3000']);

  if (devPorts.has(port)) {
    return `${protocol}//${hostname}:5001`;
  }

  return '';
}

export const CONFIG = {
  API_BASE_URL: resolveApiBaseUrl(),

  // 存储键
  STORAGE_KEY_HISTORY: 'tarot_history',
  MAX_HISTORY: 100,

  // 默认牌阵
  DEFAULT_SPREAD: 'single'
};
