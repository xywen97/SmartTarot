/**
 * 主入口文件
 */
import { askFollowUp, startDailyTarot, startReading } from './services/reading.js';
import { getHistory, deleteHistory, clearAllHistory } from './services/history.js';
import { appendText, clearOutput, getOutputText } from './ui/loading.js';
import { shareReading } from './utils/share.js';
import { initTheme, toggleTheme } from './utils/theme.js';
import { showTarotSkillsInfo } from './utils/tarot-skills-info.js';
import { CONFIG } from './config.js';

// 全局变量存储当前占卜结果
let currentReading = {
  question: '',
  cards: [],
  reading: '',
  spreadId: '',
  customSpread: null,
  readerStyle: ''
};

/**
 * 初始化应用
 */
async function init() {
  console.log('🌙 AI 塔罗占卜系统初始化...');

  // 初始化主题
  initTheme();

  // 设置事件监听器
  setupEventListeners();
  
  console.log('✅ 系统已就绪');
}

/**
 * 设置事件监听器
 */
function setupEventListeners() {
  // 主题切换按钮
  const themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', toggleTheme);
  }

  // 开始占卜按钮
  const drawBtn = document.getElementById('draw-btn');
  if (drawBtn) {
    drawBtn.addEventListener('click', handleDrawClick);
  }

  const dailyBtn = document.getElementById('daily-btn');
  if (dailyBtn) {
    dailyBtn.addEventListener('click', handleDailyClick);
  }

  // 分享按钮
  const shareBtn = document.getElementById('share-btn');
  if (shareBtn) {
    shareBtn.addEventListener('click', handleShareClick);
  }

  // 智能推荐按钮
  const recommendBtn = document.getElementById('recommend-btn');
  if (recommendBtn) {
    recommendBtn.addEventListener('click', handleRecommendClick);
  }

  const spreadSelect = document.getElementById('spread-select');
  if (spreadSelect) {
    spreadSelect.addEventListener('change', handleSpreadChange);
  }

  document.querySelectorAll('#question-templates button').forEach((button) => {
    button.addEventListener('click', () => {
      const questionInput = document.getElementById('question-input');
      questionInput.value = button.dataset.question;
      questionInput.focus();
    });
  });

  const followUpBtn = document.getElementById('follow-up-btn');
  if (followUpBtn) {
    followUpBtn.addEventListener('click', handleFollowUpClick);
  }

  // Tarot Skills 信息按钮
  const tarotSkillsInfoBtn = document.getElementById('tarot-skills-info-btn');
  if (tarotSkillsInfoBtn) {
    tarotSkillsInfoBtn.addEventListener('click', showTarotSkillsInfo);
  }

  // 历史记录按钮
  const historyBtn = document.getElementById('history-btn');
  if (historyBtn) {
    historyBtn.addEventListener('click', showHistoryModal);
  }

  // 历史记录模态框关闭
  const historyClose = document.getElementById('history-close');
  if (historyClose) {
    historyClose.addEventListener('click', hideHistoryModal);
  }
  
  // 点击模态框外部关闭
  const historyModal = document.getElementById('history-modal');
  if (historyModal) {
    historyModal.addEventListener('click', (e) => {
      if (e.target === historyModal) {
        hideHistoryModal();
      }
    });
  }
  
  // 清空历史记录
  const clearHistoryBtn = document.getElementById('clear-history');
  if (clearHistoryBtn) {
    clearHistoryBtn.addEventListener('click', handleClearHistory);
  }
  
  // 历史记录搜索
  const historySearch = document.getElementById('history-search');
  if (historySearch) {
    historySearch.addEventListener('input', handleHistorySearch);
  }
  
  // 问题输入框 - Ctrl/Cmd + Enter 快捷键
  const questionInput = document.getElementById('question-input');
  if (questionInput) {
    questionInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
        handleDrawClick();
      }
    });
  }
}

function getReaderStyle() {
  return document.getElementById('reader-style-select')?.value || '';
}

function getCustomSpread() {
  const spreadSelect = document.getElementById('spread-select');
  if (!spreadSelect || spreadSelect.value !== 'custom') {
    return null;
  }

  const name = document.getElementById('custom-spread-name').value.trim() || '自定义牌阵';
  const positionLines = document.getElementById('custom-spread-positions').value
    .split('\n')
    .map(line => line.trim())
    .filter(Boolean);

  if (positionLines.length < 1 || positionLines.length > 10) {
    throw new Error('自定义牌阵需要 1-10 个位置');
  }

  return {
    name,
    description: '用户根据当前问题创建的自定义牌阵',
    positions: positionLines.map(line => ({
      name: line,
      description: line
    }))
  };
}

function handleSpreadChange() {
  const panel = document.getElementById('custom-spread-panel');
  const spreadSelect = document.getElementById('spread-select');
  if (!panel || !spreadSelect) return;

  panel.classList.toggle('hidden', spreadSelect.value !== 'custom');
}

