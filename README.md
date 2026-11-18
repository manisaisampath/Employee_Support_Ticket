# Employee Support Ticket Management System

## 1. Project Overview

The Employee Support Ticket Management System is a web-based application developed using Python Flask and SQLite.

It provides a centralized platform for organizations to manage employee technical support requests.

Employees can submit support tickets, track their progress, and communicate with support staff through comments. Support staff can view all submitted tickets, update their statuses, and respond to employee requests.

## 2. Problem Statement

Organizations need an organized system to manage employee technical issues and support requests.

Managing these requests manually can make it difficult to track ticket progress, maintain communication, and ensure timely resolution.

This application addresses the problem by providing a centralized ticket management platform with role-based access control.

## 3. Features

### Employee Features
- Secure login and authentication.
- Employee dashboard.
- Create new support tickets.
- View submitted tickets.
- Track ticket status.
- View individual ticket details.
- Add comments to their own tickets.
- Read support staff responses.

### Support Staff Features
- Secure login.
- Support dashboard.
- View all employee tickets.
- Search and filter tickets.
- View individual ticket details.
- Update ticket statuses.
- Add comments to any ticket.
- View ticket conversation history.

### Security Features
- Secure password hashing.
- Session-based authentication.
- Role-based access control.
- CSRF protection.
- Server-side input validation.
- Parameterized SQL queries.
- Secure session cookie configuration.
- Environment-based secret key configuration.

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Backend programming |
| Flask | Web framework |
| SQLite | Database |
| HTML5 | Frontend structure |
| CSS3 | User interface styling |
| JavaScript | Client-side functionality |
| Jinja2 | Template rendering |
| Pytest | Automated testing |
| Git | Version control |
| GitHub | Code hosting |

## 5. User Roles

The application supports two pre-seeded user accounts.

| Username | Role |
|---|---|
| ravi | Employee |
| support_admin | Support Staff |

Passwords are configured securely during database seeding and are not included in the repository.

### Employee Permissions
- Create support tickets.
- View only their own tickets.
- Add comments to their own tickets.
- Track ticket progress.

### Support Staff Permissions
- View all employee tickets.
- Update ticket statuses.
- Add comments to any ticket.
- Communicate with employees.

## 6. Ticket Management

### Ticket Categories
- Hardware
- Software
- Network
- Access
- Other

### Ticket Priorities
- Low
- Medium
- High

### Ticket Statuses
- Open
- In Progress
- Resolved
- Closed

New tickets automatically receive the Open status.

Ticket titles are required and limited to 100 characters. Descriptions are also required.

Only support staff can change ticket statuses. Employees cannot edit submitted ticket details.

## 7. Comment Management

The application provides a comment system for communication between employees and support staff.

- Employees can comment on their own tickets.
- Support staff can comment on any ticket.
- Comments display the author and timestamp.
- Empty comments are rejected.
- Comments cannot be edited or deleted.
- Comments are allowed even when a ticket is closed.
- Adding a comment updates the ticket's last updated date.

## 8. Database Design

The application uses SQLite with three main tables.

### Users
- id
- username
- password_hash
- role
- created_at

### Tickets
- id
- title
- description
- category
- priority
- status
- created_by
- created_date
- last_updated_date

### Comments
- id
- ticket_id
- author_id
- comment_text
- created_at

Primary keys, foreign keys, database constraints, and indexes are used to maintain data integrity.

## 9. Project Structure

```text
employee-support-ticket-app/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── security.py
│   ├── decorators.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── employee.py
│   │   └── support.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── employee/
│   │   ├── support/
│   │   └── errors/
│   │
│   └── static/
│       ├── css/
│       └── js/
│
├── tests/
├── schema.sql
├── seed.py
├── run.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 10. Installation and Setup

### Prerequisites
- Python 3.11 or later.
- Git.
- Visual Studio Code or another Python-compatible editor.

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd employee-support-ticket-app
```

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

### Step 3: Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 4: Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 5: Configure environment variables

Set a secret key in PowerShell:

```powershell
$env:SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
```

Configure seed passwords securely:

```powershell
$env:SEED_RAVI_PASSWORD = "YOUR_EMPLOYEE_PASSWORD"
$env:SEED_SUPPORT_PASSWORD = "YOUR_SUPPORT_PASSWORD"
```

