# JobMailer Frontend

A modern Next.js frontend application for the JobMailer API - an AI-powered job application platform.

## Features

- **Complete Job Application Workflow**: From profile creation to email sending
- **AI-Powered Email Generation**: Uses Google Gemini AI for personalized emails
- **Cover Letter PDF Generation**: Professional cover letters with resume attachments
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time API Integration**: Connects to production JobMailer API

## Tech Stack

- **Next.js 15.5.3**: React framework with App Router
- **React 19.1.0**: Latest React version
- **Tailwind CSS 4**: Utility-first CSS framework
- **JavaScript ES6+**: Modern JavaScript features

## Getting Started

### Prerequisites

- Node.js 18.0 or later
- npm or yarn package manager

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

### Production Build

```bash
npm run build
npm start
```

## API Integration

The frontend integrates with the JobMailer API hosted at:
`https://jobmailer-dezw.onrender.com`

### Available Endpoints

- `POST /api/create-profile/` - Create user profile
- `GET /api/get-profile/{id}/` - Get user profile
- `POST /api/generate-email-enhanced/` - Generate AI email
- `POST /api/generate-cover-letter-pdf/` - Generate cover letter PDF
- `POST /api/send-email-with-resume-and-cover-letter/` - Send email with attachments

## Application Flow

### Step 1: Profile Creation
- Personal information (name, location, contact details)
- Education background
- Technical skills and experience
- Professional experience and projects
- Resume file upload (optional)

### Step 2: Job Application Details
- Company and role information
- Job description
- Enhanced details (previous company, achievements, etc.)
- Company address and recipient information

### Step 3: Review and Send
- AI-generated email preview
- Cover letter PDF download
- Email customization and sending

## Components

- `Header.js` - Navigation header
- `Footer.js` - Application footer
- `JobMailerForm.js` - Main form container with workflow management
- `ProfileForm.js` - User profile creation form
- `JobApplicationForm.js` - Job application details form
- `ResultsDisplay.js` - Email preview and sending interface

## Configuration

API configuration is managed in `src/config/api.js`:
- Base URL configuration
- Endpoint definitions
- API helper functions
- Error handling

## Features

### Responsive Design
- Mobile-first approach
- Tailwind CSS responsive utilities
- Optimized for all screen sizes

### Error Handling
- Comprehensive error messages
- Network error handling
- User-friendly error display

### Loading States
- Loading indicators during API calls
- Disabled states for better UX
- Progress indicators

### File Handling
- Resume file upload support
- PDF cover letter generation
- File download functionality

## Deployment

The application is ready for deployment on platforms like:
- Vercel (recommended for Next.js)
- Netlify
- AWS Amplify
- Any Node.js hosting platform

## Environment Variables

No environment variables are required for basic functionality. The API base URL is configured directly in the code for production use.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the JobMailer application suite.