/** @jsxImportSource @emotion/react */
import React, { useState } from 'react';
import { Input } from 'antd';
import { Link, useNavigate } from 'react-router-dom';
import * as styles from '../styles/LoginPage.styles';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const navigate = useNavigate();

  const handleLogin = async () => {
    if (!email || !password) {
      setMessage('아이디와 비밀번호를 입력해 주세요.');
      return;
    }

    const loginData = { email, password };

    try {
      const response = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(loginData),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage('로그인 성공!');
        // 로그인 성공 시 리디렉션 예시 (메인 페이지로 이동)
        navigate('/home');
      } else {
        setMessage(data.detail || '로그인 실패');
      }
    } catch (error) {
      setMessage(error.message || '서버 오류');
    }
  };

  return (
    <div css={styles.container}>
      <h2 css={styles.title}>LOGIN</h2>
      <div css={styles.form}>
        <div css={styles.row}>
          <label css={styles.label}>아이디</label>
          <Input
            placeholder="이메일을 입력하세요."
            css={styles.input}
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div css={styles.row}>
          <label css={styles.label}>비밀번호</label>
          <Input.Password
            placeholder="비밀번호를 입력하세요."
            css={styles.input}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <div css={styles.passwordReset}>
          <Link to="/find-password" css={styles.passwordLink}>
            비밀번호 찾기
          </Link>
        </div>
        <button css={styles.loginButton} onClick={handleLogin}>
          로그인
        </button>
      </div>
      {message && <p>{message}</p>} {/* 오류 메시지 표시 */}
    </div>
  );
};

export default LoginPage;
