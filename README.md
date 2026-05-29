# Nepali Astrology Booking Platform

## Setup

1. Create a Supabase project and run [migrations/001_init.sql](migrations/001_init.sql) in the SQL editor.
2. Create a storage bucket named `media` with public access.
3. Create your first admin user in Supabase Auth (email/password).
4. Copy `.env.example` to `.env` and fill values.
5. Install dependencies and run the app.

## Run locally

- Windows PowerShell:
  - Create a virtual environment, install requirements, then run `python app.py` or `python main.py`.

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
| SITE_URL | yes | https://www.nepaliastrology.com |
| FLASK_ENV | yes | production |

### 2. Deploy

Connect the GitHub repo to Vercel. Deployment entrypoint is `app.py`; the Flask package lives in `application/` (so names do not collide).

### 3. Custom domain

In Vercel → Project → Domains, add `nepaliastrology.com` and `www.nepaliastrology.com`.
Add the CNAME and A records shown by Vercel to your DNS provider.

### 4. First run after deploy

Visit `/admin/login` and log in with the admin account created in the Supabase Auth dashboard.

---

## Post-deployment SEO steps

After deployment, complete the following to boost search engine visibility:

### 1. Create Google Business Profile

Go to [business.google.com](https://business.google.com):
- Business name: **nepali astrology**
- Category: **astrologer** or **astrology service**
- Website: `https://www.nepaliastrology.com`
- Phone: your contact phone number
- Address: Kathmandu, Nepal
- Add photos, services list, booking link
- Encourage clients to leave reviews (crucial ranking signal)

### 2. Submit to Google Search Console

1. Visit [search.google.com/search-console](https://search.google.com/search-console)
2. Add property: `https://www.nepaliastrology.com`
3. Verify ownership (choose preferred method)
4. Submit sitemap: `https://www.nepaliastrology.com/sitemap.xml`
5. Monitor crawl errors and indexation status
6. Request indexing for important pages

### 3. Submit to Bing Webmaster Tools

1. Visit [bing.com/webmasters](https://bing.com/webmasters)
2. Add site and verify ownership
3. Submit sitemap: `https://www.nepaliastrology.com/sitemap.xml`

### 4. Directory listings & backlinks

Create verified business listings on these nepali and global directories (all free):
- **Justdial Nepal** – local search engine popular in nepal
- **Yellow Pages Nepal** – business directory
- **Nepal Business Directory** – local seo
- **Yelp** – global reach, reviews
- Local Kathmandu tourism and service directories

Use consistent **NAP** (Name, Address, Phone) across all profiles for local seo strength.

### 5. Social media profiles

Create and optimize profiles on:
- **Facebook** – add website url to bio, post regularly about astrology insights
- **Instagram** – use local astrology hashtags, link to website
- **YouTube** – upload astrology videos, link in descriptions
- **LinkedIn** – business page for professional reach

Add your website URL to all bios and link back to nepaliastrology.com.

### 6. Request reviews from clients

After each booking:
- Email: include link to leave Google review
- WhatsApp: send review request template
- In-session: mention google reviews help other seekers find the right astrologer

**Google reviews are the strongest local ranking factor.** Aim for 4.5+ stars and 50+ reviews in first 6 months.

### 7. Monitor rankings and traffic

- Use [Google Search Console](https://search.google.com/search-console) to track keyword impressions, clicks, and rankings
- Install [Google Analytics 4](https://analytics.google.com) to track visitor behaviour
- Monitor Core Web Vitals for page speed (ranking factor)
- Track rankings for target keywords: "nepali astrology", "kundali reading nepal", "online astrology nepal", etc.

### 8. Content strategy

Update your blog and pages with:
- **Initial blog posts** targeting tier 2 & 3 keywords (see SEO spec):
  1. what is vedic astrology and how is it different from western astrology
  2. how to read your janam kundali — a beginner's guide
  3. rashifal 2025 — yearly predictions for all 12 signs
  4. kundali matching for marriage — what to look for
  5. vastu shastra tips for a happy and prosperous home
  6. the 12 houses in vedic astrology explained
  7. saturn mahadasha — what to expect and how to prepare
  8. numerology in the nepali tradition — your life path number
  9. rahu and ketu — the lunar nodes in your birth chart
  10. how to choose the right astrologer for your consultation

- Each post: **minimum 800 words**, primary keyword in title + first paragraph, h2 subheadings every 200–300 words, CTA link to book consultation
- Publish **1–2 posts per month** for first 3 months to build topical authority

### 9. Link building

- Reach out to local nepali blogs/websites for guest post opportunities
- Provide free readings to local influencers in exchange for feature/mention
- Sponsor local events and include website link in announcements
- Create high-quality internal links between related pages (blog → astrologer profiles, services → astrologer pages, etc.)

### 10. Structured data validation

Test all structured data:
- Visit [schema.org validator](https://validator.schema.org)
- Paste home page, blog post, astrologer profile HTML source
- Ensure LocalBusiness, Article, Person, Service, and FAQPage schemas validate with no errors

---

## SEO implementation checklist

✅ **Technical SEO**
- `base.html`: Complete meta tags, Open Graph, Twitter Card, JSON-LD LocalBusiness
- `/sitemap.xml`: Auto-generated, all public pages indexed
- `/robots.txt`: Disallows /admin/, /api/, /book/, /checkout/
- Per-page titles, descriptions, keywords across all public templates
- Image alt text with keywords, width/height attributes, loading="lazy", fetchpriority on hero
- Canonical URLs (https://www.nepaliastrology.com + request.path)
- Open Graph images (1200x630px recommended)
- Core Web Vitals performance headers (cache, CSP, X-Frame-Options)

✅ **On-page SEO**
- Heading hierarchy: one H1 per page, H2 for sections, H3 for subsections
- Tier 1 keywords in title tags (first 60 characters)
- Primary keyword in H1, secondary keywords in H2/H3
- Tier 1, 2, 3 keywords naturally woven into body content
- Keywords in first 100 words of pages
- Internal links with keyword anchor text

✅ **Structured data**
- LocalBusiness schema (home page + all pages)
- Person schema (astrologer profile pages)
- Article schema (blog posts)
- Service schema (service cards)
- FAQPage schema (home page)

✅ **Post-deployment**
- [ ] Google Business Profile created & verified
- [ ] Search Console property added & sitemap submitted
- [ ] Bing Webmaster Tools property added
- [ ] Directory listings (Justdial, Yellow Pages, Yelp, etc.)
- [ ] Social media profiles optimized with link
- [ ] Initial 10 blog posts published
- [ ] Review request process set up
- [ ] Analytics & rank tracking configured
