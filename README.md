Given the update that no specific framework is used in the front-end of your project, let's adjust the README.md template accordingly to better match your project's actual technical stack and setup. Here's the revised version without references to Vue.js, Nuxt.js, or any associated libraries and plugins.

---

# Auystyr - Online Book Exchange Platform
![Logo](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME/blob/main/assets/logo.png?raw=true)


## Overview

Auystyr is a pioneering online bookcrossing social platform specifically designed for the university community, focusing on facilitating the exchange of books among students and teachers at SDU. By integrating a robust system for book exchanges, user profiles, and event notifications, Auystyr aims to create a dynamic, environmentally friendly, and cost-effective community for book lovers.

### Target Audience

- Students aged 17-24
- Teachers aged 25-63

## Features

### Core Features

- **Book Exchange**: Central functionality that allows users to list books for exchange, search for available books, and initiate or respond to book exchange requests.
- **User Profiles**: Enables users to save or add necessary information for participating in the book exchange process.
- **Event Notifications**: Keeps users informed about bookcrossing events and other related activities within the university, offering both free and paid participation options.

### Performance Benefits

- **Event Features**: Provides timely news and descriptions for university-related book events, including an efficient payment system for paid events.
- **Integration with Kaspi**: Allows traditional payment methods for event participation.

### Unexpected Benefits

- **Interactive Games**: Offers tests and games for book enthusiasts, enhancing user engagement.
- **Intuitive Interface**: Ensures a user-friendly experience across the platform.

## Technology Stack

### Front-End

The front-end is developed with standard web technologies including HTML, CSS, and JavaScript, ensuring a responsive and accessible experience across all major browsers and devices.

### Back-End

- **Core**: Python, Django/REST Framework
- **Database**: PostgreSQL, Django-postgrespool 2.0
- **Server**: Deployed on an Apache server, with a Node.js front-end server proxied by Apache

### Integrations

- **Google Books API**: Automatically searches for and fetches book information based on the specified language.

## Deployment

The application is deployed on OVHCloud and Netlify, showcasing the responsiveness and compatibility across all major browsers and devices.

- [Visit the deployed website on OVHCloud](#)
- [Visit the deployed website on Netlify](#)

## Getting Started

### Prerequisites

- Python 3.8+
- Pipenv

### Installation

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   git pull
   ```

2. **Set Up the Back-End**

   Navigate to the cloned directory, then:

   ```bash
   sudo pipenv install
   sudo pipenv shell
   # Start the server
   python manage.py runserver
   # Make migrations
   python manage.py makemigrations
   python manage.py migrate
   ```

### Development and Production

Given the simplicity of the front-end, the development process mainly involves editing HTML, CSS, and JavaScript files directly. For seeing your changes, simply open the HTML files in a web browser. For a more advanced setup, consider using a live server plugin available in most code editors, such as Visual Studio Code, to automatically reload the browser on file changes.

---

This revised README.md reflects the absence of a specific front-end framework in your project while maintaining a clear and structured presentation of your project's details, goals, and setup instructions.
