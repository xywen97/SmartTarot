/**
 * 历史记录服务
 */
import { CONFIG } from '../config.js';

/**
 * 保存历史记录
 */
export function saveHistory(question, spreadId, cards, reading, metadata = {}) {
  try {
    const history = getHistory();
    
    const record = {
      id: `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: Date.now(),
      question,
      spreadId,
      cards: cards.map(c => ({
        cardId: c.id,
        cardName: c.name_cn,
        orientation: c.orientation
      })),
      rawCards: cards,
      reading,
      favorite: false,
      customSpread: metadata.customSpread || null,
      readerStyle: metadata.readerStyle || '',
      recordType: metadata.recordType || 'tarot'
    };
    
    history.unshift(record);
    
    if (history.length > CONFIG.MAX_HISTORY) {
      history.length = CONFIG.MAX_HISTORY;
    }
    
    localStorage.setItem(CONFIG.STORAGE_KEY_HISTORY, JSON.stringify(history));
    
    console.log('✅ 历史记录已保存');
  } catch (e) {
    console.error('保存历史记录失败:', e);
  }
}

/**
 * 获取历史记录
 */
export function getHistory() {
  try {
    const data = localStorage.getItem(CONFIG.STORAGE_KEY_HISTORY);
    return data ? JSON.parse(data) : [];
  } catch (e) {
    console.error('读取历史记录失败:', e);
    return [];
  }
}

/**
 * 删除历史记录
 */
export function deleteHistory(id) {
  try {
    const history = getHistory().filter(r => r.id !== id);
    localStorage.setItem(CONFIG.STORAGE_KEY_HISTORY, JSON.stringify(history));
    console.log('✅ 历史记录已删除');
  } catch (e) {
    console.error('删除历史记录失败:', e);
  }
}

/**
 * 清空所有历史记录
 */
export function clearAllHistory() {
  try {
    localStorage.removeItem(CONFIG.STORAGE_KEY_HISTORY);
    console.log('✅ 所有历史记录已清空');
  } catch (e) {
    console.error('清空历史记录失败:', e);
  }
}

/**
 * 获取收藏的记录
 */
export function getFavorites() {
  try {
    const history = getHistory();
    return history.filter(r => r.favorite);
  } catch (e) {
    console.error('读取收藏记录失败:', e);
    return [];
  }
}

/**
 * 切换收藏状态
 */
export function toggleFavorite(id) {
  try {
    const history = getHistory();
    const record = history.find(r => r.id === id);
    if (record) {
      record.favorite = !record.favorite;
      localStorage.setItem(CONFIG.STORAGE_KEY_HISTORY, JSON.stringify(history));
      console.log(`✅ 收藏状态已切换: ${record.favorite ? '收藏' : '取消收藏'}`);
      return record.favorite;
    }
  } catch (e) {
    console.error('切换收藏状态失败:', e);
  }
  return false;
}
