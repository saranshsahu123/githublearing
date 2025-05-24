import os
import re
import spacy
import pdfplumber
import docx
from django.shortcuts import render
from .forms import ResumeUploadForm

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

def ai_chatbot_response(skills_list):
    company_db = {
        "Google": ["python", "machine learning", "tensorflow", "sql"],
    "Microsoft": ["azure", "c#", "sql", "python"],
    "Amazon": ["aws", "python", "java", "data analysis"],
    "TCS": ["java", "sql", "spring", "oracle"],
    "Infosys": ["python", "sql", "django", "react"],
    "Wipro": ["html", "css", "javascript", "node"],
    "Capgemini": ["java", "spring", "sql"],
    "Accenture": ["python", "react", "cloud", "sql"],
    "IBM": ["java", "cloud computing", "data analysis", "python"],
    "HCL Technologies": ["java", "c++", "sql", "cloud computing"],
    "Tech Mahindra": ["java", "sql", "cloud computing", "python"],
    "Cognizant": ["java", "sql", "cloud computing", "python"],
    "Oracle": ["oracle", "sql", "java", "cloud computing"],
    "SAP": ["sap", "java", "sql", "cloud computing"],
    "Adobe": ["photoshop", "illustrator", "javascript", "html"],
    "Intel": ["c++", "python", "machine learning", "data analysis"],
    "Cisco": ["networking", "python", "cloud computing", "security"],
    "Dell Technologies": ["java", "cloud computing", "sql", "python"],
    "HP": ["java", "cloud computing", "sql", "python"],
    "NVIDIA": ["c++", "python", "machine learning", "deep learning"],
    "Salesforce": ["salesforce", "java", "sql", "cloud computing"],
    "VMware": ["virtualization", "cloud computing", "python", "java"],
    "Red Hat": ["linux", "python", "cloud computing", "java"],
    "Zoho": ["java", "sql", "cloud computing", "python"],
    "Flipkart": ["java", "sql", "cloud computing", "python"],
    "Ola": ["java", "sql", "cloud computing", "python"],
    "Paytm": ["java", "sql", "cloud computing", "python"],
    "Zomato": ["java", "sql", "cloud computing", "python"],
    "Swiggy": ["java", "sql", "cloud computing", "python"],
    "BYJU'S": ["java", "sql", "cloud computing", "python"],
    "Unacademy": ["java", "sql", "cloud computing", "python"],
    "Vedantu": ["java", "sql", "cloud computing", "python"],
    "WhiteHat Jr": ["java", "sql", "cloud computing", "python"],
    "Freshworks": ["java", "sql", "cloud computing", "python"],
    "Zoho": ["java", "sql", "cloud computing", "python"],
    "InMobi": ["java", "sql", "cloud computing", "python"],
    "CureFit": ["java", "sql", "cloud computing", "python"],
    "Razorpay": ["java", "sql", "cloud computing", "python"],
    "PhonePe": ["java", "sql", "cloud computing", "python"],
    "PolicyBazaar": ["java", "sql", "cloud computing", "python"],
    "Lenskart": ["java", "sql", "cloud computing", "python"],
    "UrbanClap": ["java", "sql", "cloud computing", "python"],
    "BigBasket": ["java", "sql", "cloud computing", "python"],
    "Grofers": ["java", "sql", "cloud computing", "python"],
    "Delhivery": ["java", "sql", "cloud computing", "python"],
    "Snapdeal": ["java", "sql", "cloud computing", "python"],
    "ShopClues": ["java", "sql", "cloud computing", "python"],
    "Myntra": ["java", "sql", "cloud computing", "python"],
    "Jabong": ["java", "sql", "cloud computing", "python"],
    "Pepperfry": ["java", "sql", "cloud computing", "python"],
    "Housing.com": ["java", "sql", "cloud computing", "python"],
    "Quikr": ["java", "sql", "cloud computing", "python"],
    "MagicBricks": ["java", "sql", "cloud computing", "python"],
    "99acres": ["java", "sql", "cloud computing", "python"],
    "Naukri.com": ["java", "sql", "cloud computing", "python"],
    "Monster India": ["java", "sql", "cloud computing", "python"],
    "Shine.com": ["java", "sql", "cloud computing", "python"],
    "TimesJobs": ["java", "sql", "cloud computing", "python"],
    "Indeed India": ["java", "sql", "cloud computing", "python"],
    "LinkedIn India": ["java", "sql", "cloud computing", "python"],
    "Glassdoor India": ["java", "sql", "cloud computing", "python"],
    "Upwork": ["java", "sql", "cloud computing", "python"],
    "Freelancer": ["java", "sql", "cloud computing", "python"],
    "Toptal": ["java", "sql", "cloud computing", "python"],
    "Guru": ["java", "sql", "cloud computing", "python"],
    "PeoplePerHour": ["java", "sql", "cloud computing", "python"],
    "Fiverr": ["java", "sql", "cloud computing", "python"],
    "Envato": ["java", "sql", "cloud computing", "python"],
    "ThemeForest": ["java", "sql", "cloud computing", "python"],
    }

    suggestions = []
    for company, required in company_db.items():
        matches = set(skills_list) & set(required)
        if matches:
            suggestions.append({
                "company": company,
                "matched_skills": list(matches),
                "match_score": len(matches)
            })

    suggestions = sorted(suggestions, key=lambda x: x["match_score"], reverse=True)
    return suggestions


