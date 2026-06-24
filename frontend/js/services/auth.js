/**
 * 登录与云同步服务
 */
import apiClient from '../api/client.js';
import { CONFIG } from '../config.js';
import { getHistory, mergeHistory } from './history.js';

export function getAuthToken() {
  return localStorage.getItem(CONFIG.STORAGE_KEY_AUTH_TOKEN) || '';
}

export function getCurrentUser() {
  try {
    const data = localStorage.getItem(CONFIG.STORAGE_KEY_AUTH_USER);
    return data ? JSON.parse(data) : null;
  } catch (e) {
    return null;
  }
}

export function isLoggedIn() {
  return Boolean(getAuthToken() && getCurrentUser());
}

export async function login(email, password) {
  const data = await apiClient.post('/api/auth/login', { email, password });
  persistSession(data.user, data.token);
  await syncHistory();
  return data.user;
}

export async function register(email, password, displayName) {
  const data = await apiClient.post('/api/auth/register', {
    email,
    password,
    display_name: displayName
  });
  persistSession(data.user, data.token);
  await syncHistory();
  return data.user;
}

export function logout() {
  localStorage.removeItem(CONFIG.STORAGE_KEY_AUTH_TOKEN);
  localStorage.removeItem(CONFIG.STORAGE_KEY_AUTH_USER);
}

export async function syncHistory() {
  const token = getAuthToken();
  if (!token) {
    return { synced: 0, merged: 0 };
  }

  const response = await fetch(`${CONFIG.API_BASE_URL}/api/auth/sync`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ readings: getHistory() })
  });

  if (!response.ok) {
    throw new Error(`云同步失败: HTTP ${response.status}`);
  }

  const data = await response.json();
  if (!data.success) {
    throw new Error(data.error || '云同步失败');
  }

  const merged = mergeHistory(data.readings || []);
  return { synced: data.synced || 0, merged };
}

function persistSession(user, token) {
  localStorage.setItem(CONFIG.STORAGE_KEY_AUTH_TOKEN, token);
  localStorage.setItem(CONFIG.STORAGE_KEY_AUTH_USER, JSON.stringify(user));
  if (typeof user?.query_credits === 'number') {
    window.dispatchEvent(new CustomEvent('billing:balance', {
      detail: { queryCredits: user.query_credits }
    }));
  }
}
