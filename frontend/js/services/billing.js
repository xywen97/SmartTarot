/**
 * 查询余量与充值服务
 */
import apiClient from '../api/client.js';
import { CONFIG } from '../config.js';

export async function loadBillingStatus() {
  const data = await apiClient.get('/api/billing/status');
  emitBalance(data.query_credits);
  return data;
}

export async function createRechargeOrder(packageId, provider) {
  const data = await apiClient.post('/api/billing/recharge/orders', {
    package_id: packageId,
    provider
  });
  return data.order;
}

export function emitBalance(queryCredits) {
  if (typeof queryCredits !== 'number') return;

  window.dispatchEvent(new CustomEvent('billing:balance', {
    detail: { queryCredits }
  }));
}

export function formatAmount(amountCents) {
  return `¥${(amountCents / 100).toFixed(2)}`;
}

export function resolveBillingAssetUrl(path) {
  if (!path) return '';
  if (/^https?:\/\//i.test(path)) return path;
  return `${CONFIG.API_BASE_URL}${path}`;
}
