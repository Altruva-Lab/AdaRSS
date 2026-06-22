import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import Navbar from './Navbar';

interface APIKey {
  key: string;
  name: string;
  is_active: boolean;
  created_at: string;
  usage_count: number;
  owner_email: string | null;
}

interface User {
  id: number;
  email: string;
}

const AdminKeys: React.FC = () => {
  const { user } = useAuth();
  const [keys, setKeys] = useState<APIKey[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [newKeyName, setNewKeyName] = useState('');
  const [selectedUserId, setSelectedUserId] = useState<number | ''>('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [keysRes, usersRes] = await Promise.all([
        api.get('/admin/keys'),
        api.get('/admin/users'),
      ]);
      setKeys(keysRes.data);
      setUsers(usersRes.data);
    } catch (err: any) {
      setMessage(err.response?.data?.detail || 'Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const generateKey = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newKeyName.trim()) {
      setMessage('Please enter a key name');
      return;
    }
    if (!selectedUserId) {
      setMessage('Please select a user');
      return;
    }
    setLoading(true);
    try {
      const userEmail = users.find(u => u.id === selectedUserId)?.email;
      if (!userEmail) {
        setMessage('Selected user not found');
        return;
      }
      await api.post('/admin/generate-key', null, {
        params: { name: newKeyName, user_email: userEmail }
      });
      setNewKeyName('');
      setSelectedUserId('');
      setMessage('✅ API key generated for user');
      fetchData();
    } catch (err: any) {
      setMessage(err.response?.data?.detail || 'Generation failed');
    } finally {
      setLoading(false);
    }
  };

  const revokeKey = async (keyId: string) => {
    if (!window.confirm('Revoke this API key? It will stop working immediately.')) return;
    try {
      await api.delete(`/api-keys/${keyId}`);
      setKeys(keys.map(k => k.key === keyId ? { ...k, is_active: false } : k));
      setMessage('✅ Key revoked');
    } catch (err: any) {
      setMessage(err.response?.data?.detail || 'Revoke failed');
    }
  };

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
        <h1>Admin – API Keys</h1>
        <p>View and manage all API keys across all clients.</p>

        {/* Generate Key for User */}
        <div className="card">
          <h2>🔑 Generate Key for Client</h2>
          <form onSubmit={generateKey} className="generate-form">
            <div className="form-group">
              <label>Client</label>
              <select
                value={selectedUserId}
                onChange={(e) => setSelectedUserId(Number(e.target.value))}
                required
              >
                <option value="">Select a client</option>
                {users.map((u) => (
                  <option key={u.id} value={u.id}>
                    {u.email}
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Key Name</label>
              <input
                type="text"
                placeholder="e.g., Production"
                value={newKeyName}
                onChange={(e) => setNewKeyName(e.target.value)}
                required
              />
            </div>
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Generating...' : 'Generate Key'}
            </button>
          </form>
        </div>

        {/* All Keys Table */}
        <div className="card">
          <h2>🔐 All API Keys</h2>
          {loading && <p>Loading...</p>}
          {keys.length === 0 && !loading && (
            <p className="empty-state">No API keys found.</p>
          )}
          <div className="table-responsive">
            <table className="keys-table">
              <thead>
                <tr>
                  <th>Owner</th>
                  <th>Name</th>
                  <th>Key (truncated)</th>
                  <th>Status</th>
                  <th>Usage</th>
                  <th>Created</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {keys.map((key) => (
                  <tr key={key.key}>
                    <td>{key.owner_email || 'Unassigned'}</td>
                    <td><strong>{key.name}</strong></td>
                    <td><code>{key.key.slice(0, 10)}...</code></td>
                    <td>
                      <span className={key.is_active ? 'badge-active' : 'badge-inactive'}>
                        {key.is_active ? '✅ Active' : '❌ Revoked'}
                      </span>
                    </td>
                    <td>{key.usage_count.toLocaleString()} requests</td>
                    <td>{new Date(key.created_at).toLocaleDateString()}</td>
                    <td>
                      {key.is_active && (
                        <button onClick={() => revokeKey(key.key)} className="btn-danger">
                          Revoke
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {message && <div className={`message ${message.includes('✅') ? 'success' : 'error'}`}>{message}</div>}
      </div>
    </div>
  );
};

export default AdminKeys;