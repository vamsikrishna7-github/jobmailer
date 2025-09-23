# JobMailer API

A Django REST API that generates and sends professional job application emails using Google Gemini AI and Django SMTP.

## 🚀 Features

- **AI-Powered Email Generation**: Uses Google Gemini AI to create personalized job application emails
- **SMTP Email Sending**: Sends emails via Django's built-in SMTP functionality
- **REST API**: Clean, well-documented REST endpoints
- **Database Tracking**: Stores email requests and sent emails for record-keeping
- **Admin Interface**: Django admin panel for managing data

## 🛠 Tech Stack

- **Backend**: Django 5.0.7
- **API Framework**: Django REST Framework 3.15.2
- **AI Integration**: Google Generative AI (Gemini)
- **Email**: Django SMTP with Gmail
- **Database**: SQLite (default)
- **Environment Management**: python-dotenv

## 📋 Prerequisites

- Python 3.8+
- Gmail account with App Password
- Google Gemini API key

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd jobmailer
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```bash
cp env_template.txt .env
```

Edit the `.env` file with your credentials:

```env
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True

# Google Gemini AI Configuration
GEMINI_API_KEY=AIzaSyAdfmjeiY9KQ3fbkHsgd1-t41dRRW9ANTk

# Email Configuration (Gmail)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password-here
```

### 5. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Optional: for admin access
```

### 6. Run the Server

**Option 1: Using the startup script (Recommended)**
```bash
./run_server.sh
```

**Option 2: Manual setup**
```bash
export PYTHONPATH="/media/mrx/projects/jobmailer/venv/lib/python3.10/site-packages:$PYTHONPATH"
python3 manage.py runserver
```

The API will be available at `http://localhost:8000`

### 7. Test AI Integration (Optional)

Test the Gemini AI integration:
```bash
python3 test_gemini.py
```

## 📚 API Endpoints

### Health Check
```
GET /api/health/
```

### Generate Email
```
POST /api/generate-email/
```

**Request Body:**
```json
{
    "hr_email": "hr@company.com",
    "company": "Tech Corp",
    "role": "Software Engineer",
    "name": "John Doe",
    "skills": "Python, Django, React, PostgreSQL, Docker"
}
```

### Send Email
```
POST /api/send-email/
```

**Request Body:**
```json
{
    "hr_email": "hr@company.com",
    "subject": "Application for Software Engineer Position",
    "body": "Dear Hiring Manager,\n\nI am writing to express my interest..."
}
```

## 🧪 Testing with Postman

1. Import the `postman_collection.json` file into Postman
2. Set the `baseUrl` variable to `http://localhost:8000`
3. Run the requests to test the API endpoints

### Test Workflow:
1. **Health Check**: Verify the API is running
2. **Generate Email**: Create a job application email using AI
3. **Send Email**: Send the generated email via SMTP

## 🔧 Configuration

### Gmail App Password Setup

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
   - Use this password in `EMAIL_HOST_PASSWORD`

### Google Gemini API Setup

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add the key to your `.env` file

## 📁 Project Structure

```
jobmailer/
├── jobmailer/          # Django project settings
│   ├── settings.py     # Main configuration
│   ├── urls.py         # URL routing
│   └── ...
├── mailer/             # Main application
│   ├── models.py       # Database models
│   ├── views.py        # API views
│   ├── urls.py         # App URLs
│   └── admin.py        # Admin configuration
├── docs/               # Documentation
│   └── api_documentation.md
├── postman_collection.json
├── requirements.txt
├── env_template.txt
└── README.md
```

## 🗄️ Database Models

### EmailRequest
Stores email generation requests and AI-generated content.

### EmailSent
Tracks sent emails and their delivery status.

## 🚀 Production Deployment

### Environment Variables for Production

