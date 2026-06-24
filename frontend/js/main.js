/**
 * 主入口文件
 */
import { askFollowUp, startDailyTarot, startReading } from './services/reading.js';
import { getHistory, getVisibleHistoryCount, deleteHistory, hideAllHistory, updateJournal, toggleFavorite as toggleHistoryFavorite } from './services/history.js';
import { getCurrentUser, isLoggedIn, login, logout, register, syncHistory } from './services/auth.js';
import { createRechargeOrder, formatAmount, loadBillingStatus, resolveBillingAssetUrl } from './services/billing.js';
import apiClient from './api/client.js';
import { appendText, clearOutput, getOutputText, resetOutput } from './ui/loading.js';
import { clearCards } from './ui/card.js';
import { shareReading } from './utils/share.js';
import { initTheme, toggleTheme } from './utils/theme.js';
import { showTarotSkillsInfo } from './utils/tarot-skills-info.js';
import { CONFIG } from './config.js';

// 全局变量存储当前占卜结果
let currentReading = createEmptyReading();

let deckCache = [];
let activeJournalId = null;
let authMode = 'login';
let gateAuthMode = 'login';
let billingState = {
  queryCredits: null,
  packages: [],
  selectedPackageId: 'starter',
  selectedProvider: 'wechat'
};
let qrZoomState = null;

/**
 * 初始化应用
 */
