# Async Web Crawler for Website Title and Favicon

This project is a fully asynchronous web server built with FastAPI and HTTPX. Its primary functionality is to retrieve the title and favicon of a given website URL.

## Features
- **Async Architecture**: Fully asynchronous web server using FastAPI.
- **HTTP Requests**: Handled using HTTPX.
- **Caching**: Implemented using Redis to cache the results for a limited time, avoiding duplicate requests.
- **Favicon**: The favicon is fetched, saved, and returned as a file URL.
- **Design Pattern**: Follows the MVC (Model-View-Controller) design pattern.
- **Database**: PostgreSQL used as the database.
- **Docker**: Docker used to manage the application, Redis, and PostgreSQL.

## How It Works
1. **Request**: The server accepts a website URL as input.
2. **Title**: It retrieves and returns the title of the website.
3. **Favicon**: The server fetches and saves the website's favicon, returning a file URL.
4. **Caching**: The URL and its corresponding data are cached in Redis for a limited time to prevent redundant requests.
5. **Docker**: The server runs in a Docker container along with Redis and PostgreSQL.

## Getting Started

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject

```bash
docker-compose up -d
```

## Technologies Used
- **Python**: Core programming language
- **FastAPI**: Web framework
- **Pydantic**: Json Serializer
- **SQLAlchemy**: ORM
- **HTTPX**: Asynchronous HTTP requests
- **Redis**: Caching layer
- **PostgreSQL**: Database
- **Docker**: Containerization
