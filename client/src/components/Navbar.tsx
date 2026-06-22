import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar: React.FC = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="container">
        <div className="navbar-brand">
          <Link to={isAuthenticated ? (user?.role === 'admin' ? '/admin/users' : '/dashboard') : '/'}>
            AdaRSS <span></span>
          </Link>
        </div>
        {isAuthenticated && (
          <div className="navbar-right">
            {user?.role === 'admin' && (
              <>
                <Link to="/dashboard" className="nav-link">Dashboard</Link>
                <Link to="/admin/users" className="nav-link">Users</Link>
                <Link to="/admin/keys" className="nav-link">API Keys</Link>
              </>
            )}
            <span>{user?.email}</span>
            <button onClick={handleLogout} className="btn-logout">
              Logout
            </button>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;