async function init() {
  console.log('🌙 AI 塔罗占卜系统初始化...');

  // 初始化主题
  initTheme();

  // 设置事件监听器
  setupEventListeners();
  updateAuthUI();
  refreshBillingStatus();
  
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

  const learnBtn = document.getElementById('learn-btn');
  if (learnBtn) {
    learnBtn.addEventListener('click', showLearnModal);
  }

  const authToggle = document.getElementById('auth-toggle');
  if (authToggle) {
    authToggle.addEventListener('click', showAuthModal);
  }

  const creditToggle = document.getElementById('credit-toggle');
  if (creditToggle) {
    creditToggle.addEventListener('click', showAuthModal);
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

  const learnClose = document.getElementById('learn-close');
  if (learnClose) {
    learnClose.addEventListener('click', hideLearnModal);
  }

  const journalClose = document.getElementById('journal-close');
  if (journalClose) {
    journalClose.addEventListener('click', hideJournalModal);
  }

  const authClose = document.getElementById('auth-close');
  if (authClose) {
    authClose.addEventListener('click', hideAuthModal);
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

  const learnModal = document.getElementById('learn-modal');
  if (learnModal) {
    learnModal.addEventListener('click', (e) => {
      if (e.target === learnModal) {
        hideLearnModal();
      }
    });
  }

  const journalModal = document.getElementById('journal-modal');
  if (journalModal) {
    journalModal.addEventListener('click', (e) => {
      if (e.target === journalModal) {
        hideJournalModal();
      }
    });
  }

  const authModal = document.getElementById('auth-modal');
  if (authModal) {
    authModal.addEventListener('click', (e) => {
      if (e.target === authModal) {
        hideAuthModal();
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

  const learnSearch = document.getElementById('learn-search');
  if (learnSearch) {
    learnSearch.addEventListener('input', renderLearnDeck);
  }

  const learnFilter = document.getElementById('learn-filter');
  if (learnFilter) {
    learnFilter.addEventListener('change', renderLearnDeck);
  }

  const journalSave = document.getElementById('journal-save');
  if (journalSave) {
    journalSave.addEventListener('click', handleJournalSave);
  }

  document.getElementById('auth-login-tab')?.addEventListener('click', () => setAuthMode('login'));
  document.getElementById('auth-register-tab')?.addEventListener('click', () => setAuthMode('register'));
  document.getElementById('auth-submit')?.addEventListener('click', () => handleAuthSubmit('modal'));
  document.getElementById('gate-login-tab')?.addEventListener('click', () => setGateAuthMode('login'));
  document.getElementById('gate-register-tab')?.addEventListener('click', () => setGateAuthMode('register'));
  document.getElementById('gate-auth-submit')?.addEventListener('click', () => handleAuthSubmit('gate'));
  document.getElementById('sync-now-btn')?.addEventListener('click', handleSyncNow);
  document.getElementById('logout-btn')?.addEventListener('click', handleLogout);
  document.getElementById('create-recharge-order')?.addEventListener('click', handleCreateRechargeOrder);
  document.querySelectorAll('.payment-method').forEach((button) => {
    button.addEventListener('click', handlePaymentMethodClick);
  });
  window.addEventListener('billing:balance', handleBalanceEvent);
  window.addEventListener('billing:recharge-required', handleRechargeRequired);
  document.querySelectorAll('.password-toggle').forEach((button) => {
    button.addEventListener('click', handlePasswordToggle);
  });
  
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

function createEmptyReading() {
  return {
    question: '',
    cards: [],
    reading: '',
    spreadId: '',
    customSpread: null,
    readerStyle: ''
  };
}

function resetReadingState() {
  currentReading = createEmptyReading();

  const questionInput = document.getElementById('question-input');
  if (questionInput) {
    questionInput.value = '';
  }

  const followUpInput = document.getElementById('follow-up-input');
  if (followUpInput) {
    followUpInput.value = '';
  }

  document.getElementById('follow-up-panel')?.classList.add('hidden');

  const shareBtn = document.getElementById('share-btn');
  if (shareBtn) {
    shareBtn.style.display = 'none';
  }

  const reasonDiv = document.getElementById('recommend-reason');
  if (reasonDiv) {
    reasonDiv.textContent = '';
    reasonDiv.style.display = 'none';
  }

  clearCards();
  resetOutput();
}

function activateFollowUpPanel() {
  const panel = document.getElementById('follow-up-panel');
  if (panel) {
    panel.classList.remove('hidden');
  }
}

async function refreshBillingStatus() {
  if (!isLoggedIn()) {
    billingState = {
      ...billingState,
      queryCredits: null,
      packages: []
    };
    renderBillingUI();
    return;
  }

  try {
    const status = await loadBillingStatus();
    billingState = {
      ...billingState,
      queryCredits: status.query_credits,
      packages: status.recharge_packages || []
    };

    if (!billingState.packages.some(pkg => pkg.id === billingState.selectedPackageId)) {
      billingState.selectedPackageId = billingState.packages[0]?.id || 'starter';
    }

    renderBillingUI();
  } catch (error) {
    console.warn('查询余量加载失败:', error);
    renderBillingUI();
  }
}

function handleBalanceEvent(event) {
  billingState.queryCredits = event.detail.queryCredits;
  renderBillingUI();
}

function handleRechargeRequired(event) {
  billingState.queryCredits = event.detail.query_credits ?? billingState.queryCredits;
  renderBillingUI();
  showAuthModal();
  setAuthStatus('可用查询次数不足，请选择套餐充值后继续使用。');
}

function renderBillingUI() {
  const creditToggle = document.getElementById('credit-toggle');
  const creditCount = document.getElementById('billing-credit-count');
  const packages = document.getElementById('billing-packages');

  const label = typeof billingState.queryCredits === 'number'
    ? `余量 ${billingState.queryCredits}`
    : '余量 --';

  if (creditToggle) {
    creditToggle.textContent = label;
    creditToggle.classList.toggle('is-empty', billingState.queryCredits === 0);
  }

  if (creditCount) {
    creditCount.textContent = typeof billingState.queryCredits === 'number'
      ? String(billingState.queryCredits)
      : '--';
  }

  if (!packages) return;

  if (!billingState.packages.length) {
    packages.innerHTML = '<div class="billing-empty">登录后加载充值套餐</div>';
    return;
  }

  packages.innerHTML = billingState.packages.map(pkg => `
    <button type="button" class="billing-package ${pkg.id === billingState.selectedPackageId ? 'active' : ''}" data-package-id="${pkg.id}">
      <strong>${pkg.name}</strong>
      <span>${pkg.credits} 次 · ${formatAmount(pkg.amount_cents)}</span>
    </button>
  `).join('');

  packages.querySelectorAll('.billing-package').forEach((button) => {
    button.addEventListener('click', () => {
      billingState.selectedPackageId = button.dataset.packageId;
      hideRechargeOrder();
      renderBillingUI();
    });
  });

  document.querySelectorAll('.payment-method').forEach((button) => {
    button.classList.toggle('active', button.dataset.provider === billingState.selectedProvider);
  });
}

function handlePaymentMethodClick(event) {
  billingState.selectedProvider = event.currentTarget.dataset.provider;
  hideRechargeOrder();
  renderBillingUI();
}

async function handleCreateRechargeOrder() {
  if (!isLoggedIn()) {
    showAuthModal();
    setAuthStatus('请先登录后再充值。');
    return;
  }

  const button = document.getElementById('create-recharge-order');
  button.disabled = true;
  button.textContent = '生成中...';
  setAuthStatus('正在创建充值订单...');

  try {
    const order = await createRechargeOrder(billingState.selectedPackageId, billingState.selectedProvider);
    renderRechargeOrder(order);
    setAuthStatus('订单已创建，请扫码付款；支付完成后等待后台确认入账。');
  } catch (error) {
    setAuthStatus(error.message || '创建订单失败');
  } finally {
    button.disabled = false;
    button.textContent = '生成扫码订单';
  }
}

function renderRechargeOrder(order) {
  const container = document.getElementById('recharge-order');
  if (!container) return;

  const providerName = order.provider === 'wechat' ? '微信支付' : '支付宝';
  const qrCodeUrl = resolveBillingAssetUrl(order.qr_code_url);
  container.classList.remove('hidden');
  container.innerHTML = `
    <button type="button" class="payment-qr-trigger" aria-label="放大${providerName}收款码">
      <img class="payment-qr-code" src="${qrCodeUrl}" alt="${providerName}收款码">
    </button>
    <div class="order-detail">
      <strong>${order.credits} 次查询 · ${formatAmount(order.amount_cents)}</strong>
      <span>订单号：${order.order_no}</span>
      <small>${providerName}收款码 · 状态：${order.status === 'paid' ? '已支付' : '待确认'}</small>
    </div>
  `;

  const trigger = container.querySelector('.payment-qr-trigger');
  trigger.addEventListener('click', () => openQrZoom(order, trigger));
  requestAnimationFrame(() => openQrZoom(order, trigger));
}

function hideRechargeOrder() {
  closeQrZoom({ immediate: true });

  const container = document.getElementById('recharge-order');
  if (!container) return;

  container.classList.add('hidden');
  container.innerHTML = '';
}

function openQrZoom(order, trigger) {
  if (!trigger || qrZoomState?.overlay) return;

  const providerName = order.provider === 'wechat' ? '微信支付' : '支付宝';
  const qrCodeUrl = resolveBillingAssetUrl(order.qr_code_url);
  const overlay = document.createElement('div');
  overlay.className = 'qr-zoom-layer';
  overlay.innerHTML = `
    <div class="qr-zoom-backdrop"></div>
    <div class="qr-zoom-card" role="dialog" aria-modal="true" aria-label="${providerName}收款码">
      <button type="button" class="qr-zoom-close" aria-label="收起二维码">&times;</button>
      <img class="qr-zoom-image" src="${qrCodeUrl}" alt="${providerName}收款码">
      <div class="qr-zoom-caption">
        <strong>${order.credits} 次查询 · ${formatAmount(order.amount_cents)}</strong>
        <span>${providerName}收款码 · ${order.status === 'paid' ? '已支付' : '待确认'}</span>
      </div>
    </div>
  `;

  const handleEscape = (event) => {
    if (event.key === 'Escape') {
      closeQrZoom();
    }
  };

  document.body.appendChild(overlay);
  qrZoomState = { overlay, trigger, handleEscape };
  document.addEventListener('keydown', handleEscape);
  overlay.querySelector('.qr-zoom-close').addEventListener('click', () => closeQrZoom());
  overlay.querySelector('.qr-zoom-backdrop').addEventListener('click', () => closeQrZoom());

  requestAnimationFrame(() => {
    overlay.classList.add('active');
    animateQrZoom(trigger, overlay.querySelector('.qr-zoom-card'), 'open');
  });
}

function closeQrZoom(options = {}) {
  if (!qrZoomState?.overlay) return;

  const { overlay, trigger, handleEscape } = qrZoomState;
  const card = overlay.querySelector('.qr-zoom-card');
  document.removeEventListener('keydown', handleEscape);
  qrZoomState = null;

  if (options.immediate || !trigger?.isConnected || !card) {
    overlay.remove();
    return;
  }

  overlay.classList.add('closing');
  const animation = animateQrZoom(trigger, card, 'close');
  animation.finished.finally(() => {
    overlay.remove();
  });
}

function animateQrZoom(trigger, card, direction) {
  const source = trigger.getBoundingClientRect();
  const target = card.getBoundingClientRect();
  const sourceCenterX = source.left + source.width / 2;
  const sourceCenterY = source.top + source.height / 2;
  const targetCenterX = target.left + target.width / 2;
  const targetCenterY = target.top + target.height / 2;
  const translateX = sourceCenterX - targetCenterX;
  const translateY = sourceCenterY - targetCenterY;
  const scaleX = source.width / target.width;
  const scaleY = source.height / target.height;
  const collapsed = {
    opacity: 0.72,
    transform: `translate(${translateX}px, ${translateY}px) scale(${scaleX}, ${scaleY})`
  };
  const expanded = {
    opacity: 1,
    transform: 'translate(0, 0) scale(1, 1)'
  };

  return card.animate(
    direction === 'open' ? [collapsed, expanded] : [expanded, collapsed],
    {
      duration: direction === 'open' ? 280 : 240,
      easing: 'cubic-bezier(0.2, 0.8, 0.2, 1)',
      fill: 'forwards'
    }
  );
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
    const data = await apiClient.post('/api/reading/recommend-spread', { question });

    if (data.success) {
      // 设置推荐的牌阵
      spreadSelect.value = data.spread_id;
      handleSpreadChange();

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

async function showLearnModal() {
  const modal = document.getElementById('learn-modal');
  modal.classList.add('active');

  if (!deckCache.length) {
    const loaded = await loadDeck();
    if (!loaded) {
      return;
    }
  }

  renderLearnDeck();
}

function hideLearnModal() {
  const modal = document.getElementById('learn-modal');
  modal.classList.remove('active');
}

function showAuthModal() {
  updateAuthUI();
  if (!isLoggedIn()) {
    clearAuthForm();
    setAuthMode('login');
  }
  document.getElementById('auth-modal').classList.add('active');
}

function hideAuthModal() {
  closeQrZoom({ immediate: true });
  document.getElementById('auth-modal').classList.remove('active');
}

function setAuthMode(mode) {
  authMode = mode;
  document.getElementById('auth-login-tab').classList.toggle('active', mode === 'login');
  document.getElementById('auth-register-tab').classList.toggle('active', mode === 'register');
  document.getElementById('auth-display-name').classList.toggle('hidden', mode !== 'register');
  document.getElementById('auth-confirm-row').classList.toggle('hidden', mode !== 'register');
  document.getElementById('auth-submit').textContent = mode === 'login' ? '登录' : '注册并同步';
  setAuthStatus('');
}

function setGateAuthMode(mode) {
  gateAuthMode = mode;
  document.getElementById('gate-login-tab').classList.toggle('active', mode === 'login');
  document.getElementById('gate-register-tab').classList.toggle('active', mode === 'register');
  document.getElementById('gate-auth-display-name').classList.toggle('hidden', mode !== 'register');
  document.getElementById('gate-auth-confirm-row').classList.toggle('hidden', mode !== 'register');
  document.getElementById('gate-auth-submit').textContent = mode === 'login' ? '登录' : '注册并进入';
  setAuthStatus('', 'gate');
}

function updateAuthUI() {
  const user = getCurrentUser();
  const loggedIn = isLoggedIn();
  const toggle = document.getElementById('auth-toggle');
  const userPanel = document.getElementById('auth-user-panel');
  const formPanel = document.getElementById('auth-form-panel');
  const userInfo = document.getElementById('auth-user-info');

  if (toggle) {
    toggle.textContent = loggedIn ? '已登录' : '登录';
  }

  document.body.classList.toggle('is-authenticated', loggedIn);

  if (!userPanel || !formPanel || !userInfo) return;

  userPanel.classList.toggle('hidden', !loggedIn);
  formPanel.classList.toggle('hidden', loggedIn);

  if (loggedIn && user) {
    userInfo.innerHTML = `
      <strong>${user.display_name}</strong>
      <span>${user.email}</span>
      <small>登录后，本地历史会同步到云端；云端记录会合并回本机。</small>
    `;
  }
}

function setAuthStatus(message, scope = 'modal') {
  const statusId = scope === 'gate' ? 'gate-auth-status' : 'auth-status';
  const status = document.getElementById(statusId);
  if (status) {
    status.textContent = message;
  }
}

function clearAuthForm(scope = 'all') {
  const ids = scope === 'gate'
    ? ['gate-auth-email', 'gate-auth-password', 'gate-auth-password-confirm', 'gate-auth-display-name']
    : scope === 'modal'
      ? ['auth-email', 'auth-password', 'auth-password-confirm', 'auth-display-name']
      : [
          'auth-email', 'auth-password', 'auth-password-confirm', 'auth-display-name',
          'gate-auth-email', 'gate-auth-password', 'gate-auth-password-confirm', 'gate-auth-display-name'
        ];

  ids.forEach((id) => {
    const input = document.getElementById(id);
    if (input) {
      input.value = '';
    }
  });

  ids.filter(id => id.includes('password')).forEach((id) => {
    const input = document.getElementById(id);
    if (input) {
      input.type = 'password';
    }
  });

  document.querySelectorAll('.password-toggle').forEach((button) => {
    button.textContent = '👁';
  });
}

async function handleAuthSubmit(scope = 'modal') {
  const isGate = scope === 'gate';
  const mode = isGate ? gateAuthMode : authMode;
  const prefix = isGate ? 'gate-auth' : 'auth';
  const email = document.getElementById(`${prefix}-email`).value.trim();
  const password = document.getElementById(`${prefix}-password`).value;
  const passwordConfirm = document.getElementById(`${prefix}-password-confirm`).value;
  const displayName = document.getElementById(`${prefix}-display-name`).value.trim();
  const submit = document.getElementById(`${prefix}-submit`);

  if (!email || !password) {
    setAuthStatus('请输入邮箱和密码', scope);
    return;
  }

  if (mode === 'register' && password !== passwordConfirm) {
    setAuthStatus('两次输入的密码不一致', scope);
    return;
  }

  submit.disabled = true;
  submit.textContent = mode === 'login' ? '登录中...' : '注册中...';
  setAuthStatus('正在连接云端...', scope);

  try {
    if (mode === 'login') {
      await login(email, password);
    } else {
      await register(email, password, displayName);
    }

    updateAuthUI();
    await refreshBillingStatus();
    resetReadingState();
    clearAuthForm(scope);
    renderHistoryList(document.getElementById('history-search')?.value || '');
    setAuthStatus('已登录，并完成历史记录同步', scope);
    hideAuthModal();
  } catch (error) {
    setAuthStatus(error.message || '操作失败', scope);
  } finally {
    submit.disabled = false;
    if (isLoggedIn()) {
      submit.textContent = mode === 'login' ? '登录' : (isGate ? '注册并进入' : '注册并同步');
    } else if (isGate) {
      setGateAuthMode(mode);
    } else {
      setAuthMode(mode);
    }
  }
}

function handlePasswordToggle(event) {
  const targetId = event.currentTarget.dataset.target;
  const input = document.getElementById(targetId);
  if (!input) return;

  const nextType = input.type === 'password' ? 'text' : 'password';
  input.type = nextType;
  event.currentTarget.textContent = nextType === 'password' ? '👁' : '🙈';
}

async function handleSyncNow() {
  const button = document.getElementById('sync-now-btn');
  button.disabled = true;
  button.textContent = '同步中...';
  setAuthStatus('正在同步历史记录...');

  try {
    const result = await syncHistory();
    renderHistoryList(document.getElementById('history-search')?.value || '');
    setAuthStatus(`同步完成：上传 ${result.synced} 条，合并 ${result.merged} 条，可见 ${getVisibleHistoryCount()} 条`);
  } catch (error) {
    setAuthStatus(error.message || '同步失败');
  } finally {
    button.disabled = false;
    button.textContent = '立即同步';
  }
}

function handleLogout() {
  logout();
  billingState.queryCredits = null;
  billingState.packages = [];
  hideRechargeOrder();
  resetReadingState();
  clearAuthForm('all');
  setAuthMode('login');
  setGateAuthMode('login');
  updateAuthUI();
  renderHistoryList(document.getElementById('history-search')?.value || '');
  setAuthStatus('已退出登录，本地历史仍保留', 'gate');
  hideAuthModal();
}

function showJournalModal(id) {
  const history = getHistory();
  const item = history.find(h => h.id === id);
  if (!item) return;

  activeJournalId = id;
  const modal = document.getElementById('journal-modal');
  const summary = document.getElementById('journal-summary');
  const tagsInput = document.getElementById('journal-tags');
  const noteInput = document.getElementById('journal-note');

  const date = new Date(item.timestamp).toLocaleString('zh-CN');
  const cards = item.cards.map(c => c.cardName).join('、');
  summary.innerHTML = `
    <strong>${item.question}</strong>
    <span>${date}</span>
    <span>${cards || '无牌面记录'}</span>
  `;
  tagsInput.value = (item.tags || []).join(', ');
  noteInput.value = item.note || '';
  modal.classList.add('active');
}

function hideJournalModal() {
  const modal = document.getElementById('journal-modal');
  modal.classList.remove('active');
  activeJournalId = null;
}

function handleJournalSave() {
  if (!activeJournalId) return;

  const tags = document.getElementById('journal-tags').value
    .split(',')
    .map(tag => tag.trim())
    .filter(Boolean);
  const note = document.getElementById('journal-note').value.trim();

  if (updateJournal(activeJournalId, tags, note)) {
    hideJournalModal();
    renderHistoryList(document.getElementById('history-search').value);
  } else {
    alert('保存失败，请稍后重试');
  }
}

async function loadDeck() {
  const deckContainer = document.getElementById('learn-deck');
  deckContainer.innerHTML = '<div class="history-empty">正在加载牌库...</div>';

  try {
    const response = await fetch(`${CONFIG.API_BASE_URL}/api/data/deck`);
    const data = await response.json();
    deckCache = data.success ? data.cards : [];
    return deckCache.length > 0;
  } catch (error) {
    console.error('加载牌库失败:', error);
    deckCache = [];
    deckContainer.innerHTML = '<div class="history-empty">牌库加载失败，请确认后端服务已启动</div>';
    return false;
  }
}

function renderLearnDeck() {
  const deckContainer = document.getElementById('learn-deck');
  const search = document.getElementById('learn-search').value.trim().toLowerCase();
  const filter = document.getElementById('learn-filter').value;

  const cards = deckCache.filter(card => {
    const matchesFilter = filter === 'all'
      || card.type === filter
      || card.suit === filter;
    const haystack = [
      card.name,
      card.name_cn,
      card.element,
      card.astrology,
      ...(card.upright?.keywords || []),
      ...(card.reversed?.keywords || [])
    ].join(' ').toLowerCase();

    return matchesFilter && (!search || haystack.includes(search));
  });

  if (!cards.length) {
    deckContainer.innerHTML = '<div class="history-empty">没有匹配的牌</div>';
    return;
  }

  deckContainer.innerHTML = cards.map(card => {
    const suitName = getSuitName(card);
    return `
      <article class="learn-card">
        <img src="${card.image}" alt="${card.name_cn}" loading="lazy">
        <div class="learn-card-body">
          <div class="learn-card-title">
            <strong>${card.name_cn}</strong>
            <span>${card.name}</span>
          </div>
          <div class="learn-card-meta">
            <span>${suitName}</span>
            <span>${card.element || '无元素'}</span>
            <span>${card.astrology || '无星象'}</span>
          </div>
          <div class="learn-meaning">
            <b>正位</b>
            <p>${(card.upright?.keywords || []).join(' · ')}</p>
            <small>${card.upright?.meaning || ''}</small>
          </div>
          <div class="learn-meaning">
            <b>逆位</b>
            <p>${(card.reversed?.keywords || []).join(' · ')}</p>
            <small>${card.reversed?.meaning || ''}</small>
          </div>
        </div>
      </article>
    `;
  }).join('');
}

function getSuitName(card) {
  if (card.type === 'major') return '大阿尔卡纳';
  const names = {
    wands: '权杖',
    cups: '圣杯',
    swords: '宝剑',
    pentacles: '星币'
  };
  return names[card.suit] || '小阿尔卡纳';
}

function renderDailyTrends(history) {
  const trends = document.getElementById('daily-trends');
  const dailyRecords = history
    .filter(item => item.recordType === 'daily' || item.spreadId === 'daily')
    .slice(0, 30);

  if (!dailyRecords.length) {
    trends.innerHTML = '';
    return;
  }

  const totalCards = dailyRecords.flatMap(item => item.rawCards || []);
  const uprightCount = totalCards.filter(card => card.orientation === 'upright').length;
  const reversedCount = totalCards.filter(card => card.orientation === 'reversed').length;
  const suitCounts = totalCards.reduce((acc, card) => {
    const key = card.type === 'major' ? 'major' : card.suit;
    acc[key] = (acc[key] || 0) + 1;
    return acc;
  }, {});
  const dominantSuit = Object.entries(suitCounts).sort((a, b) => b[1] - a[1])[0];
  const suitLabels = {
    major: '大阿尔卡纳',
    wands: '权杖',
    cups: '圣杯',
    swords: '宝剑',
    pentacles: '星币'
  };

  trends.innerHTML = `
    <div class="trend-title">每日塔罗趋势（最近 ${dailyRecords.length} 次）</div>
    <div class="trend-grid">
      <div><strong>${uprightCount}</strong><span>正位</span></div>
      <div><strong>${reversedCount}</strong><span>逆位</span></div>
      <div><strong>${dominantSuit ? suitLabels[dominantSuit[0]] : '-'}</strong><span>高频主题</span></div>
    </div>
  `;
}

/**
 * 渲染历史记录列表
 */
function renderHistoryList(searchQuery = '') {
  const historyList = document.getElementById('history-list');
  const history = getHistory();
  const visibleHistory = history.filter(item => !item.hidden);
  renderDailyTrends(visibleHistory);
  
  // 过滤历史记录
  const filteredHistory = searchQuery
    ? visibleHistory.filter(item => 
        item.question.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : visibleHistory;
  
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
    const tags = item.tags || [];
    const hasNote = Boolean(item.note);
    
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
            <button class="history-item-btn" onclick="editJournal('${item.id}')" title="日记">
              📝
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
        ${tags.length || hasNote ? `
          <div class="history-journal">
            ${tags.map(tag => `<span>${tag}</span>`).join('')}
            ${hasNote ? '<em>已记录日记</em>' : ''}
          </div>
        ` : ''}
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
 * 隐藏历史记录
 */
function handleClearHistory() {
  if (confirm('将隐藏当前页面中的所有历史记录，但不会删除本地或后台保存的数据。确定继续吗？')) {
    hideAllHistory();
    renderHistoryList();
  }
}

/**
 * 切换收藏状态
 */
window.toggleFavorite = function(id) {
  if (toggleHistoryFavorite(id)) {
    renderHistoryList();
  }
};

window.editJournal = function(id) {
  showJournalModal(id);
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
