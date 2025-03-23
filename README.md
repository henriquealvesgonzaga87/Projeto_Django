# Recipes Project

Welcome to the **Recipes Project**! This repository is dedicated to storing and sharing delicious recipes from around the world.

## Overview

This project is a Django-based web application designed to manage and serve content. It includes several apps such as `authors`, `recipes`, and `tag`, and is structured to support scalability and maintainability. The project also includes utilities, templates, and static files for a complete web application experience.

## Project Structure
├── .coveragerc # Configuration for test coverage<br>
├── .env # Environment variables file<br>
├── .env-example # Example environment variables file<br>
├── .gitignore # Git ignore file<br>
├── manage.py # Django management script<br>
├── pytest.ini # Configuration for pytest<br>
├── requirements.txt # Python dependencies<br>
├── authors/ # Authors app<br>
│ ├── init.py<br>
│ ├── admin.py<br>
│ ├── apps.py<br>
│ ├── models.py<br>
│ ├── serializers.py<br>
│ ├── signals.py<br>
│ ├── urls.py<br>
│ ├── validators.py<br>
│ ├── forms/ # Forms for the authors app<br>
│ ├── migrations/ # Database migrations<br>
│ ├── templates/ # Templates for the authors app<br>
│ ├── tests/ # Unit tests for the authors app<br>
│ └── views/ # Views for the authors app<br>
├── base_static/ # Global static files<br>
├── base_templates/ # Global templates<br>
├── bin/ # Scripts and binaries<br>
├── locale/ # Localization files<br>
├── media/ # Media files<br>
├── project/ # Core project files<br>
├── recipes/ # Recipes app<br>
├── tag/ # Tag app<br>
├── tests/ # Project-wide tests<br>
└── utils/ # Utility functions and helpers<br>


## Features

- A collection of diverse recipes.
- Easy-to-follow instructions.
- Organized by categories for convenience.
- **Authors App**: Manage authors and related data.
- **Recipes App**: Handle recipes and their metadata.
- **Tag App**: Manage tags for categorization.
- **Global Templates and Static Files**: Shared resources for the entire project.
- **Localization**: Support for multiple languages.

## Requirements

- Python 3.11+
- Django 5.0.6

## Getting Started

1. Clone the repository:
    ```bash
    git clone https://github.com/henriquealvesgonzaga87/Projeto_Django.git
    ```

2. Navigate to the project directory:
    ```bash
    cd <repository-folder>
    ```

3. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Set up the environment variables:
    - Copy .env-example to .env and update the values as needed.

6. Apply migrations:
    ```bash
    python manage.py migrate
    ```

7. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Testing<br>
Run the tests using pytest:
```bash
    pytest
```

## Contributing

We welcome contributions! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

---

Happy cooking! 🍳