def extract_resume_data(file_path):
    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    else:
        text = extract_text_from_docx(file_path)

    lines = [line.strip() for line in text.split('\n') if line.strip()]
    # Clean and validate name (remove digits and special characters)
    raw_name = lines[0] if len(lines) > 0 else ""
    name = re.sub(r'[^a-zA-Z\s]', '', raw_name).strip()

# Optional: Make sure name is not empty after cleanup
    if not name:
       name = "Name Not Found"

    job_role_line = lines[1].lower() if len(lines) > 1 else ""
    
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3,5}\)?[-.\s]?\d{3,5}[-.\s]?\d{3,5}', text)

    skill_keywords = ['python', 'java', 'c++', 'sql', 'html', 'css', 'django', 'react', 'node', 
                      'aws', 'linux', 'git', 'shell scripting']
    skills = [word for word in skill_keywords if re.search(rf"\b{word}\b", text, re.IGNORECASE)]

    education_text = text[text.lower().find("education"):][:500] if "education" in text.lower() else ""
    degree_ranks = {
        'b.tech': 3, 'm.tech': 4, 'phd': 5, 'm.sc': 4, 'b.e': 3, 'b.sc': 3,
        'diploma': 2, '12th': 1, '10th': 1, "bachelor's": 2,
    }

    degree = None
    degree_score = 0
    for deg, score in degree_ranks.items():
        if re.search(rf"\b{deg}\b", education_text, re.IGNORECASE):
            degree = deg.upper()
            degree_score = score
            break

    project_keywords = ['project', 'final year', 'internship']
    has_project = any(word in text.lower() for word in project_keywords)

    # Job matching logic
    known_roles = {
        "full stack": "Full Stack Developer",
        "software": "Software Engineer",
        "devops": "DevOps Engineer",
        "data scientist": "Data Scientist",
        "cloud": "Cloud Engineer"
    }

    job_roles = {
        "Full Stack Developer": ["python", "django", "html", "css", "javascript", "react", "node"],
        "Software Engineer": ["java", "python", "c++", "problem solving", "algorithms"],
        "DevOps Engineer": ["docker", "kubernetes", "aws", "jenkins", "terraform", "ansible", "linux"],
        "Data Scientist": ["python", "machine learning", "data analysis", "pandas", "numpy", "tensorflow"],
        "Cloud Engineer": ["aws", "azure", "gcp", "cloud computing", "vpc", "load balancer"]
    }

    matched_role = None
    job_match_score = 0
    for keyword, role in known_roles.items():
        if keyword in job_role_line:
            matched_role = role
            expected_skills = job_roles[role]
            job_match_score = sum(1 for s in skills if s in expected_skills)
            break

    

    # Score out of 10
    raw_score = degree_score + len(skills) + job_match_score + (2 if has_project else 0)
    rank_score = round((raw_score / 20) * 10, 2)

    companies = ai_chatbot_response(skills)

    return {
        "name": name,
        "job_role": matched_role or job_role_line,
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0) if phone_match else None,
        "skills": skills,
        "degree": degree,
        "has_project": has_project,
        "rank_score": rank_score,
        "matched_role_skills": job_roles.get(matched_role, []) if matched_role else [],
        "matched_skills": [s for s in skills if matched_role and s in job_roles[matched_role]],
        "companies": companies,
        
    }


def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['resume']
            file_path = os.path.join('media', uploaded_file.name)

            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            data = extract_resume_data(file_path)
            return render(request, 'result.html', {'data': data})
    else:
        form = ResumeUploadForm()

    return render(request, 'upload.html', {'form': form})
