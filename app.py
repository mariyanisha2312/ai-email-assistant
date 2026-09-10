from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_email():

    try:

        data = request.get_json()

        email_type = data.get("email_type")
        user_request = data.get("request")

        prompt = f"""
You are a professional email writing assistant.

Email type:
{email_type}

User request:
{user_request}

Write a professional email.

Include:
- A suitable subject
- Greeting
- Clear and polite email body
- Professional closing

Return only the email.
"""

        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=prompt
        )

        email = response.text

        return jsonify({
            "success": True,
            "email": email
        })

    except Exception as e:

        print("AI ERROR:", e)

        return jsonify({
            "success": False,
            "message": "AI service is temporarily busy. Please try again in a few seconds."
        }), 503

if __name__ == "__main__":
    app.run(debug=True)