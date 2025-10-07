from flask import Blueprint, request, jsonify
from flask_login import login_required
from ..extensions import db
from ..models import CaseStudy, ForumPost

community_bp = Blueprint("community", __name__)


@community_bp.get("/case-studies")
@login_required
def list_case_studies():
    q = CaseStudy.query
    location = request.args.get("location")
    if location:
        q = q.filter(CaseStudy.location.ilike(f"%{location}%"))
    items = q.all()
    return jsonify([
        {"case_id": c.case_id, "title": c.title, "location": c.location, "success_metrics": c.success_metrics}
        for c in items
    ])


@community_bp.get("/forum")
@login_required
def list_forum():
    category = request.args.get("category")
    q = ForumPost.query
    if category:
        q = q.filter(ForumPost.category == category)
    posts = q.order_by(ForumPost.timestamp.desc()).all()
    return jsonify([
        {"post_id": p.post_id, "title": p.title, "content": p.content, "category": p.category, "timestamp": p.timestamp.isoformat()}
        for p in posts
    ])


@community_bp.post("/forum")
@login_required
def create_post():
    data = request.get_json(force=True)
    title = data.get("title")
    content = data.get("content")
    category = data.get("category")
    if not title or not content:
        return jsonify({"error": "Title and content required"}), 400
    post = ForumPost(title=title, content=content, category=category, user_id=None)
    db.session.add(post)
    db.session.commit()
    return jsonify({"post_id": post.post_id}), 201
