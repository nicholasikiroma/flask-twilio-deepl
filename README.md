# Tutorial: Building a Multilingual Chat Application For Customer Support with Flask, Twilio Conversations, and DeepL Translation AI
![Screenshot of chat screen](./static/images/Screenshot%20from%202023-06-10%2018-26-56.png)

## Description:
A dynamic web chat application for real-time message translations based on preset language defaults.

## Usage:

Download or clone repo:
```bash
git clone https://github.com/nicholasikiroma/flask-twilio-deepl.git
```

Navigate to cloned directory:
```bash
cd flask-twilio-deepl
```

Create virtual environment and activate it:
```bash
virtualenv venv
source venv/bin/activate
```

Install Python dependencies:
```bash
pip install -r requirements.txt
```

Create a *.env* file with the contents:
```text
TWILIO_AUTH_TOKEN=<your-twilio-auth-token>
TWILIO_API_KEY_SID=<your-twilio-api-key-sid>
TWILIO_API_KEY_SECRET=<your-twilio-api-key-secret>
FLASK_SECRET_KEY=<your-flask-secret-key>
DEEPL_AUTH_KEY=<your-deepl-auth-key>
```

Install Node depencencies:
```bash
npm install
```

Run Tailwind:
```bash
npm run buid
```

Run Flask:
```bash
flask run --debug
```

