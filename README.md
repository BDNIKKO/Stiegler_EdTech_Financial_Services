# Nexus Lending Solutions

Developed by:
- Brandon Herrschaft: Backend Developer and Data Engineer - https://github.com/bherrschaft
- Nicholas Moppert: Frontend Developer - https://github.com/BDNIKKO
- Dewey Adkins: IT Support Specialist

Honorable Mentions:
- CTAC Instructors and TA's for their support and guidance thorughout the last 6 months of the cohort.
- The Data Engineering team at Live Oak Bank for their input on our project during the planning phase. 
- Our families for their love and support throughout our career change journey.

Welcome to our capstone project! We've built a loan application platform that makes the lending process 
way less painful for everyone involved. Here's what makes it cool:

- Instant loan decisions using our custom Logestic Regression ML model.
- Clean, modern interface
- Real Business Owner dashboard for tracking applications and analytics 
- Actual database management with pgAdmin4
- Freshdesk integration for support tickets
- Everything runs in Docker, so it's super easy to get started

The whole idea was to push the limits of what we could achieve during our time learning in the CTAC cohort and this is the culmination of our work. 
We wanted to make sure we had features for users and business owners, and to also serve as a template for future developers to use.

We hope you enjoy using Nexus Lending Solutions as much as we enjoyed building it. 


## Key Features

### 🧑‍💼 For Users
- **Secure Authentication**
  - JWT-based authentication system
  - Secure password handling

- **Smart Loan Application**
  - Intelligent loan decisioning using hybrid approach:
    - Direct approval for high-quality applications
    - ML-powered assessment for complex cases
  - Multiple evaluation factors:
    - Debt-to-income ratio
    - Loan-to-income ratio
    - Employment Length
    - Credit score prediction based upon related factors
    - Income
    - Loan Amount
    - Loan Term
  - Real-time decision feedback
  - Transparent metrics display

- **Personal Dashboard**
  - Application status tracking
  - Financial journey overview
  - Quick access to new applications
  - Integrated support ticket system

- **Support & Information**
  - Comprehensive "About Us" section
  - Company mission and values
  - Transparent business practices
  - Direct support access

### 👔 For Business Owners
- **Administrative Control**
  - Comprehensive loan analytics dashboard
  - Real-time application monitoring
  - Decision tracking system

- **Data Management**
  - Secure PostgreSQL database
  - Structured data organization
  - Analytics tracking tables
  - Automated reporting
  - Automated ETL process for incoming applications

- **Security Features**
  - Role-based access control
  - Secure data encryption

### 👩‍💻 For Developers
- **Modern Tech Stack**
  - React.js frontend
  - Flask backend
  - PostgreSQL database
  - RESTful API architecture
  - Docker containerization
  - pgAdmin4 for database management

- **UI/UX Design**
  - Responsive design system
  - Modern CSS styling
  - Consistent theming
  - Interactive components
  - Mobile-first approach

- **Code Organization**
  - Modular component structure
  - Clear routing system
  - Consistent naming conventions
  - Well-documented codebase

## Technical Architecture

### Services
- Frontend (React.js) - Port 3000
- Backend (Flask) - Port 5000
- PostgreSQL Database - Port 5432
- pgAdmin4 - Port 8080
- Scheduler (Cron Jobs)

### Prerequisites
- Docker
- Docker Compose

### Quick Start

1. Clone the repository:


git clone https://github.com/BDNIKKO/Stiegler_EdTech_Financial_Services.git


2. Start all services:

docker compose up --build


The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- pgAdmin: http://localhost:8080

### React Frontend Architecture

Our React frontend provides an intuitive user interface with real-time updates and responsive design. Here's how it's structured:

#### Core Features
- **Authentication & Navigation**
  - JWT token management for secure sessions
  - Role-based navigation (admin vs standard users)
  - Protected routes with automatic redirects
  ```javascript:frontend/src/components/Dashboard.js
  startLine: 37
  endLine: 47
  ```

#### User Dashboard
- **Personal Overview**
  - Loan application status tracking
  - Financial statistics display
  - Quick action buttons for common tasks
  ```javascript:frontend/src/components/Dashboard.js
  startLine: 81
  endLine: 144
  ```

#### Analytics Dashboard (Admin Only)
- **Real-time Metrics**
  - Application counts and approval rates
  - Average loan amounts
  - Decision distribution
  - Interactive progress bars
  ```javascript:frontend/src/components/LoanAnalytics.js
  startLine: 127
  endLine: 166
  ```

