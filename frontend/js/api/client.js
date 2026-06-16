/**
 * API 客户端
 */
import { CONFIG } from '../config.js';

class APIClient {
  constructor() {
    this.baseURL = CONFIG.API_BASE_URL;
  }
  
  /**
   * GET 请求
   */
  async get(endpoint) {
    try {
      const response = await fetch(`${this.baseURL}${endpoint}`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.error('GET 请求失败:', error);
      throw error;
    }
  }
  
  /**
   * POST 请求
   */
  async post(endpoint, data) {
    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('POST 请求失败:', error);
      throw error;
    }
  }
  
  /**
   * 流式 POST 请求（SSE）
   */
  async streamPost(endpoint, data, onChunk, onDone, onError) {
    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop();
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            try {
              const parsed = JSON.parse(data);
              
              if (parsed.type === 'content') {
                onChunk(parsed.text);
              } else if (parsed.type === 'done') {
                if (onDone) onDone();
              } else if (parsed.type === 'error') {
                if (onError) onError(parsed.error);
              }
            } catch (e) {
              console.error('解析 SSE 数据失败:', e);
            }
          }
        }
      }
    } catch (error) {
      console.error('流式请求失败:', error);
      if (onError) onError(error.message);
      throw error;
    }
  }
}

export default new APIClient();
