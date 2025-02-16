# Little Lemon Booking System

## Project Overview
The **Little Lemon Booking System** is a web-based application designed to facilitate restaurant reservations for customers. This project is built using Django as the backend framework, MySQL as the database, and JavaScript for handling form interactions on the frontend. The system ensures efficient booking management, prevents duplicate reservations, and allows users to view and manage their bookings seamlessly.

## Features
- **User Authentication:** Secure login and registration functionality.
- **Booking Management:** Customers can create, update, and cancel reservations.
- **API Integration:** Provides a RESTful API for handling reservations.
- **Duplicate Prevention:** Ensures that duplicate reservations for the same time slot are not allowed.
- **Database Management:** Stores reservation details efficiently in MySQL.
- **Frontend Interactivity:** Uses JavaScript to enhance user experience with dynamic form validation.

## Technology Stack
### **Backend**
- Django (Python)
- Django REST Framework
- MySQL

### **Frontend**
- HTML
- CSS
- JavaScript

### **Tools & Deployment**
- Git & GitHub (version control)
- Postman (API testing)

## Setup & Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repo/little-lemon.git
   cd little-lemon
   ```
2. **Set Up Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Database:**
   - Update `settings.py` with your MySQL database credentials.
   - Run migrations:
     ```bash
     python manage.py migrate
     ```
5. **Start the Server:**
   ```bash
   python manage.py runserver
   ```
6. **Access the Application:**
   - Open `http://127.0.0.1:8000/` in your browser.

## API Endpoints
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/bookings/` | Retrieve all bookings |
| POST | `/api/bookings/` | Create a new booking |
| PUT | `/api/bookings/{id}/` | Update an existing booking |
| DELETE | `/api/bookings/{id}/` | Cancel a booking |

## Future Enhancements
- Implement email notifications for booking confirmations.
- Add user roles for admin and customers.
- Improve frontend UI with a modern JavaScript framework.

## License
This project is open-source and available under the MIT License.