Use strong passwords and never publish them in the repository.

### Step 6: Initialize and seed the database

```bash
python seed.py
```

The seed script creates the two application accounts and five sample tickets. It is designed to avoid duplicate records when executed repeatedly.

### Step 7: Run the application

```bash
python run.py
```

Open the application in your browser:

http://127.0.0.1:5000/

## 11. Running Automated Tests

The project uses Pytest for automated testing.

Run the test suite:

```bash
pytest -q
```

### Reported Test Results

```text
38 passed, 0 failed
```

The reported test suite covers:

- Application startup and configuration.
- Database schema and constraints.
- Database seeding.
- Authentication and password hashing.
- Role-based access control.
- Employee ticket creation.
- Ticket ownership and access restrictions.
- Support staff ticket management.
- Ticket status updates.
- Comment functionality.
- CSRF protection.
- Error handling.

## 12. AI Usage and Development Notes

### 12.1 What AI Generated

AI assistance was used during development to help generate and organize:

- Initial product prompt.
- Software Requirements Specification (SRS).
- Product requirements and user stories.
- Project implementation plan.
- Flask application structure.
- Database schema and model implementation.
- Authentication and role-based access control.
- Employee and support dashboard code.
- Ticket creation and status management functionality.
- Comment functionality.
- HTML templates, CSS, and JavaScript.
- Error handling and security improvements.
- Automated test cases.
- Technical documentation and README content.

### 12.2 What I Changed

During development and review, I made or directed the following changes:

- Refined the project requirements and clarified user permissions.
- Established the approved ticket categories, priorities, and statuses.
- Ensured employees could access only their own tickets.
- Ensured only support staff could update ticket statuses.
- Required CSRF protection for state-changing operations.
- Reviewed the generated application and its functionality.
- Identified a CSS loading issue during application testing.
- Corrected the stylesheet reference and verified that styling appeared in the browser.
- Reviewed and improved the frontend templates and styling.
- Prepared the project for GitHub and documentation submission.

### 12.3 What I Checked

The application was reviewed and tested for:

- Successful application startup.
- Login and logout functionality.
- Employee and support staff role restrictions.
- Employee ticket creation and viewing.
- Support staff ticket management.
- Ticket status updates.
- Comment functionality.
- Input validation.
- CSRF protection.
- Database constraints.
- Password hashing.
- CSS and static file loading.
- Error handling.

Automated testing was performed using Pytest.

**Reported result: 38 passed, 0 failed.**

Manual browser verification was also performed for application startup and the employee dashboard. Other workflows should be manually verified before production use.

### 12.4 Known Gaps and Limitations

The following features are not included in the current project scope:

- Email notifications are not implemented.
- Ticket attachment uploads are not implemented.
- Advanced analytics and reporting are not implemented.
- Individual support agent assignment is not implemented.
- The application currently uses SQLite.
- The application uses Flask's development server and is intended for local development.
- Production deployment and production server configuration have not been completed.

These features may be considered for future improvements.

### 12.5 Human Review and Responsibility

AI-generated code and documentation were reviewed during development.

The implementation was checked against the defined requirements, and identified issues were addressed.

The developer remains responsible for verifying the application behaviour, test results, security, and documentation before submission or deployment.

## 13. Git and Version Control

Git was used to track project changes and maintain version history.

Final implementation commit:

```text
a7b3f9c
```

Commit message:

```text
feat: complete employee support ticket management system
```

GitHub Repository:

YOUR_GITHUB_REPOSITORY_URL

## 14. Future Enhancements

Possible future improvements include:

- Email notifications for ticket updates.
- Ticket attachment support.
- Advanced analytics and reporting.
- Individual support agent assignment.
- Improved ticket filtering and search.
- Production deployment.

## 15. Conclusion

The Employee Support Ticket Management System provides a centralized platform for managing employee technical support requests.

It supports authentication, role-based access control, ticket creation, ticket tracking, status updates, and communication through comments.

The project demonstrates practical implementation of full-stack web development, database integration, application security, automated testing, Git version control, and technical documentation.

The reported automated test result was 38 passed and 0 failed.