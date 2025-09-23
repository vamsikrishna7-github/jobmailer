# JobMailer API Documentation

## Overview
JobMailer is a Django REST API that helps generate and send professional job application emails using Google Gemini AI and Django SMTP.

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, the API uses `AllowAny` permissions. No authentication is required for testing purposes.

## Endpoints

### 1. Health Check
Check if the API is running.

**Endpoint:** `GET /api/health/`

**Response:**
```json
{
    "status": "healthy",
    "message": "JobMailer API is running"
}
```

**Status Code:** `200 OK`

---

### 2. Generate Email
Generate a professional job application email using Google Gemini AI.

**Endpoint:** `POST /api/generate-email/`

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

**Required Fields:**
- `hr_email` (string): HR/recruiter email address
- `company` (string): Company name
- `role` (string): Job position title
- `name` (string): Applicant's name
- `skills` (string): Comma-separated list of skills

**Success Response:**
```json
{
    "status": "success",
    "email_text": "Subject: Application for Software Engineer Position at Tech Corp\n\nDear Hiring Manager,\n\nI am writing to express my strong interest in the Software Engineer position at Tech Corp...",
    "request_id": 1
}
```

**Error Response:**
```json
{
    "error": "Missing required field: hr_email"
}
```

**Status Codes:**
- `200 OK`: Email generated successfully
- `400 Bad Request`: Missing required fields
- `500 Internal Server Error`: AI generation failed or server error

---

### 3. Send Email
Send an email via Django SMTP.

**Endpoint:** `POST /api/send-email/`

**Request Body:**
```json
{
    "hr_email": "hr@company.com",
    "subject": "Application for Software Engineer Position at Tech Corp",
    "body": "Dear Hiring Manager,\n\nI am writing to express my strong interest..."
}
```

**Required Fields:**
- `hr_email` (string): Recipient email address
- `subject` (string): Email subject line
- `body` (string): Email body content

**Success Response:**
```json
{
    "status": "sent",
    "message": "Email sent successfully"
}
```

**Error Response:**
```json
{
    "error": "Email configuration not set. Please configure EMAIL_HOST_USER and EMAIL_HOST_PASSWORD."
}
```

**Status Codes:**
- `200 OK`: Email sent successfully
- `400 Bad Request`: Missing required fields
- `500 Internal Server Error`: Email configuration error or sending failed

---

## Error Handling

### Common Error Responses

**Missing Required Field:**
```json
{
    "error": "Missing required field: field_name"
}
```

**Email Configuration Error:**
```json
{
    "error": "Email configuration not set. Please configure EMAIL_HOST_USER and EMAIL_HOST_PASSWORD."
}
```

**AI Generation Error:**
```json
{
    "error": "Failed to generate email with AI. Please try again."
}
```

**Generic Server Error:**
```json
{
    "error": "An unexpected error occurred"
}
```

---

## Data Models

### EmailRequest
Stores email generation requests and generated content.

**Fields:**
- `id`: Primary key
- `hr_email`: HR/recruiter email address
- `company`: Company name
- `role`: Job position title
- `name`: Applicant's name
- `skills`: Applicant's skills
- `generated_email`: AI-generated email content
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### EmailSent
Tracks sent emails and their status.

**Fields:**
- `id`: Primary key
- `to_email`: Recipient email address
- `subject`: Email subject
- `body`: Email body content
- `sent_at`: Sending timestamp
- `status`: Email status ('sent' or 'failed')

---

## Rate Limits
Currently, no rate limiting is implemented. Consider implementing rate limiting for production use.

## CORS
CORS is not configured by default. Add CORS headers if accessing the API from a frontend application.

## Example Usage

### Complete Workflow
1. Generate an email using the `/api/generate-email/` endpoint
2. Extract the email content from the response
3. Send the email using the `/api/send-email/` endpoint

### cURL Examples

**Generate Email:**
```bash
curl -X POST http://localhost:8000/api/generate-email/ \
  -H "Content-Type: application/json" \
  -d '{
    "hr_email": "hr@company.com",
    "company": "Tech Corp",
    "role": "Software Engineer",
    "name": "John Doe",
    "skills": "Python, Django, React, PostgreSQL, Docker"
  }'
```

**Send Email:**
```bash
curl -X POST http://localhost:8000/api/send-email/ \
  -H "Content-Type: application/json" \
  -d '{
    "hr_email": "hr@company.com",
    "subject": "Application for Software Engineer Position at Tech Corp",
    "body": "Dear Hiring Manager,\n\nI am writing to express my strong interest..."
  }'
```

**Health Check:**
```bash
curl -X GET http://localhost:8000/api/health/
```

---

## Environment Variables

Make sure to configure the following environment variables:

- `GEMINI_API_KEY`: Google Gemini API key
- `EMAIL_HOST_USER`: Gmail address for sending emails
- `EMAIL_HOST_PASSWORD`: Gmail app password for authentication

See the README.md for detailed setup instructions.
