# Telegram Social Platform (Casino / Sport / Gambling)

## Deployment

1. Copy environment file:

```bash
cp .env.example .env
```

2. Update `.env` with Telegram bot token and WebApp secret.

3. Build and run:

```bash
docker compose up -d --build
```

Services:
- Nginx: http://localhost
- Backend API: http://localhost/api
- Bot: running in container

## Notes
- Media files are stored in a local Docker volume (`media_data`).
- ML service stores hash data in `ml_data`.
- Admin API routes are under `/api/admin`.

## Admin Seed

On first Telegram auth, set the admin role directly in the database by updating the user role to `ADMIN`.

Example:

```sql
UPDATE users SET role = 'ADMIN' WHERE telegram_id = <your_id>;
```
