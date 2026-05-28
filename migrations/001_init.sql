-- Enable extensions
create extension if not exists "pgcrypto";

-- Tables
create table site_settings (
  id uuid primary key default gen_random_uuid(),
  site_name text,
  tagline text,
  hero_heading text,
  hero_subheading text,
  hero_cta_text text,
  about_text text,
  about_image_url text,
  contact_email text,
  contact_phone text,
  contact_address text,
  whatsapp_number text,
  facebook_url text,
  instagram_url text,
  youtube_url text,
  meta_title text,
  meta_description text,
  og_image_url text,
  footer_text text,
  updated_at timestamptz default now()
);

create table testimonials (
  id uuid primary key default gen_random_uuid(),
  client_name text not null,
  client_location text,
  rating int check (rating between 1 and 5),
  content text not null,
  avatar_url text,
  is_visible boolean default true,
  created_at timestamptz default now()
);

create table faqs (
  id uuid primary key default gen_random_uuid(),
  question text not null,
  answer text not null,
  sort_order int default 0,
  is_visible boolean default true
);

create table blog_posts (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  slug text unique not null,
  excerpt text,
  content text,
  cover_image_url text,
  meta_title text,
  meta_description text,
  is_published boolean default false,
  published_at timestamptz,
  created_at timestamptz default now()
);

create table astrologers (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  slug text unique not null,
  title text,
  bio text,
  photo_url text,
  languages text[],
  experience_years int,
  is_active boolean default true,
  sort_order int default 0,
  created_at timestamptz default now()
);

create table services (
  id uuid primary key default gen_random_uuid(),
  astrologer_id uuid references astrologers(id) on delete cascade,
  name text not null,
  description text,
  duration_minutes int not null default 60,
  price_npr numeric(10,2) not null,
  is_active boolean default true,
  sort_order int default 0
);

create table availability (
  id uuid primary key default gen_random_uuid(),
  astrologer_id uuid references astrologers(id) on delete cascade,
  day_of_week int check (day_of_week between 0 and 6),
  start_time time not null,
  end_time time not null,
  is_active boolean default true
);

create table blocked_dates (
  id uuid primary key default gen_random_uuid(),
  astrologer_id uuid references astrologers(id) on delete cascade,
  blocked_date date not null,
  reason text
);

create table bookings (
  id uuid primary key default gen_random_uuid(),
  booking_ref text unique not null,
  astrologer_id uuid references astrologers(id),
  service_id uuid references services(id),
  client_name text not null,
  client_email text not null,
  client_phone text,
  client_birth_date date,
  client_birth_time text,
  client_birth_place text,
  appointment_date date not null,
  appointment_time time not null,
  notes text,
  status text default 'pending' check (status in ('pending','confirmed','cancelled','completed')),
  payment_status text default 'unpaid' check (payment_status in ('unpaid','paid','refunded')),
  stripe_session_id text,
  amount_npr numeric(10,2),
  created_at timestamptz default now()
);

create table gallery (
  id uuid primary key default gen_random_uuid(),
  image_url text not null,
  caption text,
  sort_order int default 0,
  is_visible boolean default true
);

-- Enable RLS
alter table site_settings enable row level security;
alter table testimonials enable row level security;
alter table faqs enable row level security;
alter table blog_posts enable row level security;
alter table astrologers enable row level security;
alter table services enable row level security;
alter table availability enable row level security;
alter table blocked_dates enable row level security;
alter table bookings enable row level security;
alter table gallery enable row level security;

-- Public read policies
create policy "public_read_site_settings" on site_settings for select using (true);
create policy "public_read_testimonials" on testimonials for select using (is_visible = true);
create policy "public_read_faqs" on faqs for select using (is_visible = true);
create policy "public_read_blog_posts" on blog_posts for select using (is_published = true);
create policy "public_read_astrologers" on astrologers for select using (is_active = true);
create policy "public_read_services" on services for select using (is_active = true);
create policy "public_read_availability" on availability for select using (is_active = true);
create policy "public_read_gallery" on gallery for select using (is_visible = true);

-- Admin policies (service role)
create policy "admin_all_site_settings" on site_settings for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
create policy "admin_all_testimonials" on testimonials for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
create policy "admin_all_faqs" on faqs for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
create policy "admin_all_blog_posts" on blog_posts for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
create policy "admin_all_astrologers" on astrologers for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
create policy "admin_all_services" on services for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
create policy "admin_all_availability" on availability for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
create policy "admin_all_blocked_dates" on blocked_dates for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
create policy "admin_all_bookings" on bookings for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
create policy "admin_all_gallery" on gallery for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
