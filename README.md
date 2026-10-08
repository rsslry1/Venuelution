# Cultural Venue and Equipment Booking Management System

## Project Description

The **Cultural Venue and Equipment Booking Management System** is a web-based system designed to manage the reservation of cultural venues and the scheduling of equipment for events.

Instead of separately borrowing equipment and manually checking venue schedules, users can select an available venue, choose the equipment they need, specify quantities, select a booking date and time, and submit a booking request for approval.

The system will initially support the **Cultural Center** and **Pavilion**, while allowing administrators to add additional buildings, rooms, halls, or other establishments in the future.

The system uses **Django** for the web application, **MySQL** for the database, and **MySQL Workbench** for database design and management.

---

## Problem Being Addressed

The manual management of venue reservations and equipment requests can result in:

- Conflicting venue bookings
- Difficulty checking venue availability
- Over-allocation of equipment
- Difficulty tracking equipment quantities
- Delays in approving booking requests
- Lack of centralized booking records
- Difficulty monitoring booking history and equipment allocation

This system addresses these problems by providing a centralized platform for managing venue schedules, equipment availability, booking requests, approvals, and equipment allocation.

---

## Target Users / Stakeholders

The system has four main user roles:

### 1. Administrator

The Administrator manages the overall system, including:

- User accounts and roles
- Venues
- Equipment and equipment categories
- Bookings
- Reports
- System settings and master data

### 2. Cultural Department

The Cultural Department manages venue booking requests.

Responsibilities include:

- Reviewing booking requests
- Checking venue schedule conflicts
- Reviewing booking date and time
- Checking event purpose and attendee capacity
- Accepting or denying booking requests
- Monitoring approved and rejected bookings

### 3. ICONS Department

The ICONS Department manages equipment.

Responsibilities include:

- Managing equipment inventory
- Monitoring equipment availability and condition
- Reviewing equipment requests
- Confirming requested quantities
- Preparing and releasing equipment
- Updating equipment status when unavailable, damaged, or under maintenance

### 4. User / Booker

The User or Booker can:

- Log in
- View available venues
- Check venue availability
- Select a venue
- Select equipment
- Specify equipment quantities
- Select booking date and time
- Enter event details
- Submit booking requests
- View booking status and history

---

## Objectives

### General Objective

To develop a centralized web-based system for managing cultural venue reservations and equipment scheduling while maintaining accurate, consistent, and transactional database operations.

### Specific Objectives

- Provide users with a centralized platform for venue booking.
- Display venue availability based on date and time.
- Allow users to request multiple equipment types and quantities.
- Check equipment availability for the selected booking schedule.
- Prevent conflicting venue bookings.
- Prevent over-allocation of equipment.
- Provide an approval workflow for booking requests.
- Allow the Cultural Department to approve or reject venue bookings.
- Allow the ICONS Department to manage equipment allocation.
- Provide administrators with tools for managing users, venues, equipment, and system data.
- Maintain booking history and status records.
- Demonstrate database concepts using relational tables, stored procedures, views, foreign keys, and transactions.

---

## Key Features

### Authentication and Role Management
- User login
- Role-based access
- Administrator, Cultural Department, ICONS Department, and User roles

### Venue Management
- Add and manage venues
- Configure venue capacity
- Activate or deactivate venues
- View venue information

### Venue Availability
- Check available dates
- Check available start and end times
- Prevent conflicting venue bookings
- Manage blocked schedules

### Booking Management
- Create booking requests
- Enter event name and purpose
- Specify expected attendees
- Select booking date and time
- Track booking status
- View booking history

### Equipment Management
- Manage equipment categories
- Manage equipment inventory
- Track equipment quantities
- Monitor equipment condition
- Monitor equipment availability

### Equipment Scheduling
- Select multiple equipment types
- Specify quantity for each equipment item
- Check equipment availability for a specific date and time
- Prevent equipment over-allocation

### Approval Workflow
1. User submits a booking request.
2. Cultural Department reviews the venue booking.
3. Cultural Department accepts or denies the request.
4. If approved, the ICONS Department receives the equipment request.
5. ICONS Department checks and prepares the equipment.
6. The system records the equipment allocation.

### Notifications
- Booking status notifications
- Booking-related system notifications
- Updates for users and responsible departments

### Reports and History
- Booking history
- Booking status records
- Equipment schedules
- Equipment allocation records
- System reports

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Programming Language |
| Django | Web Application Framework |
| HTML | User Interface Structure |
| CSS | User Interface Styling |
| JavaScript | Client-side functionality |
| MySQL | Relational Database |
| MySQL Workbench | Database Design and Management |
| Git | Version Control |
| GitHub | Source Code Repository |

---

## Database Design

The proposed database contains **10 related tables**:

1. `users`
2. `venues`
3. `equipment_categories`
4. `equipment`
5. `bookings`
6. `booking_equipment`
7. `venue_schedules`
8. `equipment_allocations`
9. `booking_status_history`
10. `notifications`

### Important Relationships

- Users → Bookings
- Venues → Bookings
- Equipment Categories → Equipment
- Bookings → Booking Equipment
- Equipment → Booking Equipment
- Venues → Venue Schedules
- Bookings → Equipment Allocations
- Equipment → Equipment Allocations
- Bookings → Booking Status History
- Users → Notifications

