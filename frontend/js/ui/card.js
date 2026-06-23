/**
 * 卡牌渲染（带 3D 翻转动画）
 */

// Tarot Skills 映射（简化版）
const TAROT_SKILLS_MAP = {
  0: "初学者模式", 1: "资源利用者", 2: "直觉洞察", 3: "养育者",
  4: "结构建立者", 5: "传统智慧", 6: "价值选择", 7: "意志驱动",
  8: "温柔力量", 9: "独处反思", 10: "周期认知", 11: "因果分析",
  12: "视角转换", 13: "混沌代理", 14: "平衡调和", 15: "欲望解剖",
  16: "破坏建设", 17: "希望守护", 18: "不确定性拥抱", 19: "清晰照亮",
  20: "觉醒召唤", 21: "整合完成"
};

function escapeHtml(value) {
  return String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function getOrientationLabel(orientation) {
  return orientation === 'upright' ? '正位' : '逆位';
}

/**
 * 渲染卡牌（带翻转动画）
 */
export function renderCards(cards) {
  const container = document.getElementById('cards-container');
  container.innerHTML = '';

  // 检查是否有大阿尔卡纳（用于 Tarot Skills）
  const majorCards = cards.filter(c => (c.card || c).type === 'major');
  const hasMajor = majorCards.length > 0;

  // 如果有大阿尔卡纳，显示技能提示
  if (hasMajor) {
    const primaryMajor = majorCards[0].card || majorCards[0];
    const skillName = TAROT_SKILLS_MAP[primaryMajor.id];
    if (skillName) {
      const skillBanner = document.createElement('div');
      skillBanner.className = 'tarot-skill-banner';
      skillBanner.innerHTML = `
        <div class="skill-orb">🎴</div>
        <div class="skill-copy">
          <strong>Tarot Skill 已激活</strong>
          <span>${escapeHtml(primaryMajor.name_cn)} · ${escapeHtml(skillName)}</span>
        </div>
      `;
      container.appendChild(skillBanner);
    }
  }
  
  cards.forEach((cardData, index) => {
    const card = cardData.card || cardData;
    const orientation = cardData.orientation;
    const meaningData = card[orientation];
    const orientationLabel = getOrientationLabel(orientation);
    const keywords = meaningData?.keywords || [];

    const cardShell = document.createElement('article');
    cardShell.className = `drawn-card ${orientation === 'reversed' ? 'is-reversed' : 'is-upright'}`;
    cardShell.style.setProperty('--card-delay', `${index * 90}ms`);
    
    // 创建翻转容器
    const flipContainer = document.createElement('div');
    flipContainer.className = 'card-flip-container';
    
    const flipInner = document.createElement('div');
    flipInner.className = 'card-flip-inner';
    
    // 卡牌正面（背面）
    const flipFront = document.createElement('div');
    flipFront.className = 'card-flip-front';
    flipFront.innerHTML = `
      <div class="card-back-mark">✦</div>
      <div class="card-back-ring"></div>
    `;
    
    // 卡牌背面（实际内容）
    const flipBack = document.createElement('div');
    flipBack.className = 'card-flip-back';
    
    const cardEl = document.createElement('div');
    cardEl.className = 'card';

    // 如果有图片URL，显示图片
    if (card.image) {
      cardEl.innerHTML = `
        <img src="${escapeHtml(card.image)}" alt="${escapeHtml(card.name_cn)}" class="card-image ${orientation === 'reversed' ? 'card-image-reversed' : ''}"
             onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
        <div class="card-text-fallback" style="display: none;">
          <div class="card-name">${escapeHtml(card.name_cn)}</div>
          <div class="card-name-en">${escapeHtml(card.name)}</div>
          <div class="card-orientation">${orientationLabel}</div>
          <div class="card-keywords">${escapeHtml(keywords.join(' · '))}</div>
        </div>
        <div class="card-overlay">
          <div class="card-name">${escapeHtml(card.name_cn)}</div>
          <div class="card-orientation">${orientationLabel}</div>
        </div>
      `;
    } else {
      // 没有图片时显示文字版本
      cardEl.innerHTML = `
        <div class="card-name">${escapeHtml(card.name_cn)}</div>
        <div class="card-name-en">${escapeHtml(card.name)}</div>
        <div class="card-orientation">${orientationLabel}</div>
        <div class="card-keywords">${escapeHtml(keywords.join(' · '))}</div>
      `;
    }
    
    flipBack.appendChild(cardEl);
    flipInner.appendChild(flipFront);
    flipInner.appendChild(flipBack);
    flipContainer.appendChild(flipInner);
    cardShell.innerHTML = `
      <div class="drawn-card-topline">
        <span class="card-index">#${index + 1}</span>
        <span class="orientation-chip">${orientationLabel}</span>
      </div>
    `;
    cardShell.appendChild(flipContainer);
    cardShell.insertAdjacentHTML('beforeend', `
      <div class="drawn-card-meta">
        <strong>${escapeHtml(card.name_cn)}</strong>
        <span>${escapeHtml(card.name || 'Tarot Card')}</span>
        ${keywords.length ? `<p>${escapeHtml(keywords.slice(0, 4).join(' · '))}</p>` : ''}
      </div>
    `);
    
    // 添加到容器
    container.appendChild(cardShell);
    
    // 延迟触发翻转动画
    setTimeout(() => {
      flipContainer.classList.add('flipping');
      setTimeout(() => {
        flipInner.style.transform = 'rotateY(180deg)';
      }, 50);
    }, index * 300); // 每张牌延迟 300ms
  });
}

/**
 * 清空卡牌
 */
export function clearCards() {
  const container = document.getElementById('cards-container');
  container.innerHTML = `
    <div class="empty-state">
      <div class="empty-state-icon">🌟</div>
      <div class="empty-state-text">开始占卜后，卡牌将在这里显示</div>
    </div>
  `;
}
