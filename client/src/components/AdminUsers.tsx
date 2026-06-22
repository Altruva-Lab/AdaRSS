import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import Navbar from './Navbar';

interface Plan {
  id: number;
  name: string;
  max_requests: number;
  price: number;
  is_active: boolean;
}

interface User {
  id: number;
  email: string;
  role: string;
  is_active: boolean;
  created_at: string;
  plan_id: number | null;
}

const AdminDashboard: React.FC = () => {
  const { user } = useAuth();
  const [users, setUsers] = useState<User[]>([]);
  const [plans, setPlans] = useState<Plan[]>([]);
  const [loading, setLoading] = useState(false);
  const [newEmail, setNewEmail] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [selectedPlanId, setSelectedPlanId] = useState<number | ''>('');
  const [message, setMessage] = useState('');

  const fetchData = async () => {
    setLoading(true);
    try {
      const usersRes = await api.get('/admin/users');
      const plansRes = await api.get('/plans');
      setUsers(usersRes.data);
      setPlans(plansRes.data);
      if (plansRes.data.length > 0) {
        setSelectedPlanId(plansRes.data[0].id);
      }
    } catch (err: any) {
      setMessage(err.response?.data?.detail || 'Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const createUser = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedPlanId) {
      setMessage('Please select a plan');
      return;
    }
    setLoading(true);
    try {
      const userRes = await api.post('/admin/users', {
        email: newEmail,
        password: newPassword,
      });
      const newUser = userRes.data;
      await api.post(`/admin/users/${newUser.id}/plan?plan_id=${selectedPlanId}`);
      setMessage(`✅ Client ${newEmail} created with plan ${plans.find(p => p.id === selectedPlanId)?.name}`);
      setNewEmail('');
      setNewPassword('');
      fetchData();
    } catch (err: any) {
      setMessage(err.response?.data?.detail || 'Creation failed');
    } finally {
      setLoading(false);
    }
  };

  const toggleUser = async (userId: number) => {
    try {
      await api.patch(`/admin/users/${userId}/toggle`);
      fetchData();
    } catch (err: any) {
      setMessage(err.response?.data?.detail || 'Toggle failed');
    }
  };

  const changePlan = async (userId: number, planId: number) => {
    try {
      await api.post(`/admin/users/${userId}/plan?plan_id=${planId}`);
      fetchData();
    } catch (err: any) {
      setMessage(err.response?.data?.detail || 'Plan change failed');
    }
  };

  // Filter out admin user from list
  const filteredUsers = users.filter(u => u.role !== 'admin');

  if (!user || user.role !== 'admin') {
    return (
      <>
        <Navbar />
        <div className="container" style={{ paddingTop: '2rem' }}>
          <h2>Access Denied</h2>
          <p>You need administrator privileges to view this page.</p>
        </div>
      </>
    );
  }

  return (
    <div>
      <Navbar />
      <div className="container dashboard">
        <h1>Admin Dashboard</h1>
        <p>Manage clients, plans, and API access.</p>

        <div className="card">
          <h2>Create New Client</h2>
          <form onSubmit={createUser} className="create-form">
            <div className="form-row">
              <div className="form-group">
                <label>Email</label>
                <input
                  type="email"
                  placeholder="client@example.com"
                  value={newEmail}
                  onChange={(e) => setNewEmail(e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label>Temporary Password</label>
                <input
                  type="password"
                  placeholder="Temp password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  required
                  minLength={6}
                />
              </div>
              <div className="form-group">
                <label>Plan</label>
                <select
                  value={selectedPlanId}
                  onChange={(e) => setSelectedPlanId(Number(e.target.value))}
                  required
                >
                  <option value="">Select a plan</option>
                  {plans.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.name} ({p.max_requests} req/month)
                    </option>
                  ))}
                </select>
              </div>
            </div>
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Creating...' : 'Create Client'}
            </button>
          </form>
          {message && <p className="message">{message}</p>}
        </div>

        <div className="card">
          <h2>All Clients</h2>
          {loading && <p>Loading...</p>}
          {filteredUsers.length === 0 && !loading && <p>No clients yet.</p>}
          <div className="table-responsive">
            <table className="users-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Email</th>
                  <th>Plan</th>
                  <th>Active</th>
                  <th>Created</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredUsers.map((u) => {
                  const userPlan = plans.find(p => p.id === u.plan_id);
                  return (
                    <tr key={u.id}>
                      <td>{u.id}</td>
                      <td>{u.email}</td>
                      <td>
                        <select
                          value={u.plan_id || ''}
                          onChange={(e) => changePlan(u.id, Number(e.target.value))}
                          disabled={loading}
                        >
                          <option value="">No plan</option>
                          {plans.map(p => (
                            <option key={p.id} value={p.id}>
                              {p.name}
                            </option>
                          ))}
                        </select>
                      </td>
                      <td>{u.is_active ? '✅ Active' : '❌ Inactive'}</td>
                      <td>{new Date(u.created_at).toLocaleDateString()}</td>
                      <td>
                        <button
                          onClick={() => toggleUser(u.id)}
                          className={u.is_active ? 'btn-danger' : 'btn-success'}
                          disabled={loading}
                        >
                          {u.is_active ? 'Deactivate' : 'Activate'}
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {message && <div className="message">{message}</div>}
      </div>
    </div>
  );
};

export default AdminDashboard;