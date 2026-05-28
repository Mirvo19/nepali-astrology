from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from functools import wraps
from ...models.db import get_admin_client
from ...models.bookings import list_bookings, update_booking
from ...models.astrologers import list_astrologers, create_or_update_astrologer, delete_astrologer
from ...models.services import list_services, create_or_update_service, delete_service
from ...models.availability import list_availability, create_or_update_availability, delete_availability
from ...models.blocked_dates import list_blocked_dates, create_blocked_date, delete_blocked_date
from ...models.site_settings import get_site_settings, update_site_settings
from ...models.testimonials import list_testimonials, create_or_update_testimonial, delete_testimonial
from ...models.faqs import list_faqs, create_or_update_faq, delete_faq
from ...models.blog_posts import list_blog_posts, create_or_update_post, delete_post
from ...models.gallery import list_gallery, create_or_update_gallery, delete_gallery
from slugify import slugify
from datetime import datetime, timezone
import bleach
import uuid

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def login_required(view):
	@wraps(view)
	def wrapped(*args, **kwargs):
		if not session.get("admin_user"):
			return redirect(url_for("admin.login"))
		return view(*args, **kwargs)

	return wrapped


def validate_csrf():
	token = request.form.get("csrf_token")
	return token and token == session.get("csrf_token")


def upload_to_storage(file_storage):
	if not file_storage:
		return None
	client = get_admin_client()
	bucket = client.storage.from_("media")
	filename = f"{uuid.uuid4()}-{file_storage.filename}"
	bucket.upload(filename, file_storage.stream.read(), file_storage.mimetype)
	return bucket.get_public_url(filename)


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		if not validate_csrf():
			abort(400)
		email = request.form.get("email")
		password = request.form.get("password")
		client = get_admin_client()
		result = client.auth.sign_in_with_password({"email": email, "password": password})
		if result and result.user:
			session["admin_user"] = {"email": result.user.email}
			return redirect(url_for("admin.dashboard"))
		return render_template("admin/login.html", error="Invalid credentials")
	return render_template("admin/login.html")


@admin_bp.route("/logout")
def logout():
	session.pop("admin_user", None)
	return redirect(url_for("admin.login"))


@admin_bp.route("/")
@login_required
def dashboard():
	bookings = list_bookings()
	return render_template("admin/dashboard.html", bookings=bookings)


@admin_bp.route("/bookings", methods=["GET", "POST"])
@login_required
def bookings_manager():
	if request.method == "POST" and validate_csrf():
		update_booking(
			request.form.get("booking_id"),
			{
				"status": request.form.get("status"),
				"payment_status": request.form.get("payment_status"),
			},
		)
	filters = {
		"status": request.args.get("status"),
		"payment_status": request.args.get("payment_status"),
		"astrologer_id": request.args.get("astrologer_id"),
		"start_date": request.args.get("start_date"),
		"end_date": request.args.get("end_date"),
	}
	bookings = list_bookings(filters=filters)
	astrologers = list_astrologers(active_only=False)
	return render_template(
		"admin/bookings.html",
		bookings=bookings,
		astrologers=astrologers,
	)


@admin_bp.route("/astrologers", methods=["GET", "POST"])
@login_required
def astrologers_manager():
	if request.method == "POST" and validate_csrf():
		languages = [lang.strip() for lang in request.form.get("languages", "").split(",") if lang.strip()]
		payload = {
			"name": request.form.get("name"),
			"slug": request.form.get("slug") or slugify(request.form.get("name")),
			"title": request.form.get("title"),
			"bio": request.form.get("bio"),
			"languages": languages,
			"experience_years": request.form.get("experience_years") or 0,
			"is_active": bool(request.form.get("is_active")),
			"sort_order": request.form.get("sort_order") or 0,
		}
		photo_url = upload_to_storage(request.files.get("photo"))
		if photo_url:
			payload["photo_url"] = photo_url
		create_or_update_astrologer(payload)
	astrologers = list_astrologers(active_only=False)
	return render_template("admin/astrologers.html", astrologers=astrologers)


@admin_bp.route("/astrologers/delete", methods=["POST"])
@login_required
def astrologer_delete():
	if validate_csrf():
		delete_astrologer(request.form.get("astrologer_id"))
	return redirect(url_for("admin.astrologers_manager"))


@admin_bp.route("/services", methods=["GET", "POST"])
@login_required
def services_manager():
	if request.method == "POST" and validate_csrf():
		payload = {
			"astrologer_id": request.form.get("astrologer_id"),
			"name": request.form.get("name"),
			"description": request.form.get("description"),
			"duration_minutes": request.form.get("duration_minutes") or 60,
			"price_npr": request.form.get("price_npr") or 0,
			"is_active": bool(request.form.get("is_active")),
			"sort_order": request.form.get("sort_order") or 0,
		}
		create_or_update_service(payload)
	astrologers = list_astrologers(active_only=False)
	services = list_services(active_only=False)
	return render_template(
		"admin/services.html",
		services=services,
		astrologers=astrologers,
	)


@admin_bp.route("/services/delete", methods=["POST"])
@login_required
def service_delete():
	if validate_csrf():
		delete_service(request.form.get("service_id"))
	return redirect(url_for("admin.services_manager"))


