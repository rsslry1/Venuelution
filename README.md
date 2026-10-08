# Cultural Venue and Equipment Booking Management System

## 1. Project Title

**Cultural Venue and Equipment Booking Management System**

A Django-based web application for managing venue reservations and equipment booking for events.

---

## 2. Project Description

The **Cultural Venue and Equipment Booking Management System** is a web-based application designed to manage the reservation of venues and the scheduling of equipment for events.

The system allows users to check venue availability, select a venue, choose the equipment they need, specify quantities, select a booking date and time, and submit a booking request for approval.

The system will initially support two venues:

- **Cultural Center**
- **Pavilion**

The system is designed to allow the Administrator to add additional buildings, rooms, halls, or establishments in the future.

The system has four main roles:

- **Administrator** – manages the overall system, users, venues, equipment, bookings, and reports.
- **Cultural Department** – reviews, approves, or rejects venue booking requests.
- **ICONS Department** – manages equipment availability, preparation, and allocation.
- **User / Booker** – submits venue and equipment booking requests and monitors their booking status.

The project uses **Django, Python, MySQL, HTML, CSS, JavaScript, and MySQL Workbench**.

---

## 3. Objectives

### General Objective

To develop a centralized web-based system for managing cultural venue reservations and equipment scheduling while maintaining accurate and consistent database records.

### Specific Objectives

- Provide a centralized platform for booking venues.
- Allow users to check venue availability by date and time.
- Allow users to request multiple equipment types and quantities.
- Check equipment availability for the selected booking schedule.
- Prevent conflicting venue bookings.
- Prevent over-allocation of equipment.
- Provide an approval workflow for booking requests.
- Allow the Cultural Department to approve or reject booking requests.
- Allow the ICONS Department to manage equipment allocation.
- Allow administrators to manage users, venues, equipment, and system information.
- Maintain booking status and history.
- Apply relational database concepts such as foreign keys, stored procedures, views, and transactions.

---

## 4. Key Features

### User Authentication and Role Management

- User login
- Role-based access
- Administrator, Cultural Department, ICONS Department, and User roles

### Venue Management

- Add and manage venues
- Set venue capacity
- Activate or deactivate venues
- View venue information

### Venue Availability

- View available venues
- Check availability by date and time
- Select start and end time
- Prevent conflicting venue bookings

### Booking Management

- Create booking requests
- Select a venue
- Enter event name and purpose
- Specify expected attendees
- Select booking date and time
- View booking status
- View booking history

### Equipment Management

- Manage equipment categories
- Manage equipment inventory
- Track equipment quantities
- Monitor equipment condition
- Monitor equipment availability

### Equipment Booking

- Select multiple equipment types
- Specify quantity for each equipment item
- Check equipment availability
- Prevent equipment over-allocation

### Approval Workflow

1. User submits a booking request.
2. Cultural Department reviews the request.
3. Cultural Department approves or rejects the request.
4. If approved, the ICONS Department receives the equipment request.
5. ICONS Department checks and prepares the equipment.
6. The system records the equipment allocation.

### Notifications

- Booking status notifications
- Booking-related notifications
- Updates for users and responsible departments

### Reports and History

- Booking history
- Booking status records
- Equipment schedules
- Equipment allocation records
- System reports

---

## 5. Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Main programming language |
| **Django** | Web application framework |
| **HTML** | Web page structure |
| **CSS** | Interface styling |
| **JavaScript** | Client-side functionality |
| **MySQL** | Relational database |
| **MySQL Workbench** | Database design and management |
| **Git** | Version control |
| **GitHub** | Source code repository |

---

## 6. Project Structure

```text
cultural-venue-booking-system/
│
├── src/
│   ├── manage.py
│   ├── project/
│   ├── accounts/
│   ├── venues/
│   ├── bookings/
│   └── equipment/
│
├── docs/
│   ├── project-documentation.md
│   └── database-design.md
│
├── uml/
│   ├── use-case-diagram.png
│   ├── class-diagram.png
│   ├── sequence-diagram.png
│   └── activity-diagram.png
│
├── database/
│   ├── schema.sql
│   ├── procedures.sql
│   └── views.sql
│
├── requirements.txt
├── .gitignore
└── README.md
```

> The project structure may be modified as development progresses.

---

## 7. Setup/Execution Instructions

### Prerequisites

Make sure the following are installed:

- Python
- Django
- MySQL Server
- MySQL Workbench
- Git

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd cultural-venue-booking-system
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

For Windows:

```bash
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Create the MySQL Database

Open MySQL or MySQL Workbench and create the project database.

```sql
CREATE DATABASE cultural_booking_db;
```

Configure the database connection in the Django project's settings.

### Step 5: Run Django Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create an Administrator Account

```bash
python manage.py createsuperuser
```

Follow the instructions to create the administrator account.

### Step 7: Run the Development Server

```bash
python manage.py runserver
```

Open the application in a browser:

```text
http://127.0.0.1:8000/
```

---

## 8. UML Diagrams

The following UML diagrams represent the proposed system design.

### Use Case Diagram

The Use Case Diagram identifies the major actors and the functionalities they perform in the system.

**Actors:**

- Administrator
- Cultural Department
- ICONS Department
- User / Booker

![Use Case Diagram](uml/use-case-diagram.png)

---

### Class Diagram

The Class Diagram represents the major classes, attributes, methods, and relationships of the system.

![Class Diagram](uml/class-diagram.png)

---

### Sequence Diagram

The Sequence Diagram illustrates the interaction between the user and system components during a major operation, such as submitting a venue and equipment booking request.

![Sequence Diagram](uml/sequence-diagram.png)

---

### Activity Diagram

The Activity Diagram illustrates the workflow of the booking process, including availability checking, booking submission, approval or rejection, and equipment allocation.

![Activity Diagram](uml/activity-diagram.png)