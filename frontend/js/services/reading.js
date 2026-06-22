/**
 * 占卜服务
 */
import apiClient from '../api/client.js';
import { renderCards } from '../ui/card.js';
import { showLoading, clearOutput, appendText, showError, getOutputText } from '../ui/loading.js';
import { saveHistory } from './history.js';
import { isLoggedIn, syncHistory } from './auth.js';
import { CONFIG } from '../config.js';

/**
 * 开始占卜
 */
export async function startReading(question, options = {}) {
  const spreadId = options.spreadId || CONFIG.DEFAULT_SPREAD;
  const customSpread = options.customSpread || null;
  const readerStyle = options.readerStyle || '';

  try {
    // 1. 抽牌
    const { cards } = await apiClient.post('/api/reading/draw', {
      spread_id: spreadId,
      custom_spread: customSpread
    });
    
    // 2. 渲染卡牌
    renderCards(cards);
    
    // 3. 获取解读（流式）
    clearOutput();
    showLoading();
    
    await apiClient.streamPost(
      '/api/reading/interpret',
      {
        question,
        spread_id: spreadId,
        cards,
        custom_spread: customSpread,
        reader_style: readerStyle
      },
      // onChunk
      (text) => {
        appendText(text);
      },
      // onDone
      () => {
        saveHistory(question, spreadId, cards, getOutputText(), {
          customSpread,
          readerStyle
        });
        syncIfLoggedIn();
      },
      // onError
      (error) => {
        showError(error);
      }
    );
    
    return { success: true, cards, spreadId, customSpread, readerStyle, reading: getOutputText() };
    
  } catch (error) {
    showError(error.message);
    return { success: false, error: error.message };
  }
}

/**
 * 每日塔罗
 */
export async function startDailyTarot(question = '', options = {}) {
  const readerStyle = options.readerStyle || '';
  let dailyCards = [];

  try {
    clearOutput();
    showLoading('正在抽取今日能量...');

    await apiClient.streamPost(
      '/api/reading/daily',
      {
        question,
        reader_style: readerStyle
      },
      (payload) => {
        if (typeof payload === 'object' && payload.type === 'cards') {
          dailyCards = payload.cards || [];
          renderCards(dailyCards);
          return;
        }
        appendText(payload);
      },
      () => {
        saveHistory(question || '每日塔罗', 'daily', dailyCards, getOutputText(), {
          readerStyle,
          recordType: 'daily'
        });
        syncIfLoggedIn();
      },
      (error) => {
        showError(error);
      }
    );

    return {
      success: true,
      cards: dailyCards,
      spreadId: 'daily',
      readerStyle,
      reading: getOutputText()
    };
  } catch (error) {
    showError(error.message);
    return { success: false, error: error.message };
  }
}

async function syncIfLoggedIn() {
  if (!isLoggedIn()) return;

  try {
    await syncHistory();
  } catch (error) {
    console.warn('自动云同步失败:', error);
  }
}

/**
 * 基于当前牌面继续追问
 */
export async function askFollowUp(currentReading, followupQuestion, onChunk) {
  try {
    await apiClient.streamPost(
      '/api/reading/follow-up',
      {
        original_question: currentReading.question,
        followup_question: followupQuestion,
        spread_id: currentReading.spreadId || CONFIG.DEFAULT_SPREAD,
        cards: currentReading.cards,
        reading: currentReading.reading,
        custom_spread: currentReading.customSpread || null,
        reader_style: currentReading.readerStyle || ''
      },
      (text) => {
        if (onChunk) {
          onChunk(text);
        } else {
          appendText(text);
        }
      },
      null,
      (error) => {
        showError(error);
      }
    );

    return { success: true };
  } catch (error) {
    showError(error.message);
    return { success: false, error: error.message };
  }
}