function activateFollowUpPanel() {
  const panel = document.getElementById('follow-up-panel');
  if (panel) {
    panel.classList.remove('hidden');
  }
}

/**
 * 处理抽牌点击
 */
async function handleDrawClick() {
  const questionInput = document.getElementById('question-input');
  const question = questionInput.value.trim();
  
  if (!question) {
    alert('请输入你的问题');
    return;
  }
  
  // 获取选择的牌阵
  const spreadSelect = document.getElementById('spread-select');
  const spreadId = spreadSelect.value;
  let customSpread = null;

  try {
    customSpread = getCustomSpread();
  } catch (error) {
    alert(error.message);
    return;
  }
  
  const drawBtn = document.getElementById('draw-btn');
  const shareBtn = document.getElementById('share-btn');
  
  // 隐藏分享按钮
  shareBtn.style.display = 'none';
  
  // 禁用按钮
  drawBtn.disabled = true;
  drawBtn.textContent = '占卜中...';
  
  try {
    // 开始占卜
    const result = await startReading(question, {
      spreadId,
      customSpread,
      readerStyle: getReaderStyle()
    });
    
    if (result.success) {
      // 保存当前占卜结果
      currentReading.question = question;
      currentReading.cards = result.cards;
      currentReading.spreadId = result.spreadId;
      currentReading.customSpread = result.customSpread;
      currentReading.readerStyle = result.readerStyle;

      // 等待解读完成后获取文本
      setTimeout(() => {
        currentReading.reading = getOutputText();
        activateFollowUpPanel();
        
        // 显示分享按钮
        shareBtn.style.display = 'block';
      }, 2000);
    }
  } catch (error) {
    console.error('占卜失败:', error);
  } finally {
    // 恢复按钮
    drawBtn.disabled = false;
    drawBtn.textContent = '开始占卜';
  }
}

async function handleDailyClick() {
  const questionInput = document.getElementById('question-input');
  const focus = questionInput.value.trim();
  const dailyBtn = document.getElementById('daily-btn');
  const shareBtn = document.getElementById('share-btn');

  shareBtn.style.display = 'none';
  dailyBtn.disabled = true;
  dailyBtn.textContent = '抽取中...';

  try {
    const result = await startDailyTarot(focus, {
      readerStyle: getReaderStyle()
    });

    if (result.success) {
      currentReading.question = focus || '每日塔罗';
      currentReading.cards = result.cards;
      currentReading.spreadId = result.spreadId;
      currentReading.customSpread = {
        name: '每日塔罗',
        description: '今天的核心能量、机会、挑战与行动提醒',
        positions: [{ name: '今日能量', description: '今天最值得留意的核心能量' }]
      };
      currentReading.readerStyle = result.readerStyle;

      setTimeout(() => {
        currentReading.reading = getOutputText();
        activateFollowUpPanel();
        shareBtn.style.display = 'block';
      }, 500);
    }
  } catch (error) {
    console.error('每日塔罗失败:', error);
  } finally {
    dailyBtn.disabled = false;
    dailyBtn.textContent = '每日塔罗';
  }
}

/**
 * 处理分享点击
 */
async function handleShareClick() {
  if (!currentReading.question || !currentReading.cards.length) {
    alert('请先完成一次占卜');
    return;
  }

  await shareReading(
    currentReading.question,
    currentReading.cards,
    currentReading.reading
  );
}

async function handleFollowUpClick() {
  const input = document.getElementById('follow-up-input');
  const button = document.getElementById('follow-up-btn');
  const question = input.value.trim();

  if (!currentReading.question || !currentReading.cards.length || !currentReading.reading) {
    alert('请先完成一次占卜');
    return;
  }

  if (!currentReading.cards.every(card => card.upright && card.reversed)) {
    alert('这条旧历史记录缺少完整牌义上下文，无法继续追问。请重新占卜后再追问。');
    return;
  }

  if (!question) {
    alert('请输入追问内容');
    return;
  }

  button.disabled = true;
  button.textContent = '追问中...';

  const output = document.getElementById('reading-output');
  const prefix = `\n\n## 追问：${question}\n\n`;
  const previousReading = currentReading.reading;
  appendText(prefix);
  currentReading.reading += prefix;

  try {
    await askFollowUp({ ...currentReading, reading: previousReading }, question, (text) => {
      appendText(text);
      currentReading.reading += text;
      output.scrollTop = output.scrollHeight;
    });
    input.value = '';
  } catch (error) {
    console.error('追问失败:', error);
  } finally {
    button.disabled = false;
    button.textContent = '继续追问';
  }
}

/**
 * 处理智能推荐点击
 */
