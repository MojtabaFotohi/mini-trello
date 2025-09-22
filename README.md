# Mini Trello: Collaborative Task Management 🌟


[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/downloads/release/python-3130/)
[![Django](https://img.shields.io/badge/Django-5.2.6-green)](https://www.djangoproject.com/)
[![Celery](https://img.shields.io/badge/Celery-5.5.3-orange)](https://docs.celeryq.dev/en/stable/)
[![Redis](https://img.shields.io/badge/Redis-7.0-red)](https://redis.io/)
[![RabbitMQ](https://img.shields.io/badge/RabbitMQ-4.0-purple)](https://www.rabbitmq.com/)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)
[![Languages](https://img.shields.io/badge/Languages-12-yellow)](#multi-language-support)

**Mini Trello** is a modern, collaborative task management platform inspired by Trello, built with **Django REST Framework**. It offers user authentication, board/list/task management, email-based invitations, and supports **12 languages** with RTL for Persian and Arabic. The project leverages **Celery** for asynchronous tasks, **RabbitMQ** as the message broker, and **Redis** as the result backend. The UI is responsive, powered by **Bootstrap**, **Font Awesome**, **SortableJS** for drag-and-drop, and **SweetAlert2** for elegant alerts.

---

## ✨ Features

- **User Management**:
  - Register, login, and edit profiles with **JWT** authentication.
  - Custom user model with name, email, and preferred language.
- **Boards**:
  - Create, edit, and delete boards with customizable colors.
  - Limits: Max **5 boards** per user, **10 members** per board, **20 memberships** per user.
  - View board members with interactive tooltips.
- **Lists & Tasks**:
  - CRUD operations for lists and tasks.
  - Drag-and-drop tasks between lists with due dates and ordering.
- **Invitations**:
  - Invite members via email (sent asynchronously with Celery).
  - Track invitation status: *Pending*, *Accepted*, *Rejected*.
  - Accept/Reject invitations via API or UI.
- **Multi-Language Support**:
  - Supports **12 languages** with RTL for Persian (🇮🇷) and Arabic (🇸🇦).
  - Languages: 🇺🇸 English, 🇮🇷 Persian, 🇸🇦 Arabic, 🇩🇪 German, 🇫🇷 French, 🇮🇹 Italian, 🇮🇳 Hindi, 🇰🇷 Korean, 🇨🇳 Simplified Chinese, 🇯🇵 Japanese, 🇷🇺 Russian, 🇹🇷 Turkish, 🇪🇸 Spanish.
- **Responsive UI**:
  - Built with **Bootstrap 5.3.3** for responsive design.
  - **Font Awesome 6.4.0** for icons.
  - **SortableJS 1.15.0** for drag-and-drop functionality.
  - **SweetAlert2** for user-friendly notifications.
  - Custom animations (fadeInUp, bounce) and RTL support.
- **Asynchronous Processing**:
  - Email sending via **Celery**, **RabbitMQ**, and **Redis**.
- **Custom Management Command**:
  - `python manage.py scu` creates a superuser with credentials `admin`/`admin`.
- **API Documentation**:
  - Interactive **Swagger UI** at `/swagger/`.
  - Readable **ReDoc** at `/redoc/`.

---

## 🛠 Prerequisites

- Python 3.13+
- Django 5.2.6
- Celery 5.5.3
- Redis 7.0+
- RabbitMQ 4.0+
- SQLite (default) or PostgreSQL
- Node.js/CDNs for UI libraries (Bootstrap, Font Awesome, SortableJS, SweetAlert2)

---

## 🚀 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/MojtabaFotohi/mini-trello.git
   cd trelloProject/trello
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```


4. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser**:
   ```bash
   python manage.py scu  # Creates superuser (admin/admin)
   ```


6. **Run Development Server**:
   ```bash
   python manage.py runserver
   ```

---

## 🐳 Setting Up Celery, RabbitMQ, and Redis

1. **Install Redis**:
   ```bash
   sudo apt update
   sudo apt install redis-server
   sudo systemctl enable redis-server
   sudo systemctl start redis-server
   redis-cli ping  # Should return "PONG"
   ```

2. **Install RabbitMQ**:
   ```bash
   sudo apt update
   sudo apt install rabbitmq-server
   sudo systemctl enable rabbitmq-server
   sudo systemctl start rabbitmq-server
   sudo rabbitmqctl add_user celery_user moji
   sudo rabbitmqctl add_vhost celery_vhost
   sudo rabbitmqctl set_permissions -p celery_vhost celery_user ".*" ".*" ".*"
   ```

3. **Run Celery Worker**:
   ```bash
   celery -A trello worker --loglevel=info
   ```

---

## 🌍 Multi-Language Support

Mini Trello supports **12 languages** with translations managed via Django’s i18n framework in the `locale/` directory.

### Supported Languages
| Language                | Code      | Flag |
|-------------------------|-----------|------|
| English                 | `en`      | 🇺🇸  |
| Persian                 | `fa`      | 🇮🇷  |
| Arabic                  | `ar`      | 🇸🇦  |
| German                  | `de`      | 🇩🇪  |
| French                  | `fr`      | 🇫🇷  |
| Italian                 | `it`      | 🇮🇹  |
| Hindi                   | `hi`      | 🇮🇳  |
| Korean                  | `ko`      | 🇰🇷  |
| Japanese                | `ja`      | 🇯🇵  |
| Russian                 | `ru`      | 🇷🇺  |
| Turkish                 | `tr`      | 🇹🇷  |
| Spanish                 | `es`      | 🇪🇸  |

### Adding a New Language
1. Add the language to `LANGUAGES` in `settings.py`:
   ```python
   LANGUAGES = [
       # ... other languages ...
       ('xx', 'New Language'),
   ]
   ```
2. Generate translation file:
   ```bash
   python manage.py makemessages -l xx
   ```
3. Edit `locale/xx/LC_MESSAGES/django.po` with translations.
4. Compile translations:
   ```bash
   python manage.py compilemessages
   ```
5. Test by setting `preferred_language` to `xx` in the user model.

---

## 📚 API Documentation

Access interactive API docs:
- **Swagger UI**: `http://localhost:8000/swagger/` (Test endpoints directly).
- **ReDoc**: `http://localhost:8000/redoc/` (Readable documentation).

Key Endpoints:
- **Auth**: `/api/token/` (POST for JWT login), `/api/token/refresh/` (POST).
- **Users**: `/users/register/` (POST), `/users/profile/` (GET/PATCH).
- **Boards**: `/boards/` (GET/POST), `/boards/{id}/` (GET/PATCH/DELETE).
- **Lists**: `/lists/boards/{board_id}/lists/` (GET/POST), `/lists/lists/{id}/` (GET/PATCH/DELETE).
- **Tasks**: `/lists/lists/{list_id}/tasks/` (GET/POST), `/lists/tasks/{id}/` (GET/PATCH/DELETE).
- **Invitations**: `/invitations/` (GET/POST), `/invitations/{id}/accept/` (PATCH), `/invitations/{id}/reject/` (PATCH).

---

## ⚙️ Custom Management Command

The project includes a custom command to simplify superuser creation:
```bash
python manage.py scu
```
- Creates a superuser with username: `admin`, password: `admin`, email: `admin@gmail.com`.

---

## 🎨 UI/UX Highlights

- **Responsive Design**: Built with Bootstrap for mobile and desktop compatibility.
- **Drag-and-Drop**: SortableJS enables smooth task/list reordering.
- **Animations**: Custom fadeInUp and bounce animations for a polished experience.
- **Icons**: Font Awesome for intuitive visual elements.
- **Alerts**: SweetAlert2 for elegant, user-friendly notifications.
- **RTL Support**: Seamless right-to-left layout for Persian and Arabic.

---

## 📏 Limitations

- **Boards**: Max 5 per user.
- **Members**: Max 10 per board.
- **Memberships**: Max 20 per user.

---




## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---


---

## 🤝 Contributing

Feel free to submit issues or pull requests. For major changes, please open an issue first to discuss.

---

**Mini Trello**: Organize, collaborate, and get things done with style! 🚀
