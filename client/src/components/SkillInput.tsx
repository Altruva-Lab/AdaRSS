import React, { useState } from 'react';

interface SkillInputProps {
  onClassify: (jobTitle: string, skill: string) => void;
  loading: boolean;
}

const SkillInput: React.FC<SkillInputProps> = ({ onClassify, loading }) => {
  const [jobTitle, setJobTitle] = useState('');
  const [skill, setSkill] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onClassify(jobTitle, skill);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Job Title</label>
        <input
          type="text"
          value={jobTitle}
          onChange={(e) => setJobTitle(e.target.value)}
          placeholder="e.g., Data Scientist"
          required
        />
      </div>
      <div>
        <label>Skill</label>
        <input
          type="text"
          value={skill}
          onChange={(e) => setSkill(e.target.value)}
          placeholder="e.g., SQL"
          required
        />
      </div>
      <button type="submit" className="btn-primary" disabled={loading}>
        {loading ? 'Classifying...' : 'Classify Skill'}
      </button>
    </form>
  );
};

export default SkillInput;