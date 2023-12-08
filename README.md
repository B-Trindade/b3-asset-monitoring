# b3-asset-monitoring

`b3-asset-monitor` is a Django/Python application that provides a financial advisory system through email notifications. Currently `B3-Notifier` is only available locally - this may change in the future. `B3-Notifier` allows users to register and set custom [Bovespa B3](https://www.b3.com.br/) ticker notifications for buying and selling boundries.

## About

This project was developed with the following technologies:

- Django, Django REST Framework and DRF Spectacular
- React.js, React Router and Axios
- Celery, Redis (message broker)
- PostgreSQL
- Docker

The REST API endpoints are documented at the `http://localhost:8000/api/docs/` endpoint with automatically generated Swagger UI page by DRF Spectacular. Endpoints can be tested directly and individually through this page. Read more about [Swagger UI](https://swagger.io/tools/swagger-ui/) and [DRF Spectacular](https://drf-spectacular.readthedocs.io/en/latest/).

The `B3-Notifier` employs Celery workers as a solution to computation intensive and scheduled tasks such as fetching ticker data from YahooQuery and sending emails to users. Redis acts as a message broker between the Django backend and Celery while the database uses PostgreSQL.

---

## Setup

To setup and run services locally you must be able to run `docker-compose` commands. I recommend using the [Docker Desktop](https://docs.docker.com/desktop/) application.
It is also reccomended to use Google Chrome as your browser or other Chromium based browser.

### Install Docker Desktop

To install Docker Desktop make sure you fulfill the [prerequisites](https://docs.docker.com/desktop/install/ubuntu/#prerequisites). Install the package with apt:

```bash
sudo apt-get update
sudo apt-get install ./docker-desktop-<version>-<arch>.deb
```

### Running for the first time

To run the application for the first time you must follow some simple steps.

### Configure SMTP

Provide an `email` and `password` to be used by the app. This address will send the notifications to users. By default it uses gmail, however, this can be customized at the end of your `settings.py` file under the SMTP settings section.

```python
# /backend/app/app/settings.py

...
# SMTP Settings
EMAIL_HOST_USER = "example@gmail.com"  # your app email
EMAIL_HOST_PASSWORD = "abcdefghijklmnop"  # your gmail app key
```

### Run Docker Desktop

For this you can search Docker Desktop on the Applications menu and open it. This launches the Docker menu icon and opens the Docker Dashboard, reporting the status of Docker Desktop.

Alternatively, open a terminal and run:

```bash
systemctl --user start docker-desktop
```

### Build

After Docker Desktop is executing, you must build the images by running:

```bash
docker-compose build
```

### Run services

Now, to start the services simply run:

```bash
docker-compose up
```

The application will be available to the user at `http://localhost:3000/` and the Django admin page will be available at the `http://localhost:8000/admin/` endpoint. To use the admin page you must create a super user through the CLI command and set your admin credentials:

```bash
docker-compose run --rm backendapp sh -c "python manage.py createsuperuser"
```

---

## Functionalities and usage

Upcoming...