The `booking_equipment` table handles the many-to-many relationship between bookings and equipment.

---

## Stored Procedures

The system proposes the following MySQL stored procedures:

- `GetAvailableVenues`
- `CheckVenueAvailability`
- `CheckEquipmentAvailability`
- `CreateBooking`
- `AddBookingEquipment`
- `ApproveBooking`
- `RejectBooking`
- `AllocateEquipment`
- `CompleteBooking`
- `GetUserBookingHistory`

These procedures support venue availability checking, equipment availability checking, booking creation, approval, rejection, equipment allocation, and booking history.

---

## MySQL Views

The system includes the following proposed database views:

- `vw_available_venues`
- `vw_booking_details`
- `vw_booking_equipment`
- `vw_equipment_schedule`
- `vw_booking_history`

These views provide consolidated information for venue availability, booking details, equipment schedules, and booking history.

---

## Transactional Operations

Booking operations use database transactions to maintain data consistency.

The proposed transaction follows this process:

```text
BEGIN TRANSACTION
        ↓
Check Venue Availability
        ↓
Check Equipment Availability
        ↓
Create Booking
        ↓
Add Booking Equipment
        ↓
Reserve / Allocate Resources
        ↓
Record Status and Approval Information
        ↓
COMMIT
```

If any operation fails, the system performs a **ROLLBACK** to prevent incomplete bookings or incorrect equipment reservations.

---

## Project Structure

The repository will follow a structure similar to:

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

> The exact folder and file structure may be adjusted as development progresses.

---

## Setup / Execution Instructions

### Prerequisites

Install the following:

- Python
- Django
- MySQL Server
- MySQL Workbench
- Git

### 1. Clone the Repository

```bash
git clone <repository-url>
cd cultural-venue-booking-system
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment.

**Windows:**

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

Create a MySQL database for the project.

Example:

```sql
CREATE DATABASE cultural_booking_db;
```

Configure the database connection in the Django project settings.

### 5. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create an Administrator Account

```bash
python manage.py createsuperuser
```

Follow the prompts to create the administrator account.

### 7. Run the Development Server

```bash
python manage.py runserver
```

Open the development server in a web browser:

```text
http://127.0.0.1:8000/
```

---

# UML Diagrams

The following UML diagrams represent the proposed design of the system.

## 1. Use Case Diagram

The Use Case Diagram identifies the four major actors:

- Administrator
- Cultural Department
- ICONS Department
- User / Booker

It represents the primary functions performed by each actor.

![Use Case Diagram](uml/use-case-diagram.png)

---

## 2. Class Diagram

The Class Diagram represents the major classes, attributes, methods, and relationships within the system.

![Class Diagram](uml/class-diagram.png)

---

## 3. Sequence Diagram

The Sequence Diagram illustrates the interaction between system components during a major system operation, such as submitting a venue and equipment booking request.

![Sequence Diagram](uml/sequence-diagram.png)

---

## 4. Activity Diagram

The Activity Diagram illustrates the workflow of the booking process, including venue availability checking, equipment availability checking, approval, rejection, and equipment allocation.

![Activity Diagram](uml/activity-diagram.png)

---

## Core Booking Workflow

```text
User Login
    ↓
View Available Venues
    ↓
Select Venue
    ↓
Select Date and Time
    ↓
Check Venue Availability
    ↓
Enter Event Details
    ↓
Select Equipment and Quantities
    ↓
Check Equipment Availability
    ↓
Submit Booking Request
    ↓
Cultural Department Review
    ↓
 ┌───────────────┐
 │ Approved?     │
 └───────┬───────┘
         │
    ┌────┴────┐
    │         │
   Yes        No
    │         │
    ↓         ↓
ICONS      Booking
Review     Rejected
    │
    ↓
Equipment Allocation
    ↓
Final Booking Record
```

---

## Development Status

**Current Stage:** Project Initialization and UML Design

A fully working system is **not required at this stage**. The repository is intended to demonstrate that development has officially begun through:

- Project documentation
- Initial project structure
- Database design
- UML diagrams
- Configuration files
- Initial source code

Development will continue by implementing the database, Django application modules, authentication, booking workflow, equipment management, and approval process.

---

## Future Enhancements

Future versions may support:

- Additional venues and establishments
- More equipment categories
- Advanced calendar scheduling
- Automated notifications
- Detailed reports and analytics
- Improved equipment tracking
- Booking cancellation and modification
- Enhanced administrator controls

---

## Project Requirements Alignment

| Requirement | Implementation |
|---|---|
| Web Application | Django-based web application |
| At least 5 Tables | 10 related database tables |
| Stored Procedures | Availability, booking, approval, rejection, and allocation procedures |
| Database Views | 5 proposed MySQL views |
| Transactions | Booking and equipment allocation transactions |
| MySQL Workbench | Database design, ERD, SQL, procedures, views, and testing |
| UML Design | Use Case, Class, Sequence, and Activity Diagrams |
| Version Control | Git and GitHub |

---

## License

This project is developed as an academic capstone project.
