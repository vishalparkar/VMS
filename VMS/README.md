IMP - Please wait before testing this. Will update a few points in the code shortly and remove this notice.

# VMS Django Project

## Project Overview

VMS (Vendor Management System) is a Django-based web application designed to manage vendor information, purchase orders, and performance metrics efficiently.

## Features

- Vendor Management: Create, update, and delete vendor information.
- Purchase Orders: Manage purchase orders associated with vendors.
- Performance Metrics: Track and analyze vendor performance over time.

## Technologies Used

- Django 5.0.4
- Django REST Framework
- SQLite (for development)
- PostgreSQL (for production)

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip
- virtualenv

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/vishalparkar/VMS.git
   ```
2. Navigate to the project directory:
   ```bash
   cd VMS-Django-Project
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```
5. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Project

1. Make migrations and migrate the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
2. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the MIT License.


### Testing the API

Ensure that you have curl OR HTTPie installed on your machine to use the below commands.

Using `curl`

To test the API endpoints with curl, you can use the following command format:

List all vendors:
curl -X GET http://localhost:8000/api/vendors/ -H 'Accept: application/json'

Create a new vendor:
curl -X POST http://localhost:8000/api/vendors/ -H 'Content-Type: application/json' -d '{"name": "New Vendor", "contact_details": "Contact Info", "address": "Vendor Address", "vendor_code": "V123"}'


Replace http://localhost:8000/ with the desired main domain

Using `HTTPie`
HTTPie is a user-friendly HTTP client that can be used from the terminal. Here's how you can test the same operations:

List all vendors:
http GET http://localhost:8000/api/vendors/

Create a new vendor:
http POST http://localhost:8000/api/vendors/ name='New Vendor' contact_details='Contact Info' address='Vendor Address' vendor_code='V123'


Again, Replace http://localhost:8000/ with the desired main domain
