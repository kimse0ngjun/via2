// src/services/api.js
import axios from 'axios';

// 백엔드 FastAPI 서버 주소
const API_BASE_URL = 'http://localhost:8000/api/auth';

/**
 * 회원가입
 * @param {Object} userData { name, age, email, password, password_confirm }
 */
export async function registerUser(userData) {
  const response = await axios.post(`${API_BASE_URL}/register`, userData);
  return response.data; // { message: "회원가입이 완료되었습니다." }
}

/**
 * 로그인
 * @param {Object} userData { email, password }
 */
export async function loginUser(userData) {
  const response = await axios.post(`${API_BASE_URL}/login`, userData);
  return response.data; // { access_token, user: {...} }
}
