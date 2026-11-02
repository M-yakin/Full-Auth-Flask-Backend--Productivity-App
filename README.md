# Productivity App - Workout Logger API

A secure Flask RESTful API backend featuring session-based authentication and full user-owned CRUD operations for tracking workouts.

## Project Description
This backend supports multi-user workout logging with strict access controls. Each user must authenticate to create, view, update, or delete their personal workout records.

## Features
- **Session Authentication:** Login, Signup, Logout, and Session persistence checks (`/me`, `/check_session`).
- **Resource Management:** User-owned `Workout` resource with full CRUD permissions.
- **Data Protection:** Flask-Bcrypt hashed passwords and session authorization.
- **Pagination:** Index queries support page (`?page=1`) and item count (`&per_page=10`) pagination parameters.

## Installation Instructions

1. **Clone the repository and enter project directory:**
   ```bash
   git clone <YOUR_REPO_URL>
   cd Full-Auth-Flask-Backend--Productivity-App
