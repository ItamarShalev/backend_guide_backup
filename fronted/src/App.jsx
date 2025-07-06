import { useState } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import Layout from './components/Layout';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import TodosPage from './pages/TodosPage';
import './App.css';

const AppContent = () => {
  const { isAuthenticated, loading } = useAuth();
  const [authMode, setAuthMode] = useState('login');

  if (loading) {
    return (
      <Layout>
        <div className="loading-screen">
          <div className="spinner"></div>
          <p>Loading...</p>
        </div>
      </Layout>
    );
  }

  if (!isAuthenticated) {
    return (
      <Layout>
        {authMode === 'login' ? (
          <LoginPage switchToRegister={() => setAuthMode('register')} />
        ) : (
          <RegisterPage switchToLogin={() => setAuthMode('login')} />
        )}
      </Layout>
    );
  }

  return (
    <Layout>
      <TodosPage />
    </Layout>
  );
};

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
