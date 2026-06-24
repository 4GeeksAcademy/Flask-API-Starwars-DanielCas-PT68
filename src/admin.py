from flask_admin.contrib.sqla import ModelView
from models import db, User, Planet, People, Favorite


def setup_admin(app):
    app.config["FLASK_ADMIN_SWATCH"] = "cerulean"
    app.config["SECRET_KEY"] = "starwars-secret-key"

    from flask_admin import Admin
    admin = Admin(app, name="StarWars API", template_mode="bootstrap3")

    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Planet, db.session))
    admin.add_view(ModelView(People, db.session))
    admin.add_view(ModelView(Favorite, db.session))