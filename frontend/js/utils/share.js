/**
 * 分享功能
 */

/**
 * 生成分享卡片
 */
export async function generateShareCard(question, cards, reading) {
  try {
    // 创建隐藏的分享卡片容器
    const shareCard = document.createElement('div');
    shareCard.id = 'share-card';
    shareCard.style.cssText = `
      position: fixed;
      left: -9999px;
      width: 600px;
      padding: 40px;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
      border: 2px solid #9d4edd;
      border-radius: 20px;
      box-shadow: 0 0 40px rgba(157, 78, 221, 0.5);
      font-family: 'Crimson Text', serif;
    `;
    
    // 构建卡片内容
    const cardNames = cards.map(c => {
      const orientation = c.orientation === 'upright' ? '正位' : '逆位';
      const name = c.name_cn || c.cardName || c.name || '未知卡牌';
      return `${name} (${orientation})`;
    }).join('、');
    
    // 截取解读前200字
    const readingPreview = reading.length > 200 
      ? reading.substring(0, 200) + '...' 
      : reading;
    
    shareCard.innerHTML = `
      <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="color: #ffd700; font-size: 2rem; margin: 0;">⭐ AI 塔罗占卜 🌙</h1>
      </div>
      
      <div style="background: rgba(26, 26, 47, 0.8); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h2 style="color: #9d4edd; font-size: 1.2rem; margin-bottom: 10px;">🔮 占卜问题</h2>
        <p style="color: #e0e0e0; font-size: 1.1rem; line-height: 1.6;">${question}</p>
      </div>
      
      <div style="background: rgba(26, 26, 47, 0.8); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h2 style="color: #9d4edd; font-size: 1.2rem; margin-bottom: 10px;">🃏 抽取的牌</h2>
        <p style="color: #ffd700; font-size: 1rem;">${cardNames}</p>
      </div>
      
      <div style="background: rgba(26, 26, 47, 0.8); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h2 style="color: #9d4edd; font-size: 1.2rem; margin-bottom: 10px;">✨ 解读摘要</h2>
        <p style="color: #e0e0e0; font-size: 0.95rem; line-height: 1.8; white-space: pre-wrap;">${readingPreview}</p>
      </div>
      
      <div style="text-align: center; color: #666; font-size: 0.9rem;">
        <p style="margin: 0;">愿塔罗之光照亮你的前路 ✨</p>
      </div>
    `;
    
    document.body.appendChild(shareCard);
    
    // 使用 html2canvas 生成图片
    const canvas = await html2canvas(shareCard, {
      backgroundColor: '#0a0a0f',
      scale: 2
    });
    
    // 移除临时元素
    document.body.removeChild(shareCard);
    
    return canvas;
  } catch (error) {
    console.error('生成分享卡片失败:', error);
    throw error;
  }
}

/**
 * 下载分享卡片
 */
export function downloadShareCard(canvas) {
  const link = document.createElement('a');
  link.download = `tarot-reading-${Date.now()}.png`;
  link.href = canvas.toDataURL('image/png');
  link.click();
}

/**
 * 复制到剪贴板（如果支持）
 */
export async function copyToClipboard(canvas) {
  try {
    canvas.toBlob(async (blob) => {
      await navigator.clipboard.write([
        new ClipboardItem({ 'image/png': blob })
      ]);
      alert('✅ 已复制到剪贴板！');
    });
  } catch (error) {
    console.error('复制失败:', error);
    alert('❌ 浏览器不支持复制图片，请使用下载功能');
  }
}

/**
 * 分享占卜结果
 */
export async function shareReading(question, cards, reading) {
  try {
    // 显示加载提示
    const loadingDiv = document.createElement('div');
    loadingDiv.innerHTML = `
      <div style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); 
                  background: rgba(26, 26, 46, 0.95); padding: 30px; border-radius: 15px; 
                  border: 2px solid #9d4edd; z-index: 9999; text-align: center;">
        <div class="spinner" style="margin: 0 auto 15px;"></div>
        <p style="color: #e0e0e0;">正在生成分享卡片...</p>
      </div>
    `;
    document.body.appendChild(loadingDiv);
    
    // 生成卡片
    const canvas = await generateShareCard(question, cards, reading);
    
    // 移除加载提示
    document.body.removeChild(loadingDiv);
    
    // 显示分享选项
    showShareOptions(canvas);
  } catch (error) {
    console.error('分享失败:', error);
    alert('❌ 生成分享卡片失败，请稍后重试');
  }
}

/**
 * 显示分享选项对话框
 */
function showShareOptions(canvas) {
  const modal = document.createElement('div');
  modal.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
  `;
  
  modal.innerHTML = `
    <div style="background: #1a1a2e; padding: 30px; border-radius: 15px; 
                border: 2px solid #9d4edd; max-width: 90%; max-height: 90%; overflow: auto;">
      <h2 style="color: #ffd700; margin-bottom: 20px; text-align: center;">📤 分享占卜结果</h2>
      
      <div style="margin-bottom: 20px; text-align: center;">
        <img src="${canvas.toDataURL('image/png')}" 
             style="max-width: 100%; border-radius: 10px; box-shadow: 0 0 20px rgba(157, 78, 221, 0.3);">
      </div>
      
      <div style="display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
        <button id="share-download" class="btn" style="width: auto; padding: 12px 30px;">
          💾 下载图片
        </button>
        <button id="share-copy" class="btn btn-secondary" style="width: auto; padding: 12px 30px;">
          📋 复制图片
        </button>
        <button id="share-close" class="btn btn-secondary" style="width: auto; padding: 12px 30px;">
          ✖️ 关闭
        </button>
      </div>
    </div>
  `;
  
  document.body.appendChild(modal);
  
  // 事件监听
  document.getElementById('share-download').onclick = () => {
    downloadShareCard(canvas);
  };
  
  document.getElementById('share-copy').onclick = async () => {
    await copyToClipboard(canvas);
  };
  
  document.getElementById('share-close').onclick = () => {
    document.body.removeChild(modal);
  };
  
  // 点击背景关闭
  modal.onclick = (e) => {
    if (e.target === modal) {
      document.body.removeChild(modal);
    }
  };
}
