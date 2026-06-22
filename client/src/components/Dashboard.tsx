import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import Navbar from './Navbar';
import SkillInput from './SkillInput';
import AdviceDisplay from './AdviceDisplay';
import { type ClassifyResponse, type AdviceResponse } from '../types';

interface APIKey {
  key: string;
  name: string;
  is_active: boolean;
  created_at: string;
  usage_count: number;
}

interface UserProfile {
  email: string;
  role: string;
  plan: string | null;
  max_requests: number;
  usage: number;
  usage_percentage: number;
}

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [keys, setKeys] = useState<APIKey[]>([]);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(false);
  const [newKeyName, setNewKeyName] = useState('');
  const [message, setMessage] = useState('');

  // Classification state
  const [classificationResult, setClassificationResult] = useState<ClassifyResponse | null>(null);
  const [classifyLoading, setClassifyLoading] = useState(false);

  // Advice state
  const [adviceResult, setAdviceResult] = useState<AdviceResponse | null>(null);
  const [adviceLoading, setAdviceLoading] = useState(false);
  const [history, setHistory] = useState('');
  const [targetSkill, setTargetSkill] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [keysRes, profileRes] = await Promise.all([
        api.get('/api-keys'),
        api.get('/me'),
      ]);
      setKeys(keysRes.data);
      setProfile(profileRes.data);
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
    setLoading(true);
    try {
      const response = await api.post('/api-keys', { name: newKeyName });
      setKeys([response.data, ...keys]);
      setNewKeyName('');
      setMessage('✅ New API key generated');
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

  // Handle classification
  const handleClassify = async (jobTitle: string, skill: string) => {
    setClassifyLoading(true);
    try {
      const result = await api.post<ClassifyResponse>('/classify', {
        job_title: jobTitle,
        skill,
      });
      setClassificationResult(result.data);
    } catch (err: any) {
      setMessage(err.response?.data?.detail || 'Classification failed');
    } finally {
      setClassifyLoading(false);
    }
  };

  // Handle advice
  const handleAdvice = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!history.trim() || !targetSkill.trim()) {
      setMessage('Please fill in both fields');
      return;
    }
    setAdviceLoading(true);
    try {
      const result = await api.post<AdviceResponse>('/advice', {
        history,
        target_skill: targetSkill,
      });
      setAdviceResult(result.data);
    } catch (err: any) {
      setMessage(err.response?.data?.detail || 'Advice generation failed');
    } finally {
      setAdviceLoading(false);
    }
  };

  const getBadgeClass = (classification: string) => {
    switch (classification) {
      case 'Enduring': return 'badge-enduring';
      case 'Emergent': return 'badge-emergent';
      case 'Transient': return 'badge-transient';
      default: return '';
    }
  };

  return (
    <div>
      <Navbar />
      <div className="container dashboard">
        <h1>API Key Management</h1>
        <p>Manage your API keys for integrating AdaRSS into your applications.</p>

        {/* Usage Summary */}
        {profile && (
          <div className="card usage-card">
            <h2>📊 Usage Summary</h2>
            <div className="usage-stats">
              <div className="stat-item">
                <span className="stat-label">Plan</span>
                <span className="stat-value">{profile.plan || 'None'}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Used</span>
                <span className="stat-value">{profile.usage.toLocaleString()}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Remaining</span>
                <span className="stat-value">
                  {profile.max_requests > 0
                    ? (profile.max_requests - profile.usage).toLocaleString()
                    : 'Unlimited'}
                </span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Total Keys</span>
                <span className="stat-value">{keys.length}</span>
              </div>
            </div>
            {profile.max_requests > 0 && (
              <div className="progress-section">
                <div className="progress-bar">
                  <div
                    className="progress-fill"
                    style={{
                      width: `${Math.min(profile.usage_percentage, 100)}%`,
                      background: profile.usage_percentage > 80 ? '#dc2626' : '#2563eb',
                    }}
                  />
                </div>
                <span className="progress-text">
                  {profile.usage_percentage.toFixed(1)}% used
                </span>
              </div>
            )}
          </div>
        )}

        {/* Generate Key */}
        <div className="card">
          <h2>🔑 Generate New Key</h2>
          <form onSubmit={generateKey} className="generate-form">
            <input
              type="text"
              placeholder="Key name (e.g., Production, Staging)"
              value={newKeyName}
              onChange={(e) => setNewKeyName(e.target.value)}
              required
            />
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Generating...' : 'Generate Key'}
            </button>
          </form>
        </div>

        {/* API Keys Table */}
        <div className="card">
          <h2>🔐 Your API Keys</h2>
          {loading && <p>Loading...</p>}
          {keys.length === 0 && !loading && (
            <p className="empty-state">No API keys yet. Generate one above.</p>
          )}
          <div className="table-responsive">
            <table className="keys-table">
              <thead>
                <tr>
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

        {/* ==================== CLASSIFICATION SECTION ==================== */}
        <div className="card">
          <h2>🔍 Classify a Skill</h2>
          <SkillInput onClassify={handleClassify} loading={classifyLoading} />
          {classificationResult && (
            <div className="result-box">
              <h3>Result:</h3>
              <div>
                <span className={`badge ${getBadgeClass(classificationResult.classification)}`}>
                  {classificationResult.classification}
                </span>
                <span style={{ marginLeft: '0.5rem', fontSize: '0.875rem', color: '#6b7280' }}>
                  Label: {classificationResult.label}
                </span>
              </div>
            </div>
          )}
        </div>

        {/* ==================== ADVICE SECTION ==================== */}
        <div className="card">
          <h2>🧠 Get Career Advice</h2>
          <form onSubmit={handleAdvice} className="advice-form">
            <div className="form-group">
              <label>Your Work History</label>
              <textarea
                value={history}
                onChange={(e) => setHistory(e.target.value)}
                placeholder="e.g., 5 years Python, Django, REST APIs, SQL databases, AWS"
                rows={3}
                required
              />
            </div>
            <div className="form-group">
              <label>Target Skill</label>
              <input
                type="text"
                value={targetSkill}
                onChange={(e) => setTargetSkill(e.target.value)}
                placeholder="e.g., Kubernetes"
                required
              />
            </div>
            <button type="submit" className="btn-secondary" disabled={adviceLoading}>
              {adviceLoading ? 'Generating...' : 'Get Advice'}
            </button>
          </form>
          {adviceResult && (
            <div className="result-box">
              <h3>💡 Advice:</h3>
              <div>
                <span className={`badge ${getBadgeClass(adviceResult.classification)}`}>
                  {adviceResult.classification}
                </span>
                <span style={{ marginLeft: '0.5rem', fontSize: '0.875rem', color: '#6b7280' }}>
                  {adviceResult.advice_type}
                </span>
              </div>
              <p style={{ marginTop: '0.5rem', fontSize: '0.875rem', color: '#374151' }}>
                {adviceResult.description}
              </p>
              <div className="advice-detail">{adviceResult.roadmap}</div>
              <div className="similarity">Similarity Score: {(adviceResult.similarity * 100).toFixed(1)}%</div>
            </div>
          )}
        </div>

        {message && <div className={`message ${message.includes('✅') ? 'success' : 'error'}`}>{message}</div>}
      </div>
    </div>
  );
};

export default Dashboard;