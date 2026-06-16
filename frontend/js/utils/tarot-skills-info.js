/**
 * Tarot Skills 信息展示
 */

const TAROT_SKILLS_INFO = {
  title: "🔮 Tarot Skills - LLM 行为校正模式",
  description: "每张大阿尔卡纳牌对应一种独特的思维模式，用于打破 AI 的默认行为模式，提供更深刻、更多元的解读。",
  skills: [
    { id: 0, name: "愚者", skill: "初学者模式", breaks: "专家偏见" },
    { id: 1, name: "魔术师", skill: "资源利用者", breaks: "工具依赖" },
    { id: 2, name: "女祭司", skill: "直觉洞察", breaks: "过度理性" },
    { id: 3, name: "皇后", skill: "养育者", breaks: "效率至上" },
    { id: 4, name: "皇帝", skill: "结构建立者", breaks: "混乱无序" },
    { id: 5, name: "教皇", skill: "传统智慧", breaks: "盲目创新" },
    { id: 6, name: "恋人", skill: "价值选择", breaks: "价值模糊" },
    { id: 7, name: "战车", skill: "意志驱动", breaks: "被动等待" },
    { id: 8, name: "力量", skill: "温柔力量", breaks: "强硬对抗" },
    { id: 9, name: "隐士", skill: "独处反思", breaks: "外部依赖" },
    { id: 10, name: "命运之轮", skill: "周期认知", breaks: "线性思维" },
    { id: 11, name: "正义", skill: "因果分析", breaks: "情感偏见" },
    { id: 12, name: "倒吊人", skill: "视角转换", breaks: "固定视角" },
    { id: 13, name: "死神", skill: "混沌代理", breaks: "过度讨好" },
    { id: 14, name: "节制", skill: "平衡调和", breaks: "极端化" },
    { id: 15, name: "恶魔", skill: "欲望解剖", breaks: "道德说教" },
    { id: 16, name: "高塔", skill: "破坏建设", breaks: "维持现状" },
    { id: 17, name: "星星", skill: "希望守护", breaks: "悲观主义" },
    { id: 18, name: "月亮", skill: "不确定性拥抱", breaks: "过度确定" },
    { id: 19, name: "太阳", skill: "清晰照亮", breaks: "过度复杂" },
    { id: 20, name: "审判", skill: "觉醒召唤", breaks: "沉睡麻木" },
    { id: 21, name: "世界", skill: "整合完成", breaks: "片面分析" }
  ]
};

/**
 * 显示 Tarot Skills 信息模态框
 */
export function showTarotSkillsInfo() {
  const modal = document.createElement('div');
  modal.className = 'modal active';
  modal.id = 'tarot-skills-modal';

  const skillsHTML = TAROT_SKILLS_INFO.skills.map(skill => `
    <div class="skill-item" style="padding: 12px; margin-bottom: 10px; background: var(--color-bg-primary); border-radius: 8px; border-left: 3px solid var(--color-accent-primary);">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
          <strong style="color: var(--color-gold); font-size: 1rem;">${skill.id}. ${skill.name}</strong>
          <span style="color: var(--color-accent-primary); margin-left: 10px; font-size: 0.9rem;">${skill.skill}</span>
        </div>
        <div style="font-size: 0.85rem; color: var(--color-text-muted);">
          打破: ${skill.breaks}
        </div>
      </div>
    </div>
  `).join('');

  modal.innerHTML = `
    <div class="modal-content" style="max-width: 900px;">
      <div class="modal-header">
        <h2>${TAROT_SKILLS_INFO.title}</h2>
        <button class="modal-close" id="skills-modal-close">&times;</button>
      </div>
      <div class="modal-body">
        <div style="background: rgba(157, 78, 221, 0.1); padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid var(--color-accent-primary);">
          <p style="margin: 0; line-height: 1.6;">${TAROT_SKILLS_INFO.description}</p>
          <p style="margin: 10px 0 0 0; font-size: 0.9rem; color: var(--color-text-secondary);">
            💡 <strong>自动应用</strong>：当抽到大阿尔卡纳牌时，系统会自动应用对应的思维模式，让 AI 打破常规，提供更独特的洞察。
          </p>
        </div>

        <h3 style="color: var(--color-gold); margin-bottom: 15px; font-size: 1.2rem;">22 种思维模式</h3>
        <div style="max-height: 50vh; overflow-y: auto;">
          ${skillsHTML}
        </div>

        <div style="margin-top: 20px; padding: 15px; background: rgba(255, 215, 0, 0.1); border-radius: 8px; text-align: center;">
          <p style="margin: 0; color: var(--color-text-secondary); font-size: 0.9rem;">
            🎴 每次占卜抽到大阿尔卡纳时，都会应用对应的技能模式<br>
            让 AI 从不同的角度为你解读，打破思维定式
          </p>
        </div>
      </div>
    </div>
  `;

  document.body.appendChild(modal);

  // 关闭事件
  document.getElementById('skills-modal-close').onclick = () => {
    document.body.removeChild(modal);
  };

  modal.onclick = (e) => {
    if (e.target === modal) {
      document.body.removeChild(modal);
    }
  };
}

/**
 * 获取技能信息
 */
export function getSkillInfo(cardId) {
  return TAROT_SKILLS_INFO.skills.find(s => s.id === cardId);
}
