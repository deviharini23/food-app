import React, { useState } from 'react';
import axios from 'axios';

function LoginPage({ setUserId }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const handleLogin = async () => {
    if (!username || !password) {
      setError("Username and password are required.");
      return;
    }

    try {
      const res = await axios.post(
        "http://localhost:8000/register_or_login",
        { username, password },
        { headers: { "Content-Type": "application/json" } }
      );

      if (res.data.user_id) {
        setUserId(res.data.user_id);
        setMessage(res.data.message || "Logged in successfully.");
        setError('');
      } else {
        setError("Unexpected response from server.");
        setMessage('');
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed.");
      setMessage('');
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Login/Register</h2>
      <input
        value={username}
        onChange={e => setUsername(e.target.value)}
        placeholder="Username"
        style={{ margin: "5px", padding: "5px" }}
      />
      <input
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        placeholder="Password"
        style={{ margin: "5px", padding: "5px" }}
      />
      <button onClick={handleLogin} style={{ margin: "5px", padding: "5px" }}>
        Register/Login
      </button>
      {message && <p style={{ color: "green" }}>{message}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default LoginPage;
