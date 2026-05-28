# Nepali Astrology Booking Platform

## Setup

1. Create a Supabase project and run [migrations/001_init.sql](migrations/001_init.sql) in the SQL editor.
2. Create a storage bucket named `media` with public access.
3. Create your first admin user in Supabase Auth (email/password).
4. Copy `.env.example` to `.env` and fill values.
5. Install dependencies and run the app.

## Run locally

- Windows PowerShell:
  - Create a virtual environment, install requirements, then run `python main.py`.

## Admin login

- Visit `/admin/login` and sign in with Supabase Auth credentials.

## Notes

- Public pages are CMS-driven from `site_settings` and other tables.
- Stripe routes are placeholders; integrate with your Stripe keys later.
- Supabase service role key is required on the server for admin operations.

## Vercel deployment

### 1. Set environment variables in Vercel dashboard

Go to project → Settings → Environment variables and add:

| Variable | Required | Notes |
|---|---|---|
| FLASK_SECRET_KEY | yes | min 32 random chars |
| SUPABASE_URL | yes | from Supabase project settings |
| SUPABASE_KEY | yes | service role key |
| SUPABASE_ANON_KEY | yes | anon key |
| STRIPE_SECRET_KEY | no | add when ready |
| STRIPE_WEBHOOK_SECRET | no | add when ready |
| SMTP_HOST | no | email sending |
| SMTP_PORT | no | default 587 |
| SMTP_USER | no | |
| SMTP_PASS | no | |
| SITE_URL | yes | https://nepaliastrology.com |
| FLASK_ENV | yes | production |

### 2. Deploy

Connect the GitHub repo to Vercel. Deployment uses `wsgi.py` (not `app.py`, which would shadow the `app/` package).

### 3. Custom domain

In Vercel → Project → Domains, add `nepaliastrology.com` and `www.nepaliastrology.com`.
Add the CNAME and A records shown by Vercel to your DNS provider.

### 4. First run after deploy

Visit `/admin/login` and log in with the admin account created in the Supabase Auth dashboard.
