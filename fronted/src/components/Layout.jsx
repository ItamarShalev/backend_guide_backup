import { useAuth } from '../context/AuthContext';
import './Layout.css';

const Layout = ({ children }) => {
  const { user, logout, isAuthenticated } = useAuth();

  return (
    <div className="layout">
      <header className="header">
        <div className="header-content">
          <h1 className="logo">TodoApp</h1>
          {isAuthenticated && (
            <div className="header-actions">
              <span className="welcome">Welcome back!</span>
              <button onClick={logout} className="logout-btn">
                Logout
              </button>
            </div>
          )}
        </div>
      </header>
      <main className="main-content">
        {children}
      </main>
    </div>
  );
};

export default Layout;
