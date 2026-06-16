/**
 * 主题切换功能
 */

const THEME_KEY = 'tarot_theme';
const THEMES = {
  DARK: 'dark',
  LIGHT: 'light'
};

/**
 * 获取当前主题
 */
export function getCurrentTheme() {
  return localStorage.getItem(THEME_KEY) || THEMES.DARK;
}

/**
 * 设置主题
 */
export function setTheme(theme) {
  const body = document.body;
  
  // 添加过渡类
  body.classList.add('theme-transitioning');
  
  // 切换主题
  if (theme === THEMES.LIGHT) {
    body.classList.add('light-theme');
  } else {
    body.classList.remove('light-theme');
  }
  
  // 保存到 localStorage
  localStorage.setItem(THEME_KEY, theme);
  
  // 更新按钮图标
  updateThemeButton(theme);
  
  // 移除过渡类
  setTimeout(() => {
    body.classList.remove('theme-transitioning');
  }, 300);
  
  console.log(`✅ 主题已切换为: ${theme === THEMES.LIGHT ? '亮色' : '暗色'}`);
}

/**
 * 切换主题
 */
export function toggleTheme() {
  const currentTheme = getCurrentTheme();
  const newTheme = currentTheme === THEMES.DARK ? THEMES.LIGHT : THEMES.DARK;
  setTheme(newTheme);
}

/**
 * 更新主题按钮图标
 */
function updateThemeButton(theme) {
  const button = document.getElementById('theme-toggle');
  if (button) {
    button.textContent = theme === THEMES.LIGHT ? '🌙' : '☀️';
    button.title = theme === THEMES.LIGHT ? '切换到暗色主题' : '切换到亮色主题';
  }
}

/**
 * 初始化主题
 */
export function initTheme() {
  const savedTheme = getCurrentTheme();
  
  // 应用保存的主题
  if (savedTheme === THEMES.LIGHT) {
    document.body.classList.add('light-theme');
  }
  
  // 更新按钮
  updateThemeButton(savedTheme);
  
  console.log(`🎨 初始化主题: ${savedTheme === THEMES.LIGHT ? '亮色' : '暗色'}`);
}
