# 1-Server Flask with React Frontend Example (Google Auth)

This is a simple example of a Flask server with a React frontend with Vite. During production, only 1 server (the Flask server) is needed to serve both the frontend and backend. During development, there are 2 servers to enable hot module reloading for the frontend.

This example uses **Google OAuth2 authentication**. If you would like to see an example with Princeton CAS, please see [this repository](https://github.com/joshuamotoaki/flask-vite-react). The only difference between the two repositories is the authentication method.

## Explanation

The [`index.html`](backend/templates/index.html) file is the entry point for the frontend. During dev mode, the frontend is served by Vite. The Flask app will automatically grab these files from the Vite server so that hot module reloading is enabled. When the frontend is built, the static files are placed in the `backend/build` folder. The Flask server serves the static files from the `backend/build` folder during production.

## Getting Started

First, let's handle Google Auth setup. OAuth2 requires HTTPS, so we will have to generate self-signed certificates for local development. Generate the private key and certificate using OpenSSL in the `backend` folder:

```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

Fill in the certificate information when prompted:

```
Country Name: US
State or Province Name: NJ
Locality Name: Princeton
Organization Name: Princeton University
Organizational Unit Name: [can be blank]
Common Name: localhost
Email Address: [can be blank]
```

1. Register the app (https://localhost:8000) as a client of Google.
2. Log into Google using your project Google account
3. Browse to https://console.developers.google.com/apis/credentials
4. Click CREATE PROJECT – for Project name enter your project name
5. Click CREATE Click CONFIGURE CONSENT SCREEN – for User Type choose External
6. Click CREATE For App name enter your app name
7. For User support email enter your your project gmail address. For Developer contact information enter your project gmail address
8. Click SAVE AND CONTINUE a few times to finish the consent
9. Click Credentials, Click Create Credentials, OAuth client ID, Web Application. In newer versions, there might be a button that just says "Create OAuth client ID"
10. In Authorized JavaScript origins: Click ADD URI Enter https://localhost:8000 Typically you also would add a URI for your app on Render or Heroku. In Authorized redirect URIs: Click ADD URI Enter https://localhost:8000/login/callback Typically you also would add a callback URI for your app on Render or Heroku.
11. Add Client ID and Client Secret to the `.env` file.

Now, let's run the application:

1. Clone the repository
2. Create a virtual environment `python -m venv .venv`
3. Activate the virtual environment `source .venv/bin/activate`
4. Install the dependencies `pip install -r requirements.txt`
5. Install the frontend dependencies `cd frontend && npm install`
6. Start the frontend `cd frontend && npm run dev`
7. Start the backend `cd backend && python app.py`
8. Open the browser and go to `https://localhost:8000`

It is very important that you use `https` and not `http` when accessing the site (otherwise it will not work).

## Building for Production

To build the frontend for production, run the following command in the `frontend` folder:

```bash
npm run build
```

You should notice that the frontend files are now in the `backend/build` folder. To run the Flask server in production mode, run the following command in the `backend` folder:

```bash
python app.py --production
```

In reality, you would want to serve the Flask app using a production-ready server like Gunicorn.
