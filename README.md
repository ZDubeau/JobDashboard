# job-dashboard

## Requirements

- "python3" + "pipenv" + "pyenv"
- ["docker"](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
- ["docker-compose"](https://docs.docker.com/compose/install/)

## PostgreSQL

Using "docker-compose", you can manage a local PostgreSQL:

1. Run: "docker-compose up -d"
2. Check: "docker-compose ps"
3. Watch the logs: "docker-compose logs"
4. Run the database shell:
5. Stop: "docker-compose down"
6. Remove data: "rm -rf ./data"


## PGAdmin

This should already be started with "docker-compose up -d":

1. Open a browser to [http://localhost:8080](http://localhost:8080)
2. Login with credentials: "pgadmin" / "pgadmin"
3. Add a PostgreSQL server with the following details:
    - Name: "postgres"
    - Host: "postgres"
    - Port: "5432"
    - Username: "job"
    - Password: "dashboard"

