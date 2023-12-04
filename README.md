# b3-asset-monitoring

=====================

`b3-asset-monitor` is a Django/Python application that provides a financial advisory system through email notifications. Currently `B3-Notifier` is only available locally - this may change in the future. `B3-Notifier` allows users to register and set custom [Bovespa B3](https://www.b3.com.br/) ticker notifications for buying and selling boundries.

---

## Setup

To setup and run services locally you must be able to run `docker-compose` commands. I recommend using the [Docker Desktop](https://docs.docker.com/desktop/) application.

### Install Docker Desktop

To install Docker Desktop make sure you fulfill the [prerequisites](https://docs.docker.com/desktop/install/ubuntu/#prerequisites). Install the package with apt:

```bash
sudo apt-get update
sudo apt-get install ./docker-desktop-<version>-<arch>.deb
```

### Running for the first time

To run the application for the first time you must follow some simple steps.

### Run Docker Desktop.

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
