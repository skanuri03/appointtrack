# AppointTrack - Medical Appointment Manager

A secure web application for healthcare providers and patients to manage medical appointments.

## Features

### Core Functionality
- 🔐 **User Authentication**
  - Secure registration and login
  - Password hashing
- 📅 **Appointment Management**
  - Create, view, edit, delete appointments
  - Track: Provider, Date/Time, Reason, Status

### Advanced Features
- 🔍 **Smart Filtering**
  - Filter by status (Upcoming/Completed/Cancelled)
  - Sort by date or provider
- 📊 **Dashboard**
  - Visual appointment statistics
  - Upcoming appointments summary

## Installation

### Requirements
- Python 3.6+
- XAMPP (for MySQL)
- Modern web browser

### Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
2. Start MySQL in XAMPP
3. Run the application
    python app.py
## Configuration
Edit `config.py` if needed:
```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_DB = 'appointtrack'
```

## First-Time Setup
1. Access http://localhost:5000
2. Register a new account
3. Start adding appointments


## Project structure

appointtrack/
├── app.py                # Main application
├── appointtrack.sql      # Database schema
├── config.py             # Configuration
├── requirements.txt      # Dependencies
├── static/               # Static files
│   ├── css/              # Stylesheets
│   └── images/           # App assets
└── templates/            # HTML templates
    ├── base.html         # Main template
    ├── login.html        # Login page
    ├── register.html     # Registration
    ├── appointments.html # Dashboard
    └── add_edit_appointment.html # Form

## Troubleshooting
### Common Issues
- **MySQL Connection Failed**: Verify XAMPP MySQL service is running
- **Template Errors**: Check all files exist in /templatesecho - **Missing Packages**: Run `pip install flask flask-mysqldb flask-login`

## License
MIT License
