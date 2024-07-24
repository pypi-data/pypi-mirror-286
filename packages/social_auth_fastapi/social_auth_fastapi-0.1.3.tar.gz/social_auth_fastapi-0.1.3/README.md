<h1 align="center"> FastAPI FUnd Services</h1>
<p align="center">
  <a href="">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  </a>
  <a href="https://fastapi.tiangolo.com">
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
  </a>
  <a href="https://docs.pydantic.dev/2.4/">
    <img src="https://img.shields.io/badge/Pydantic-E92063?logo=pydantic&logoColor=fff&style=for-the-badge" alt="Pydantic">
  </a>
  <a href="https://www.postgresql.org">
    <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  </a>

  <a href="https://docs.docker.com/compose/">
    <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff&style=for-the-badge" alt="Docker">
  </a>
  <a href="https://casbin.org/">
    <img alt="Static Badge" src="https://img.shields.io/badge/Casbin-316192?style=for-the-badge&logo=AdGuard&logoColor=%23E60505&color=%2300BCB4">
  </a>
</p>

## 0. Technology Stack and Features

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
    - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) for the Python SQL database interactions (ORM).
    - 🔍 [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
    - 💾 [PostgreSQL](https://www.postgresql.org) as the SQL database.
- 🐋 [Docker Compose](https://www.docker.com) for development and production.
- 🔒 Secure password hashing by default.
- 🔑 JWT token authentication.
- 📫 Email based password recovery.

- 🎨 [PDM](https://pdm-project.org/latest/) is a modern Python package and dependency manager supporting the latest PEP standards.
- 📞 [Traefik](https://traefik.io) as a reverse proxy / load balancer.
- 🚢 Deployment instructions using Docker Compose, including how to set up a frontend Traefik proxy to handle automatic HTTPS certificates.
- 🏭 CI (continuous integration) and CD (continuous deployment) based on GitHub Actions.

### Development process
1. Define the database model (`models`) and remember to perform database migration for each change
2. Define the data validation model (`schemas`)
3. Define routes (`router`) and views (`api`)
4. Define the business logic (`services`)
5. Write database operations (`crud`)
6. Define common (`common`)

## 1. Prerequisites

### 1.0 Start
Clone repository

Clone repository
```sh
git clone https://github.com/congpc130599/social-auth
```

### 1.1 Environment Variables (.env)
Then create a `.env` file in the `project` directory.

You can then update configs in the .env files to customize your configurations.
```shell
touch .env
cp .env.example .env
```

### 1.2 Install using pdm

```sh
curl -sSL https://pdm-project.org/install-pdm.py | python3 -
pdm python install 3.11.7
pdm install
```

### Scripts

- `pdm dev`: Run server

- `pdm format`: Perform ruff format check

- `pdm lint`: Perform pre-commit formatting

- `pdm safety`: Execute pdm export dependency package

Ensuring it ran without any problem.

### 1.5 Internationalization

Get pybabel tools directly within your FastAPI project without hassle.
- Init messages
    ```sh
    pdm locale
    ```

- Extract messages with following command
    ```sh
    pdm locale-update
    ```
- Go to `./locale/en_US/.po` and add your translations.

- Compile all locale directories. python3 babel.py compile
    ```sh
    pdm locale-compile
    ```


> \[!NOTE\]
>`ENVIRONMENT` can be one of `dev` and `pro`, defaults to dev, and changes the behavior of api `docs` endpoints:
>
>- **dev:** `/docs`, `/redoc` and `/openapi.json` available
>- **pro:** `/docs`, `/redoc` and `/openapi.json` not available
