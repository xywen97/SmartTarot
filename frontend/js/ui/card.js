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
  const skillSlot = document.getElementById('tarot-skill-slot');
  container.innerHTML = '';
  if (skillSlot) {
    skillSlot.innerHTML = '';
  }
  const shouldMarquee = cards.length > 2;

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
      if (skillSlot) {
        skillSlot.appendChild(skillBanner);
      }
    }
  }
  
  const cardsViewport = document.createElement('div');
  cardsViewport.className = `cards-marquee ${shouldMarquee ? 'is-animated' : ''}`;
  const cardsTrack = document.createElement('div');
  cardsTrack.className = 'cards-track';
  cardsTrack.style.setProperty('--marquee-duration', `${Math.max(cards.length, 3) * 5}s`);
  cardsViewport.appendChild(cardsTrack);
  container.appendChild(cardsViewport);

  function createCardElement(cardData, index, isClone = false) {
    const card = cardData.card || cardData;
    const orientation = cardData.orientation;
    const meaningData = card[orientation];
    const orientationLabel = getOrientationLabel(orientation);
    const keywords = meaningData?.keywords || [];

    const cardShell = document.createElement('article');
    cardShell.className = `drawn-card ${orientation === 'reversed' ? 'is-reversed' : 'is-upright'}`;
    cardShell.style.setProperty('--card-delay', `${index * 90}ms`);
    if (isClone) {
      cardShell.setAttribute('aria-hidden', 'true');
    }
    
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
    
    cardShell.innerHTML = `
      <div class="drawn-card-topline">
        <span class="card-index">#${index + 1}</span>
        <span class="orientation-chip">${orientationLabel}</span>
      </div>
    `;
    cardShell.appendChild(cardEl);
    cardShell.insertAdjacentHTML('beforeend', `
      <div class="drawn-card-meta">
        <strong>${escapeHtml(card.name_cn)}</strong>
        <span>${escapeHtml(card.name || 'Tarot Card')}</span>
        ${keywords.length ? `<p>${escapeHtml(keywords.slice(0, 4).join(' · '))}</p>` : ''}
      </div>
    `);
    
    // 添加到横向轨道
    cardsTrack.appendChild(cardShell);
    
  }

  cards.forEach((cardData, index) => {
    createCardElement(cardData, index);
  });

  if (shouldMarquee) {
    cards.forEach((cardData, index) => {
      createCardElement(cardData, index, true);
    });
  }
}

/**
 * 清空卡牌
 */
export function clearCards() {
  const container = document.getElementById('cards-container');
  const skillSlot = document.getElementById('tarot-skill-slot');
  if (skillSlot) {
    skillSlot.innerHTML = '';
  }
  container.innerHTML = `
    <div class="empty-state">
      <div class="empty-state-icon">🌟</div>
      <div class="empty-state-text">开始占卜后，卡牌将在这里显示</div>
    </div>
  `;
}
