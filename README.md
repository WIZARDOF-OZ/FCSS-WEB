# Fatima Convent Senior Secondary School Website

A Django-based school website for Fatima Convent Senior Secondary School. This web application provides a homepage with dynamic banner content, an about page for school history and principal details, a gallery page with categorized media, and a contact page placeholder.

## Features

- Homepage with banner image management via Django admin.
- About page with principal profile, school story, and descriptive content.
- Gallery page with category-based image display.
- Admin dashboard support for managing banners, about content, and gallery items.
- Static asset support for CSS, JavaScript, and image resources.
- Easy customization through Django models and templates.

## Technology Stack

- Python 3
- Django
- SQLite (default database)
- HTML/CSS/JavaScript for frontend templates

## Installation

1. Clone the repository:

```bash
git clone https://github.com/mrinmoy-hex/FCSS-WEB.git
```

2. Navigate to the project directory:

```
 cd your-project
```

3. Activate the Python virtual environment:

- On Windows PowerShell:

```powershell
myenv\Scripts\Activate.ps1
```

- On Windows Command Prompt:

```cmd
myenv\Scripts\activate.bat
```

- On macOS/Linux:

```bash
source myenv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Setup

1. Apply database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

2. Create a superuser so you can access the Django admin:

```bash
python manage.py createsuperuser
```

3. Collect static files for production or testing static serving:

```bash
python manage.py collectstatic
```

## Run the App

Start the development server:

```bash
python manage.py runserver
```

Then open your browser at:

```text
http://127.0.0.1:8000/
```

## Pages

- `/` &ndash; Home page with school banner slideshow.
- `/about/` &ndash; About page with principal information, school story, and school description.
- `/gallery/` &ndash; Gallery page showing categorized images and media.
- `/contact/` &ndash; Contact page placeholder.

## Customization

- Edit `SchoolApp/settings.py` for project settings.
- Admin-managed content is stored in the `App` models:
  - `Banner`
  - `About`
  - `GalleryItem`
- Templates live in the `templates/` folder.
- Static assets are located in `static/` and `staticfiles/`.

## Notes

- The project uses `media/` for uploaded images and videos.
- Static-site assets are served from `staticfiles/` when `collectstatic` is run.

## Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch:

```bash
git checkout -b feature/your-feature
```

3. Make your changes and commit:

```bash
git commit -m "Add new feature"
```

4. Push the branch:

```bash
git push origin feature/your-feature
```

5. Open a pull request.