```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

### Security Considerations

- Use environment variables for sensitive data
- Enable HTTPS in production
- Set up proper CORS if needed
- Implement rate limiting
- Use a production database (PostgreSQL recommended)

## 🐛 Troubleshooting

### Common Issues

1. **Email not sending**: Check Gmail app password and 2FA settings
2. **Gemini API errors**: Verify API key and quota limits
3. **Database errors**: Run migrations: `python manage.py migrate`

### Debug Mode

Set `DEBUG=True` in your `.env` file to see detailed error messages.

## 📖 API Documentation

Detailed API documentation is available in `docs/api_documentation.md`.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Open an issue in the repository

---

## 🔄 Enhanced API Features

### Comprehensive User Profiles

The enhanced API now supports comprehensive user profiles with all the information you requested:

#### User Profile Fields:
- **Basic Information**: Name, Location, Phone Number, Primary Email
- **Contact Information**: Alternative Email, Portfolio URL, LinkedIn, GitHub, LeetCode
- **Education**: Degree, Field, University, Graduation Year, GPA
- **Skills Categories**:
  - Programming Languages
  - Python Frameworks
  - Frontend Technologies
  - Mobile Development
  - Databases
  - Cloud & DevOps
  - Deployment Platforms
  - Integrations
  - Development Practices
- **Professional Experience**: Detailed work history
- **Projects**: Portfolio of personal/professional projects
- **Resume**: PDF file attachment support

### Enhanced Email Generation

The AI now generates emails using comprehensive user data:
- ✅ Personalized introductions with full contact information
- ✅ Relevant skills highlighting based on job requirements
- ✅ Specific achievements from experience and projects
- ✅ Portfolio, GitHub, and LinkedIn references
- ✅ Professional signature with all contact details
- ✅ Resume attachment support

### New API Workflow

1. **Create User Profile**: `POST /api/create-profile/`
2. **Generate Enhanced Email**: `POST /api/generate-email-enhanced/`
3. **Generate Cover Letter**: `POST /api/generate-cover-letter-pdf/`
4. **Send Email with Resume & Cover Letter**: `POST /api/send-email-with-resume-and-cover-letter/`
5. **Manage Profile**: `GET /api/get-profile/{id}/`

### Resume Attachment

- Automatically attaches user's resume PDF to emails
- Tracks resume attachment status in sent emails
- Supports PDF file uploads up to 10MB
- Stored securely in Django media directory

### Enhanced Cover Letter Generation

The API now supports comprehensive cover letter generation with detailed company and recipient information:

#### Cover Letter Features:
- **Professional PDF format** with proper business letter layout
- **Full address format** including company address and recipient details
- **Personalized content** using detailed user-provided information
- **Structured paragraphs** following professional cover letter standards
- **Fallback support** - uses profile data when specific details aren't provided

#### New Optional Fields:
- `recipient_name`: Specific hiring manager or contact person
- `company_address`: Company street address
- `company_city_state_zip`: Company location details
- `previous_company`: Previous employer for experience reference
- `key_skills`: Specific skills to highlight
- `specific_achievements`: Detailed accomplishments and achievements
- `company_interest`: What excites you about this opportunity
- `personal_qualities`: Personal attributes and qualities to highlight

### Django Admin Enhancements

- **User Profile Management**: Comprehensive profile editing
- **Enhanced Email Requests**: Linked to user profiles
- **Resume Tracking**: Shows which emails included resume attachments
- **Bulk Operations**: Send multiple emails with resume attachments

## 📊 Example Complete Workflow

### 1. Create Profile
```bash
curl -X POST http://localhost:8000/api/create-profile/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Vamsikrishna Nagidi",
    "location": "Hyderabad, India",
    "phone_number": "+91-9876543210",
    "primary_email": "vamsikrishna.nagidi@gmail.com",
    "portfolio_url": "https://vamsikrishna.dev",
    "linkedin_url": "https://linkedin.com/in/vamsikrishna",
    "github_url": "https://github.com/vamsikrishna",
    "education_degree": "BTech",
    "education_field": "Computer Science",
    "university_name": "JNTU Hyderabad",
    "graduation_year": 2022,
    "programming_languages": "Python, JavaScript, Java, C++",
    "python_frameworks": "Django, Flask, FastAPI",
    "frontend_technologies": "React, HTML5, CSS3, TypeScript",
    "databases": "PostgreSQL, MongoDB, Redis",
    "cloud_devops": "AWS, Docker, Kubernetes",
    "professional_experience": "Software Engineer with 2+ years experience...",
    "projects": "Built multiple web applications using Django and React..."
  }'