@admin_bp.route("/availability", methods=["GET", "POST"])
@login_required
def availability_manager():
	astrologers = list_astrologers(active_only=False)
	selected_id = request.args.get("astrologer_id") or (astrologers[0]["id"] if astrologers else None)
	if request.method == "POST" and validate_csrf():
		action = request.form.get("action")
		if action == "availability":
			payload = {
				"astrologer_id": request.form.get("astrologer_id"),
				"day_of_week": int(request.form.get("day_of_week")),
				"start_time": request.form.get("start_time"),
				"end_time": request.form.get("end_time"),
				"is_active": True,
			}
			create_or_update_availability(payload)
		if action == "blocked":
			payload = {
				"astrologer_id": request.form.get("astrologer_id"),
				"blocked_date": request.form.get("blocked_date"),
				"reason": request.form.get("reason"),
			}
			create_blocked_date(payload)
	availability = list_availability(selected_id) if selected_id else []
	blocked = list_blocked_dates(selected_id) if selected_id else []
	return render_template(
		"admin/availability.html",
		astrologers=astrologers,
		availability=availability,
		blocked_dates=blocked,
		selected_id=selected_id,
	)


@admin_bp.route("/availability/delete", methods=["POST"])
@login_required
def availability_delete():
	if validate_csrf():
		delete_availability(request.form.get("availability_id"))
	return redirect(url_for("admin.availability_manager"))


@admin_bp.route("/blocked/delete", methods=["POST"])
@login_required
def blocked_delete():
	if validate_csrf():
		delete_blocked_date(request.form.get("blocked_id"))
	return redirect(url_for("admin.availability_manager"))


@admin_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings_manager():
	if request.method == "POST" and validate_csrf():
		payload = {key: request.form.get(key) for key in request.form.keys() if key != "csrf_token"}
		for field in ["about_image_url", "og_image_url"]:
			if request.files.get(field):
				uploaded = upload_to_storage(request.files.get(field))
				if uploaded:
					payload[field] = uploaded
		update_site_settings(payload)
	site_settings = get_site_settings()
	return render_template("admin/settings.html", site_settings=site_settings)


@admin_bp.route("/testimonials", methods=["GET", "POST"])
@login_required
def testimonials_manager():
	if request.method == "POST" and validate_csrf():
		payload = {
			"client_name": request.form.get("client_name"),
			"client_location": request.form.get("client_location"),
			"rating": int(request.form.get("rating") or 5),
			"content": request.form.get("content"),
			"is_visible": bool(request.form.get("is_visible")),
		}
		avatar_url = upload_to_storage(request.files.get("avatar"))
		if avatar_url:
			payload["avatar_url"] = avatar_url
		create_or_update_testimonial(payload)
	testimonials = list_testimonials(visible_only=False)
	return render_template("admin/testimonials.html", testimonials=testimonials)


@admin_bp.route("/testimonials/delete", methods=["POST"])
@login_required
def testimonials_delete():
	if validate_csrf():
		delete_testimonial(request.form.get("testimonial_id"))
	return redirect(url_for("admin.testimonials_manager"))


@admin_bp.route("/faqs", methods=["GET", "POST"])
@login_required
def faqs_manager():
	if request.method == "POST" and validate_csrf():
		payload = {
			"question": request.form.get("question"),
			"answer": request.form.get("answer"),
			"sort_order": request.form.get("sort_order") or 0,
			"is_visible": bool(request.form.get("is_visible")),
		}
		create_or_update_faq(payload)
	faqs = list_faqs(visible_only=False)
	return render_template("admin/faqs.html", faqs=faqs)


@admin_bp.route("/faqs/delete", methods=["POST"])
@login_required
def faqs_delete():
	if validate_csrf():
		delete_faq(request.form.get("faq_id"))
	return redirect(url_for("admin.faqs_manager"))


@admin_bp.route("/blog", methods=["GET", "POST"])
@login_required
def blog_manager():
	if request.method == "POST" and validate_csrf():
		allowed_tags = [
			"p",
			"br",
			"strong",
			"em",
			"ul",
			"ol",
			"li",
			"h1",
			"h2",
			"h3",
			"h4",
			"blockquote",
			"a",
			"img",
		]
		clean_content = bleach.clean(
			request.form.get("content"),
			tags=allowed_tags,
			attributes={"a": ["href", "title"], "img": ["src", "alt"]},
		)
		is_published = bool(request.form.get("is_published"))
		payload = {
			"title": request.form.get("title"),
			"slug": request.form.get("slug") or slugify(request.form.get("title")),
			"excerpt": request.form.get("excerpt"),
			"content": clean_content,
			"meta_title": request.form.get("meta_title"),
			"meta_description": request.form.get("meta_description"),
			"is_published": is_published,
			"published_at": datetime.now(tz=timezone.utc).isoformat() if is_published else None,
		}
		cover_url = upload_to_storage(request.files.get("cover_image"))
		if cover_url:
			payload["cover_image_url"] = cover_url
		create_or_update_post(payload)
	posts = list_blog_posts(published_only=False)
	return render_template("admin/blog.html", posts=posts)


@admin_bp.route("/blog/delete", methods=["POST"])
@login_required
def blog_delete():
	if validate_csrf():
		delete_post(request.form.get("post_id"))
	return redirect(url_for("admin.blog_manager"))


@admin_bp.route("/gallery", methods=["GET", "POST"])
@login_required
def gallery_manager():
	if request.method == "POST" and validate_csrf():
		payload = {
			"caption": request.form.get("caption"),
			"sort_order": request.form.get("sort_order") or 0,
			"is_visible": bool(request.form.get("is_visible")),
		}
		image_url = upload_to_storage(request.files.get("image"))
		if image_url:
			payload["image_url"] = image_url
		create_or_update_gallery(payload)
	gallery = list_gallery(visible_only=False)
	return render_template("admin/gallery.html", gallery=gallery)


@admin_bp.route("/gallery/delete", methods=["POST"])
@login_required
def gallery_delete():
	if validate_csrf():
		delete_gallery(request.form.get("gallery_id"))
	return redirect(url_for("admin.gallery_manager"))
