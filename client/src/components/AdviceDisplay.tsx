import React from 'react';
import { type AdviceResponse } from '../types';

interface AdviceDisplayProps {
  advice: AdviceResponse | null;
}

const AdviceDisplay: React.FC<AdviceDisplayProps> = ({ advice }) => {
  if (!advice) return null;

  const getBadgeClass = (classification: string) => {
    switch (classification) {
      case 'Enduring': return 'badge-enduring';
      case 'Emergent': return 'badge-emergent';
      case 'Transient': return 'badge-transient';
      default: return '';
    }
  };

  return (
    <div className="result-box">
      <h3>💡 Advice:</h3>
      <div>
        <span className={`badge ${getBadgeClass(advice.classification)}`}>
          {advice.classification}
        </span>
        <span style={{ marginLeft: '0.5rem', fontSize: '0.875rem', color: '#6b7280' }}>
          {advice.advice_type}
        </span>
      </div>
      <p style={{ marginTop: '0.5rem', fontSize: '0.875rem', color: '#374151' }}>
        {advice.description}
      </p>
      <div className="advice-detail">{advice.roadmap}</div>
      <div className="similarity">Similarity Score: {(advice.similarity * 100).toFixed(1)}%</div>
    </div>
  );
};

export default AdviceDisplay;