# -----------------------------------------------------------------------
# app.py
# Author: Joshua Lau '26

# Multi-Page React Application with Flask Backend

# This application serves a React frontend built with Vite through a Flask backend,
# supporting multiple entry points and both development and production environments.
# The app implements a landing page and protected route with CAS authentication.
# -----------------------------------------------------------------------


from flask import Flask, render_template, send_from_directory
import dotenv

import json
import os
import argparse
import auth

# -----------------------------------------------------------------------

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description="Run Flask app")
parser.add_argument(
    "--production", action="store_true", help="Run in production mode (disables debug)"
)

# -----------------------------------------------------------------------


app = Flask(
    __name__,
    template_folder=os.path.abspath("templates"),
    static_folder=os.path.abspath("static"),
)

dotenv.load_dotenv()
app.secret_key = os.environ["APP_SECRET_KEY"]

auth.init_auth(app)


# Add custom URL rule to serve React files from the build directory
# This is necessary to serve the Vite-built assets in production
app.add_url_rule(
    "/build/<path:filename>",
    endpoint="build",
    view_func=lambda filename: send_from_directory("build", filename),
)

# -----------------------------------------------------------------------


def get_asset_path(entry: str) -> str:
    """
    Determine the correct asset path based on Vite's manifest file

    Args:
        entry (str): The entry point name (set in Vite's config)

    Returns:
        str: The path to the compiled asset file

    This function handles both development and production asset paths:
    - In production: Reads from Vite's manifest to get the hashed filename
    - In development/fallback: Returns a default asset path
    """
    try:
        with open("build/.vite/manifest.json", "r") as f:
            manifest = json.load(f)
            return manifest[f"src/{entry}/main.jsx"]["file"]
    except:
        return f"assets/{entry}.js"


# -----------------------------------------------------------------------


# Route handler for the main landing page
@app.route("/")
def landing():
    asset_path = get_asset_path("landing")
    return render_template(
        "index.html", app_name="landing", debug=app.debug, asset_path=asset_path
    )


# Route handler for the protected page
@app.route("/protected")
def protected():
    auth.authenticate()
    asset_path = get_asset_path("protected")
    return render_template(
        "index.html", app_name="protected", debug=app.debug, asset_path=asset_path
    )

# -----------------------------------------------------------------------


if __name__ == "__main__":
    args = parser.parse_args()
    app.debug = not args.production
    app.run(host="0.0.0.0", port=8000)
