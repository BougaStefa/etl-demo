# Take-Home Project: ETL Pipeline

A full-stack ETL app that fetches and displayes SpaceX launch data. Built with FastAPI, React, and PostgreSQL.

## Tech Stack
- **Backend**: FastAPI, PostgreSQL, Sqlalchemy
- **Frontend**: React, TypeScript, Tailwind CSS, Tanstack Query
- **ETL**: Background tasks with retry logic
- **Deployment**: Docker, Docker Compose

## Running Locally

### Prerequisites
- Docker and Docker Compose

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/BougaStefa/etl-demo.git
   cd etl-demo
   ```

2. Set up environment variables:
   ```bash
   # Backend (.env)
   DATABASE_URL= dbLink
   SECRET_KEY= secretKey

   # Frontend (.env)
   VITE_API_URL=http://localhost:8000
   ```

3. Start the services:
   ```bash
   docker-compose up --build
        or
   docker compose up --build
   ```

4. Access:
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs

### Demo Access

Secrets are included in the MS Form I filled out.

## Future Improvements
- Filter and sort options for launches
- Profile page for users
- Pagination for launch data
