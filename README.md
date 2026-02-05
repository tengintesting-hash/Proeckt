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

## HTTPS (Required for Telegram WebApp)

1. Ensure your domain points to the VDS IP (A record).

2. Start the stack:

```bash
docker compose up -d --build
```

3. Issue a certificate (replace `example.com`):

```bash
docker compose run --rm certbot certonly \
  --webroot -w /var/www/certbot \
  -d example.com \
  --email you@example.com --agree-tos --no-eff-email
```

4. Link certs for Nginx:

```bash
mkdir -p ./nginx/certs
ln -sf /var/lib/docker/volumes/bot_certbot_certs/_data/live/example.com/fullchain.pem ./nginx/certs/fullchain.pem
ln -sf /var/lib/docker/volumes/bot_certbot_certs/_data/live/example.com/privkey.pem ./nginx/certs/privkey.pem
```

5. Restart Nginx:

```bash
docker compose restart nginx
```

## Notes
- Media files are stored in a local Docker volume (`media_data`).
- ML service stores hash data in `ml_data`.
- Admin API routes are under `/api/admin`.

## Admin Seed

Set `ADMIN_TELEGRAM_ID` in `.env` to grant admin role on startup.
