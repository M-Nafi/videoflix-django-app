# Videoflix - Django REST API Backend

Ein vollständiges Backend für eine Video-Streaming-Plattform mit HLS (HTTP Live Streaming) Unterstützung und Benutzerauthentifizierung.

## 🚀 Features

### Core Funktionalitäten

-   **Video Upload & Processing**: Automatische Konvertierung in mehrere Auflösungen (180p, 360p, 720p, 1080p)
-   **HLS Streaming**: HTTP Live Streaming mit adaptiver Bitrate für optimale Wiedergabe
-   **Benutzerauthentifizierung**: JWT-basierte Authentifizierung mit HTTP-only Cookies
-   **Genre-basierte Kategorisierung**: Videos nach Genres organisiert

### API Endpoints

#### Videos

-   `GET /api/video/` - Liste aller Videos (Authentifizierung erforderlich)
-   `POST /api/video/upload/` - Video Upload (öffentlich für Admin)
-   `GET /api/video/<movie_id>/<resolution>/index.m3u8` - HLS Master Playlist
-   `GET /api/video/<movie_id>/<resolution>/<segment>/` - HLS Video Segments

#### Authentifizierung

-   `POST /api/login/` - Benutzer Login
-   `POST /api/logout/` - Benutzer Logout
-   `POST /api/login/refresh/` - Token Refresh
-   `POST /api/users/` - Benutzerregistrierung

## 🛠 Tech Stack

### Backend

-   **Django 5.1.7** - Web Framework
-   **Django REST Framework 3.16.0** - API Framework
-   **PostgreSQL** - Hauptdatenbank
-   **Redis** - Caching & Background Jobs
-   **Django-RQ** - Background Task Queue
-   **FFmpeg** - Video Processing
-   **Docker** - Containerisierung

### Authentifizierung & Security

-   **JWT (djangorestframework_simplejwt)** - Token-basierte Authentifizierung
-   **Djoser** - Benutzerregistrierung & E-Mail-Aktivierung
-   **CORS Headers** - Cross-Origin Resource Sharing

### Video Processing

-   **MoviePy** - Video Manipulation
-   **Pillow** - Image Processing
-   **FFmpeg** - Video Konvertierung & HLS Segmentierung

## 📦 Installation

### Voraussetzungen

-   Docker & Docker Compose
-   Python 3.8+
-   FFmpeg

### Setup

1. **Repository klonen**

    ```bash
    git clone <repository-url>
    cd videoflix
    ```

2. **Environment Variablen**

    ```bash
    cp .env.example .env
    # .env Datei entsprechend anpassen
    ```

3. **Docker Services starten**

    ```bash
    docker-compose up -d
    ```

4. **Datenbank migrieren**

    ```bash
    docker-compose exec web python manage.py migrate
    ```

5. **Superuser erstellen**
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

## 🏗 Projektstruktur

```
videoflix/
├── core/                          # Django Projekt Settings
│   ├── settings.py               # Hauptkonfiguration
│   ├── urls.py                   # URL Routing
│   └── wsgi.py                   # WSGI Application
├── user_auth_app/                # Benutzerauthentifizierung
│   ├── models.py                 # Custom User Model
│   ├── api/
│   │   ├── views.py             # Auth Views (Login, Logout, etc.)
│   │   ├── serializers.py       # User Serializers
│   │   └── authentication.py   # JWT Cookie Authentication
│   └── templates/               # E-Mail Templates
├── videoflix/                    # Video App
│   ├── models.py                # Video Model
│   ├── api/
│   │   ├── views.py            # Video API Views
│   │   ├── serializers.py      # Video Serializers
│   │   ├── functions.py        # Utility Functions
│   │   ├── tasks.py            # Background Tasks
│   │   ├── utils.py            # Helper Classes
│   │   └── urls.py             # Video URL Patterns
│   └── tests.py                # Unit Tests
├── templates/                    # Django Templates
├── static/                       # Static Files
├── media/                        # Uploaded Media
│   ├── videos/
│   │   ├── original/           # Original Videos
│   │   ├── 180p/, 360p/, etc.  # Konvertierte Videos
│   │   ├── hls/                # HLS Streams
│   │   └── thumbnails/         # Video Thumbnails
├── requirements.txt              # Python Dependencies
├── docker-compose.yml           # Docker Configuration
└── README.md                    # Dokumentation
```

