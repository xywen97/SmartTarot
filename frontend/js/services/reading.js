/**
 * 占卜服务
 */
import apiClient from '../api/client.js';
import { renderCards } from '../ui/card.js';
import { showLoading, clearOutput, appendText, showError, getOutputText } from '../ui/loading.js';
import { saveHistory } from './history.js';
import { CONFIG } from '../config.js';

/**
 * 开始占卜
 */
export async function startReading(question, spreadId = CONFIG.DEFAULT_SPREAD) {
  try {
    // 1. 抽牌
    const { cards } = await apiClient.post('/api/reading/draw', {
      spread_id: spreadId
    });
    
    // 2. 渲染卡牌
    renderCards(cards);
    
    // 3. 显示加载状态
    showLoading();
    
    // 4. 获取解读（流式）
    clearOutput();
    
    await apiClient.streamPost(
      '/api/reading/interpret',
      {
        question,
        spread_id: spreadId,
        cards
      },
      // onChunk
      (text) => {
        appendText(text);
      },
      // onDone
      () => {
        saveHistory(question, spreadId, cards, getOutputText());
      },
      // onError
      (error) => {
        showError(error);
      }
    );
    
    return { success: true, cards };
    
  } catch (error) {
    showError(error.message);
    return { success: false, error: error.message };
  }
}
