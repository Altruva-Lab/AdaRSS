import pandas as pd
import random
import numpy as np

# ------------------- LISTS OF JOB TITLES -------------------
job_titles = [
    # Tech
    "Frontend Developer", "Backend Developer", "Full Stack Developer",
    "DevOps Engineer", "Machine Learning Engineer", "Data Scientist",
    "Data Engineer", "AI Researcher", "Software Engineer", "QA Engineer",
    "Systems Administrator", "Security Analyst", "Cloud Architect",
    # Business & Finance
    "Accountant", "Financial Analyst", "Investment Banker",
    "Marketing Manager", "Digital Marketing Specialist", "SEO Specialist",
    "Sales Manager", "Business Analyst", "HR Manager", "Recruiter",
    # Healthcare
    "Registered Nurse", "Physician", "Healthcare Administrator",
    "Medical Coder", "Radiology Technician", "Physical Therapist",
    # Creative & Design
    "Graphic Designer", "UI/UX Designer", "Art Director", "Animator",
    # Trades & Operations
    "Plumber", "Electrician", "Construction Manager", "HVAC Technician",
    "Warehouse Operator", "Logistics Coordinator", "Supply Chain Manager",
    # Education & Law
    "Teacher", "Professor", "Lawyer", "Paralegal", "Compliance Officer",
]

# ------------------- LISTS OF SKILLS (by category) -------------------
enduring_skills = [
    "SQL", "Data Structures", "REST API design", "Linux administration",
    "Network security fundamentals", "Object-Oriented Programming",
    "Statistical reasoning", "Gradient descent", "Data normalization",
    "System design patterns", "CI/CD pipelines", "Encryption basics",
    "HTTP/HTTPS protocols", "Data ethics", "Agile methodologies",
    "Model evaluation metrics", "Brand Positioning", "Keyword research",
    "GAAP principles", "Excel financial modeling", "Patient triage protocols",
    "ICD-10 coding", "Pipe fitting and soldering", "National Electrical Code",
    "Employee relations law", "Contract law fundamentals", "GDPR regulations",
    "Lean Six Sigma", "Interstate trucking regulations", "ABC analysis",
    "Incoterms", "Color theory and composition", "Test automation principles",
]

emergent_skills = [
    "Kubernetes", "Docker", "MLOps practices", "LoRA fine-tuning",
    "Apache Airflow", "Terraform", "TypeScript", "PyTorch",
    "Microservices architecture", "Zero Trust architecture", "Serverless computing",
    "Swift", "Performance testing (JMeter)", "Apache Spark",
    "GraphQL", "Vector databases", "Service Mesh (Istio)", "Flutter",
    "Cypress", "Reinforcement Learning", "Data lake architecture",
    "Google Analytics 4", "QuickBooks Online", "Epic Systems (EMR)",
    "BIM (Building Information Modeling)", "Smart thermostat installation",
    "LinkedIn Recruiter platform", "People analytics (Python/Tableau)",
    "DEI frameworks", "Salesforce CRM", "Adobe Photoshop", "Figma",
    "Westlaw legal database", "E-discovery software (Relativity)",
    "Route optimization software", "Automated picking robots (control)",
]

transient_skills = [
    "React hooks", "Next.js App Router", "Vue.js 3 Composition API",
    "Expo (React Native)", "Chef", "Selenium IDE", "Django REST Framework",
    "Apache Pig", "Caffe", "SvelteKit", "Puppet (legacy)", "KNIME specific nodes",
    "Cordova/PhoneGap", "JUnit 4 annotations", "TikTok trends management",
    "Cryptocurrency portfolio strategies", "Telemedicine platforms (Doxy.me)",
    "RF scanner inventory management", "Amazon FBA specific rules",
    "Adobe Photoshop specific filters", "WordPress page builders (Elementor)",
    "USCIS specific forms (I-129)", "After Effects expressions", "Old JUnit",
]

# We'll assign labels based on these probabilities (realistic distribution)
# 55% Enduring, 30% Emergent, 15% Transient
def assign_label():
    r = random.random()
    if r < 0.55:
        return 0  # Enduring
    elif r < 0.85:
        return 1  # Emergent
    else:
        return 2  # Transient

# Function to get a skill based on label
def get_skill_for_label(label):
    if label == 0:
        return random.choice(enduring_skills)
    elif label == 1:
        return random.choice(emergent_skills)
    else:
        return random.choice(transient_skills)

# Generate dataset
num_samples = 1000  # Adjust as needed; 200 is a good starting point
data = []
used_pairs = set()

for _ in range(num_samples):
    # Pick a job title
    job = random.choice(job_titles)
    # Assign label
    label = assign_label()
    # Get a skill for that label
    skill = get_skill_for_label(label)
    # Avoid exact duplicates (but allow same skill with different jobs)
    pair = (job, skill)
    if pair in used_pairs:
        continue  # skip duplicate
    used_pairs.add(pair)
    # Justification – we'll generate a generic one based on label
    if label == 0:
        justification = f"Foundational skill that has persisted for decades across industries."
    elif label == 1:
        justification = f"Rapidly gaining adoption; a key emerging skill in the market."
    else:
        justification = f"Framework or tool‑specific; volatile and likely to be replaced within a few years."
    data.append({
        "job_title": job,
        "skill": skill,
        "label": label,
        "justification": justification
    })

# Create DataFrame and save
df = pd.DataFrame(data)
df.to_csv("data/sample_annotated.csv", index=False)
print(f"✅ Generated {len(df)} samples with distribution:")
print(df['label'].value_counts().sort_index())