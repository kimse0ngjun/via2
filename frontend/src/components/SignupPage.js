/** @jsxImportSource @emotion/react */
import React, { useState } from 'react';
import { Input } from 'antd';
import { useNavigate } from 'react-router-dom';
import * as styles from '../styles/SignUpPage.styles';

const SignUpPage = () => {
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [age, setAge] = useState('');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');

  const navigate = useNavigate();

  // 비밀번호 유효성 검사 함수
  const validatePassword = (password) => {
    const regex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,32}$/;
    return regex.test(password);
  };

  // 회원가입 요청 처리 함수
  const handleSignUp = async (e) => {
    e.preventDefault();

    if (!name || !email || !password || !age) {
      setMessage('모든 필드를 입력해 주세요.');
      return;
    }

    if (!validatePassword(password)) {
      setMessage('비밀번호는 8~32자이며 영문, 숫자, 특수문자를 포함해야 합니다.');
      return;
    }

    if (password !== confirmPassword) {
      setMessage('비밀번호가 일치하지 않습니다.');
      return;
    }

    const signUpData = { 
      name,
      age: Number(age) || 0, // NaN 방지
      email, 
      password, 
      password_confirm: confirmPassword
    };

    console.log('회원가입 요청 데이터:', signUpData);

    try {
      const response = await fetch('http://localhost:8000/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(signUpData),
      });

      // 응답이 JSON인지 확인
      let data;
      try {
        data = await response.json();
      } catch (jsonError) {
        throw new Error('서버 응답이 올바르지 않습니다.');
      }

      if (response.ok) {
        setMessage('회원가입이 완료되었습니다.');
        navigate('/signupsuccess');
      } else {
        setMessage(data.detail || '회원가입 실패');
      }
    } catch (error) {
      console.error(error);
      setMessage(error.message || '서버 오류');
    }
  };

  return (
    <div css={styles.container}>
      <div css={styles.title}>SIGNUP</div>
      <form css={styles.form} onSubmit={handleSignUp}>
        <div css={styles.row}>
          <label css={styles.label} htmlFor="name">이름</label>
          <input
            id="name"
            name="name"
            css={styles.input}
            type="text"
            placeholder="이름을 입력하세요"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>
        <div css={styles.row}>
          <label css={styles.label} htmlFor="age">나이</label>
          <input
            id="age"
            name="age"
            css={styles.input}
            type="number"
            placeholder="나이를 입력하세요"
            value={age}
            onChange={(e) => setAge(e.target.value)}
          />
        </div>
        <div css={styles.row}>
          <label css={styles.label} htmlFor="email">이메일</label>
          <input
            id="email"
            name="email"
            css={styles.input}
            type="email"
            placeholder="example@via.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div css={styles.row}>
          <label css={styles.label} htmlFor="password">비밀번호</label>
          <Input.Password
            id="password"
            name="password"
            css={styles.input}
            placeholder="비밀번호를 입력하세요"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <div css={styles.warningText}>
          영문/숫자/특수문자 포함 필수<br />
          8자 이상 32자 이하 입력(공백 제외)<br />
        </div>
        <div css={styles.row}>
          <label css={styles.label} htmlFor="confirmPassword">비밀번호 확인</label>
          <Input.Password
            id="confirmPassword"
            name="confirmPassword"
            css={styles.input}
            placeholder="비밀번호를 다시 입력하세요"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
        </div>
        <button type="submit" css={styles.signUpButton}>회원가입</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default SignUpPage;