## 🔧 Konfiguration

### Environment Variablen (.env)

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=videoflix_db
DB_USER=videoflix_user
DB_PASSWORD=supersecret
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# Email (für Benutzerregistrierung)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True

# Frontend URLs
FRONTEND_LOGIN_URL=http://localhost:4200/login
```

## 🎥 Video Processing Pipeline

1. **Upload**: Video wird über API hochgeladen
2. **Background Processing**:
    - Konvertierung in multiple Auflösungen (180p-1080p)
    - HLS Segmentierung für adaptive Streaming
    - Thumbnail-Generierung
3. **Storage**: Alle Dateien werden im Media-Verzeichnis gespeichert
4. **Streaming**: HLS-kompatible Wiedergabe über API

### HLS (HTTP Live Streaming)

-   **Adaptive Bitrate**: Automatische Qualitätsanpassung
-   **Segmentierung**: 10-Sekunden-Segmente für optimales Buffering
-   **Cross-Platform**: Unterstützung für alle modernen Browser und Geräte

## 🧪 Testing

### Unit Tests ausführen

```bash
docker-compose exec web python manage.py test
```

### Test Coverage

```bash
docker-compose exec web coverage run --source='.' manage.py test
docker-compose exec web coverage report
```

### Testbereiche

-   **API Endpoints**: Vollständige Abdeckung aller Video- und Auth-Endpoints
-   **Video Processing**: Tests für Konvertierung und HLS-Generierung
-   **User Authentication**: JWT-Authentication und Permissions
-   **HLS Streaming**: Manifest und Segment Delivery

## 🚀 Deployment

### Production Setup

1. **Environment**: DEBUG=False setzen
2. **Static Files**: `collectstatic` ausführen
3. **Database**: PostgreSQL für Production
4. **Web Server**: Gunicorn + Nginx
5. **SSL**: HTTPS für sichere Cookie-Übertragung

### Docker Production

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 📋 API Dokumentation

### Video List Response

```json
[
	{
		"id": 1,
		"created_at": "2023-01-01T12:00:00Z",
		"title": "Movie Title",
		"description": "Movie Description",
		"thumbnail_url": "http://example.com/media/thumbnail/image.jpg",
		"category": "Drama"
	}
]
```

### HLS Streaming

-   **Manifest**: `/api/video/{movie_id}/{resolution}/index.m3u8`
-   **Segments**: `/api/video/{movie_id}/{resolution}/{segment}/`

## 🔒 Sicherheit

-   **JWT HTTP-Only Cookies**: Sichere Token-Speicherung
-   **CORS Configuration**: Kontrollierte Cross-Origin Requests
-   **Authentication Required**: Video-List-Endpoint erfordert Authentifizierung
-   **Input Validation**: Umfassende Validierung aller API-Inputs

## 🤝 Contributing

1. Fork das Repository
2. Feature Branch erstellen (`git checkout -b feature/AmazingFeature`)
3. Changes committen (`git commit -m 'Add some AmazingFeature'`)
4. Branch pushen (`git push origin feature/AmazingFeature`)
5. Pull Request erstellen

## 📝 License

Dieses Projekt ist unter der MIT License lizenziert - siehe die [LICENSE](LICENSE) Datei für Details.

## 🙋‍♂️ Support

Bei Fragen oder Problemen:

1. Issues im GitHub Repository erstellen
2. Dokumentation und API-Spezifikation prüfen
3. Logs prüfen: `docker-compose logs web`

---

**Videoflix Backend** - Entwickelt mit ❤️ und Django REST Framework
