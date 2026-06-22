import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import AdminUsers from './components/AdminUsers';
import AdminKeys from './components/AdminKeys';

const PrivateRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
};

const AppRoutes: React.FC = () => {
  const { isAuthenticated, user } = useAuth();

  return (
    <Routes>
      <Route path="/login" element={isAuthenticated ? <Navigate to={user?.role === 'admin' ? '/dashboard' : '/dashboard'} /> : <Login />} />
      <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
      <Route path="/admin/users" element={<PrivateRoute><AdminUsers /></PrivateRoute>} />
      <Route path="/admin/keys" element={<PrivateRoute><AdminKeys /></PrivateRoute>} />
      <Route path="/admin" element={<Navigate to={isAuthenticated ? '/admin/users' : '/login'} />} />
      <Route path="/" element={isAuthenticated ? <Navigate to={'/dashboard'} /> : <Navigate to="/login" />} />
      {/* <Route path="/" element={isAuthenticated ? <Navigate to={user?.role === 'admin' ? '/admin/users' : '/dashboard'} /> : <Navigate to="/login" />} /> */}
    </Routes>
  );
};

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;