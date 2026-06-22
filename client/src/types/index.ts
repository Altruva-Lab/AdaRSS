export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface ClassifyRequest {
  job_title: string;
  skill: string;
}

export interface ClassifyResponse {
  classification: string; // Enduring | Emergent | Transient
  label: number; // 0,1,2
}

export interface AdviceRequest {
  history: string;
  target_skill: string;
}

export interface AdviceResponse {
  classification: string;
  advice_type: string; // Continuous Upscaling | Career Broadening | Change of Profession
  description: string;
  roadmap: string;
  similarity: number;
}