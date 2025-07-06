import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import './AuthPages.css';

const RegisterPage = ({ switchToLogin }) => {
  const [userData, setUserData] = useState({ username: '', password: '', confirmPassword: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (userData.password !== userData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (userData.password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    setLoading(true);

    const result = await register({
      username: userData.username,
      password: userData.password,
    });

    if (result.success) {
      alert('Registration successful! Please login.');
      switchToLogin();
    } else {
      setError(result.error);
    }
    setLoading(false);
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2 className="auth-title">Create Account</h2>
        <p className="auth-subtitle">Join us today</p>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              type="text"
              value={userData.username}
              onChange={(e) => setUserData({...userData, username: e.target.value})}
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={userData.password}
              onChange={(e) => setUserData({...userData, password: e.target.value})}
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <input
              id="confirmPassword"
              type="password"
              value={userData.confirmPassword}
              onChange={(e) => setUserData({...userData, confirmPassword: e.target.value})}
              required
              disabled={loading}
            />
          </div>

          <button type="submit" className="auth-button" disabled={loading}>
            {loading ? 'Creating Account...' : 'Sign Up'}
          </button>
        </form>

        <p className="auth-switch">
          Already have an account?{' '}
          <button onClick={switchToLogin} className="switch-btn">
            Sign in
          </button>
        </p>
      </div>
    </div>
  );
};

export default RegisterPage;