async function handleRecommendClick() {
  const questionInput = document.getElementById('question-input');
  const question = questionInput.value.trim();

  if (!question) {
    alert('请先输入问题');
    return;
  }

  const recommendBtn = document.getElementById('recommend-btn');
  const spreadSelect = document.getElementById('spread-select');
  const reasonDiv = document.getElementById('recommend-reason');

  // 禁用按钮
  recommendBtn.disabled = true;
  recommendBtn.textContent = '分析中...';

  try {
    const response = await fetch(`${CONFIG.API_BASE_URL}/api/reading/recommend-spread`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ question })
    });

    const data = await response.json();

    if (data.success) {
      // 设置推荐的牌阵
      spreadSelect.value = data.spread_id;

      // 显示推荐理由
      const confidence = Math.round(data.confidence * 100);
      reasonDiv.innerHTML = `<strong>🤖 AI 推荐：</strong>${data.reason} <span style="color: var(--color-gold);">(置信度: ${confidence}%)</span>`;
      reasonDiv.style.display = 'block';

      console.log(`✅ 推荐牌阵: ${data.spread_id}, 理由: ${data.reason}`);
    } else {
      alert('推荐失败: ' + data.error);
    }
  } catch (error) {
    console.error('推荐失败:', error);
    alert('推荐失败，请稍后重试');
  } finally {
    // 恢复按钮
    recommendBtn.disabled = false;
    recommendBtn.textContent = '🤖 智能推荐';
  }
}

/**
 * 显示历史记录模态框
 */
function showHistoryModal() {
  const modal = document.getElementById('history-modal');
  modal.classList.add('active');
  renderHistoryList();
}

/**
 * 隐藏历史记录模态框
 */
function hideHistoryModal() {
  const modal = document.getElementById('history-modal');
  modal.classList.remove('active');
}

/**
 * 渲染历史记录列表
 */
function renderHistoryList(searchQuery = '') {
  const historyList = document.getElementById('history-list');
  const history = getHistory();
  
  // 过滤历史记录
  const filteredHistory = searchQuery
    ? history.filter(item => 
        item.question.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : history;
  
  if (filteredHistory.length === 0) {
    historyList.innerHTML = `
      <div class="history-empty">
        ${searchQuery ? '未找到匹配的记录' : '暂无历史记录'}
      </div>
    `;
    return;
  }
  
  historyList.innerHTML = filteredHistory.map(item => {
    const date = new Date(item.timestamp);
    const dateStr = date.toLocaleDateString('zh-CN');
    const timeStr = date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
    
    const cardsStr = item.cards.map(c => c.cardName).join('、');
    
    return `
      <div class="history-item" data-id="${item.id}">
        <div class="history-item-header">
          <div class="history-item-question">${item.question}</div>
          <div class="history-item-actions">
            <button class="history-item-btn favorite ${item.favorite ? 'active' : ''}" 
                    onclick="toggleFavorite('${item.id}')" title="收藏">
              ${item.favorite ? '⭐' : '☆'}
            </button>
            <button class="history-item-btn" onclick="viewHistory('${item.id}')" title="查看">
              👁️
            </button>
            <button class="history-item-btn" onclick="deleteHistoryItem('${item.id}')" title="删除">
              🗑️
            </button>
          </div>
        </div>
        <div class="history-item-meta">
          <span>📅 ${dateStr} ${timeStr}</span>
          <span>🃏 ${item.spreadId}</span>
        </div>
        <div class="history-item-cards">${cardsStr}</div>
      </div>
    `;
  }).join('');
}

/**
 * 处理历史记录搜索
 */
function handleHistorySearch(e) {
  renderHistoryList(e.target.value);
}

/**
 * 清空历史记录
 */
function handleClearHistory() {
  if (confirm('确定要清空所有历史记录吗？此操作不可恢复。')) {
    clearAllHistory();
    renderHistoryList();
  }
}

/**
 * 切换收藏状态
 */
window.toggleFavorite = function(id) {
  const history = getHistory();
  const item = history.find(h => h.id === id);
  if (item) {
    item.favorite = !item.favorite;
    localStorage.setItem(CONFIG.STORAGE_KEY_HISTORY, JSON.stringify(history));
    renderHistoryList();
  }
};

/**
 * 查看历史记录
 */
window.viewHistory = function(id) {
  const history = getHistory();
  const item = history.find(h => h.id === id);
  if (item) {
    // 填充问题
    document.getElementById('question-input').value = item.question;
    
    // 显示解读
    clearOutput();
    appendText(item.reading);
    
    // 更新当前占卜结果（用于分享）
    currentReading.question = item.question;
    currentReading.cards = item.rawCards || item.cards;
    currentReading.reading = item.reading;
    currentReading.spreadId = item.spreadId;
    currentReading.customSpread = item.customSpread || null;
    currentReading.readerStyle = item.readerStyle || '';
    
    // 显示分享按钮
    document.getElementById('share-btn').style.display = 'block';
    activateFollowUpPanel();
    
    // 关闭模态框
    hideHistoryModal();
    
    // 滚动到解读区域
    document.getElementById('reading-section').scrollIntoView({ behavior: 'smooth' });
  }
};

/**
 * 删除历史记录
 */
window.deleteHistoryItem = function(id) {
  if (confirm('确定要删除这条记录吗？')) {
    deleteHistory(id);
    renderHistoryList();
  }
};

// 页面加载完成后初始化
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