```

### 2. Generate Enhanced Email
```bash
curl -X POST http://localhost:8000/api/generate-email-enhanced/ \
  -H "Content-Type: application/json" \
  -d '{
    "profile_id": 1,
    "hr_email": "hr@techcorp.com",
    "company": "Tech Corp",
    "role": "Senior Software Engineer",
    "job_description": "Looking for experienced full-stack developer..."
  }'
```

### 3. Generate Cover Letter PDF
```bash
curl -X POST http://localhost:8000/api/generate-cover-letter-pdf/ \
  -H "Content-Type: application/json" \
  -d '{
    "profile_id": 1,
    "company": "Tech Corp",
    "role": "Senior Software Engineer",
    "job_description": "Looking for experienced full-stack developer",
    "recipient_name": "John Smith",
    "company_address": "123 Tech Street",
    "company_city_state_zip": "San Francisco, CA 94105",
    "previous_company": "TechStart Inc.",
    "key_skills": "Python, Django, React, PostgreSQL, AWS, Docker",
    "specific_achievements": "Led a team of 5 developers to build a scalable e-commerce platform serving 50,000+ users. Implemented CI/CD pipelines that reduced deployment time by 60%.",
    "company_interest": "Tech Corp'\''s innovative approach to cloud-native applications and commitment to developer experience",
    "personal_qualities": "strong problem-solving abilities, collaborative mindset, and passion for clean code"
  }' \
  --output cover_letter.pdf
```

### 4. Send Email with Resume and Cover Letter
```bash
curl -X POST http://localhost:8000/api/send-email-with-resume-and-cover-letter/ \
  -H "Content-Type: application/json" \
  -d '{
    "profile_id": 1,
    "hr_email": "hr@techcorp.com",
    "subject": "Application for Senior Software Engineer Position",
    "body": "Generated email content here...",
    "company": "Tech Corp",
    "role": "Senior Software Engineer",
    "job_description": "Looking for experienced full-stack developer",
    "recipient_name": "John Smith",
    "company_address": "123 Tech Street",
    "company_city_state_zip": "San Francisco, CA 94105",
    "previous_company": "TechStart Inc.",
    "key_skills": "Python, Django, React, PostgreSQL, AWS, Docker",
    "specific_achievements": "Led a team of 5 developers to build a scalable e-commerce platform serving 50,000+ users.",
    "company_interest": "Tech Corp'\''s innovative approach to cloud-native applications",
    "personal_qualities": "strong problem-solving abilities, collaborative mindset, and passion for clean code"
  }'
```

### 5. Simple Workflow (Using Profile Data)
```bash
# Generate cover letter using only profile data
curl -X POST http://localhost:8000/api/generate-cover-letter-pdf/ \
  -H "Content-Type: application/json" \
  -d '{
    "profile_id": 1,
    "company": "Tech Corp",
    "role": "Senior Software Engineer",
    "job_description": "Looking for experienced full-stack developer"
  }' \
  --output cover_letter.pdf

# Send email with basic cover letter
curl -X POST http://localhost:8000/api/send-email-with-resume-and-cover-letter/ \
  -H "Content-Type: application/json" \
  -d '{
    "profile_id": 1,
    "hr_email": "hr@techcorp.com",
    "subject": "Application for Senior Software Engineer Position",
    "body": "Generated email content here...",
    "company": "Tech Corp",
    "role": "Senior Software Engineer",
    "job_description": "Looking for experienced full-stack developer"
  }'
```

**Happy job hunting! 🎯**