#### UI/UX Design
- **Modern Styling**
  - Glassmorphism design elements
  - Responsive grid layouts
  - Custom scrollbars
  - Smooth animations and transitions
  ```css:frontend/src/components/LoanAnalytics.css
  startLine: 31
  endLine: 40
  ```

#### Data Management
- **API Integration**
  - Real-time data fetching
  - Error handling with user feedback
  - Loading states for better UX
  ```javascript:frontend/src/components/LoanAnalytics.js
  startLine: 49
  endLine: 95
  ```

The frontend is built with React and uses modern CSS for styling, with a focus on user experience and responsive design. All components are containerized using Docker and communicate with the Flask backend through RESTful API endpoints.


### Flask Backend Architecture

Our Flask backend serves as the core of the application, handling multiple critical functions:

#### Authentication & Security
- **User Management**
  - Secure registration and login system
  - Password hashing using SHA-256
  - JWT token generation with 3-hour expiration
  - Role-based access control (admin vs standard users)
#### Loan Processing
- **ML Integration**
  - Loads pre-trained logistic regression model
  - Processes loan applications in real-time
  - Handles feature scaling and predictions
  - Returns instant loan decisions

#### Database Operations
- **SQLAlchemy ORM**
  - User data management
  - Loan application storage
  - Analytics data tracking
  - Relationship handling between tables

#### API Endpoints
- **User Routes**
  - `/api/register`: New user registration
  - `/api/login`: User authentication
  - `/api/user/loans`: Personal loan history

- **Loan Routes**
  - `/api/predict`: ML model predictions
  - `/api/loan-applications/list`: Application management
  - `/api/loan-analytics`: Analytics data

#### Support Integration
- **Freshdesk Integration**
  - Ticket creation and management
  - Support request handling
  - Status tracking
  - Error logging

#### Analytics Processing
- **Real-time Metrics**
  - Application counts
  - Approval rates
  - Average loan amounts
  - Decision distribution tracking

The backend is containerized using Docker and communicates with other services including PostgreSQL for data storage, the React frontend for user interface, and the scheduler service for automated tasks.

### Database Management (pgAdmin)

Access pgAdmin through http://localhost:8080 with:
- Email: admin@example.com
- Password: admin

The database server is pre-configured in pgAdmin with:
- Host: postgres
- Port: 5432
- Database: admin
- Username: admin
- Password: admin


### Scheduler Service

The application includes a scheduler service that automatically processes loan applications and updates analytics. Think of it as our ETL (Extract, Transform, Load) pipeline - it runs every 2 minutes to:

1. Extract new loan applications from the loan table in the database
2. Transform the data by calculating important metrics:
   - Total applications
   - Approval rates
   - Average loan amounts
   - Decision distribution
3. Load the processed data into the loan_analytics table
4. Analytics dashboard then pulls from this optimized table in real-time (refreshed every 2 minutes)

#### Technical Details
- Runs in its own Docker container using Python and cron
- Configuration files:
  - `backend/Dockerfile.scheduler`: Container setup
  - `crontab`: Job scheduling (runs every 2 minutes)
  - ETL logs: Mounted at `/var/log/etl.log` for debugging


## User Access Guide

### 🔐 User Registration & Authentication

#### Standard User Registration
1. Navigate to the registration page
2. Required fields:
   - Username (unique)
   - Password
   - First Name
   - Last Name
   - Phone
   - Email
   - Address

#### User Feature Navigation
1. Navigate to the login page and sign in.
2. The Dashboard will give you access to the following features:
   - Loan Application Link
   - Support Desk Link
   - About Us Link
3. Real-time loan application status updates will be displayed on the Dashboard.

#### Accessing Business Owner Features
1. Navigate to the login page
2. Use the following credentials:
   - Username: admin
   - Password: admin123
3. Navigate to Dashboard
4. Click on Loan Dashboard which only appears after logging in as an admin. 
5. **Note:** There are no pre-nested applications in the Loan Table. You will need to manually add applications to view the analytics dashboard.
6. After adding applications you will need to wait for the scheduler to transform the data and move it into the loan-analytics table which occurs every 2 minutes.
7. The Loan Analytics Dashboard will automatically update with the new data every 2 minutes. 

#### Database Management Tools Navigation
1. In the docker desktop application navigate to the containers tab.
2. Open pgAdmin4 by clicking on the port number 8080. Alternatively you can navigate to http://localhost:8080 in your web browser. 
3. Use the following credentials to sign in:
   - Username: admin@example.com
   - Password: admin
4. Click on Servers drop down on the left which will prompt you to enter a password which is 'admin'.
5. You will then have access to all of the databases and tables used to serve the application. All of our tables are in the "admin" database.


Thank you for checking out our project! 
