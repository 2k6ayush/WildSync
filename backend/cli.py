from flask import current_app
from .extensions import db
from .models import User, CaseStudy, ForumPost, Forest, ForestData


def register_cli(app):
    @app.cli.command("seed")
    def seed_command():
        """Seed the database with initial sample data."""
        with app.app_context():
            seed()
            print("Seed completed.")


def seed():
    # Users
    admin_email = "admin@wildsync.local"
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(name="Admin", email=admin_email, department="HQ", role="admin")
        admin.set_password("ChangeMe123!")
        db.session.add(admin)
        db.session.flush()

    # Forest and data
    forest = Forest.query.filter_by(user_id=admin.user_id, location="Sample Forest").first()
    if not forest:
        forest = Forest(user_id=admin.user_id, location="Sample Forest", area=1234.5, coordinates="0,0")
        db.session.add(forest)
        db.session.flush()

    fdata = ForestData.query.filter_by(forest_id=forest.forest_id).first()
    if not fdata:
        fdata = ForestData(
            forest_id=forest.forest_id,
            tree_count=750,
            soil_data={"health": 0.6, "ph": 6.5},
            animal_data={"activity": 0.55, "species_richness": 12},
            calamity_history={"fires": 1, "floods": 0},
        )
        db.session.add(fdata)

    # Case studies
    if CaseStudy.query.count() == 0:
        db.session.add_all(
            [
                CaseStudy(
                    title="Erosion Control in Riverine Forest",
                    description="Deployed bioengineering to stabilize banks and increased canopy cover.",
                    location="Assam, India",
                    success_metrics={"canopy_increase": 0.12, "erosion_reduction": 0.4},
                ),
                CaseStudy(
                    title="Habitat Restoration for Hornbill",
                    description="Planted native figs and protected nesting sites.",
                    location="Arunachal Pradesh, India",
                    success_metrics={"nesting_sites": 25, "population_change": "+8%"},
                ),
            ]
        )

    # Forum
    if ForumPost.query.count() == 0:
        db.session.add_all(
            [
                ForumPost(user_id=admin.user_id, title="Soil health monitoring kits", content="Recommendations?", category="Resources"),
                ForumPost(user_id=admin.user_id, title="Native species for erosion control", content="Share your list.", category="Best Practices"),
            ]
        )

    db.session.commit()