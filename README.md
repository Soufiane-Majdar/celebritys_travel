# Celebrity's Travel - Moroccan Travel Agency Website

A professional travel agency website built with Django and Bootstrap, offering luxury tours, cultural experiences, and Umrah services in Morocco.

## Features

- Dynamic and responsive design
- Trip management system
- Blog with commenting system
- Testimonials
- Newsletter subscription
- Contact form
- Admin interface for content management
- SEO optimized

## Tech Stack

- Django 4.2.7
- Bootstrap 5.3
- CKEditor for rich text editing
- Django Crispy Forms with Bootstrap 5
- Django Compressor for static files
- Python 3.8+

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd celebritys_travel
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to view the website.
Visit http://127.0.0.1:8000/admin/ to access the admin interface.

## Project Structure

```
celebritys_travel/
├── blog/               # Blog app
├── core/              # Core functionality
├── trips/             # Trips and tours management
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
├── media/            # User-uploaded files
└── celebritys_travel/ # Project settings
```

## Color Palette

- Primary Colors:
  - Desert Gold: #D4AF37
  - Deep Blue: #002F6C
- Secondary Colors:
  - Neutral White: #FFFFFF
  - Soft Gray: #F5F5F5
- Accent Color:
  - Vibrant Orange: #FFA500

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any inquiries, please contact [Your Contact Information].
