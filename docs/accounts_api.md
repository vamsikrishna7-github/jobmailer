## JobMailer Accounts API

Base URL: `http://localhost:8000`

Auth: Simple JWT (email as username field)

### Authentication
- POST `/api/accounts/register/register/`
  - Body (json): `{ email, username, name, phone, password }`
  - Returns: `{ user, access, refresh }`

- POST `/api/accounts/token/`
  - Body (json): `{ email, password }`
  - Returns: `{ access, refresh }`

- POST `/api/accounts/token/refresh/`
  - Body (json): `{ refresh }`
  - Returns: `{ access }`

- POST `/api/accounts/auth/logout/`
  - Headers: `Authorization: Bearer <access>`
  - Body (json): `{ refresh }`
  - Effect: Blacklists refresh token

### Profile
- GET `/api/accounts/profile/me/` (JWT)
  - Returns the authenticated user's profile with nested relations

- PATCH `/api/accounts/profile/{id}/` (JWT)
  - Body example:
    ```json
    {
      "bio": "Updated bio",
      "skills": [{"name": "Python"}, {"name": "Django"}],
      "educations": [
        {"degree": "B.Tech", "institution": "Example U", "start_date": "2018-08-01", "end_date": "2022-05-15", "grade": "8.7 CGPA"}
      ],
      "experiences": [
        {"company_name": "Acme", "role": "SWE", "start_date": "2023-01-01", "end_date": null, "description": "Backend"}
      ],
      "projects": [
        {"title": "Portfolio", "description": "Next.js", "tech_stack": "Next.js, Tailwind", "link": "https://example.com", "github_link": "https://github.com/user/repo"}
      ],
      "social_links": {"github": "https://github.com/user", "linkedin": "https://linkedin.com/in/user"}
    }
    ```

- POST `/api/accounts/profile/upload-resume/` (JWT)
  - multipart/form-data, field: `resume` (PDF only)

### Education (owner-only CRUD)
- GET `/api/accounts/education/`
- POST `/api/accounts/education/` body: `{ degree, institution, start_date, end_date, grade }`
- GET `/api/accounts/education/{id}/`
- PATCH `/api/accounts/education/{id}/`
- DELETE `/api/accounts/education/{id}/`

### Experience (owner-only CRUD)
- GET `/api/accounts/experience/`
- POST `/api/accounts/experience/` body: `{ company_name, role, start_date, end_date, description }`
- GET `/api/accounts/experience/{id}/`
- PATCH `/api/accounts/experience/{id}/`
- DELETE `/api/accounts/experience/{id}/`

### Projects (owner-only CRUD with search)
- GET `/api/accounts/projects/?search=<query>`
- POST `/api/accounts/projects/` body: `{ title, description, tech_stack, link, github_link }`
- GET `/api/accounts/projects/{id}/`
- PATCH `/api/accounts/projects/{id}/`
- DELETE `/api/accounts/projects/{id}/`

### Skills
- GET `/api/accounts/skills/?search=<q>`
- POST `/api/accounts/skills/` body: `{ name }`
- GET `/api/accounts/skills/{id}/`
- PATCH `/api/accounts/skills/{id}/`
- DELETE `/api/accounts/skills/{id}/`

### Social Links (owner-only)
- GET `/api/accounts/links/`
- POST `/api/accounts/links/` body: `{ github, linkedin, portfolio, leetcode, codeforces, others }`
- PATCH `/api/accounts/links/{id}/`
- DELETE `/api/accounts/links/{id}/`

### Permissions
- Only the profile owner can modify profile, education, experience, projects and social links.
- Skills are global; any authenticated user may create/search.

### Notes
- Uploads stored under `MEDIA_ROOT`; validate resume as PDF only.
- Use `Authorization: Bearer <access>` for protected routes.


