from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:4b"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()

    time_available = data.get("time", "")
    place = data.get("place", "")
    mood = data.get("mood", "")

    prompt = f"""
You are Grounded, an AI outdoor companion.

Your purpose is to help people spend meaningful time away from screens.

Create a simple outdoor mission based on:

Time available: {time_available}
Place/environment: {place}
Current mood: {mood}

Return the response using exactly these sections:

MISSION TITLE:
A short creative title.

MISSION:
A motivating outdoor activity that can realistically be completed within the available time.

NOTICE & EXPLORE:
Give exactly 3 simple things the person can notice, observe, hear, smell, or explore.

PHONE-FREE CHALLENGE:
Give one small challenge that encourages the person to keep their phone away.

REFLECTION:
End with one thoughtful question they can think about after completing the mission.

Keep everything practical, positive, and safe.
Do not suggest dangerous activities.
Do not require expensive equipment.
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()
        result = response.json()

        return jsonify({"result": result["response"]})

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Could not connect to Ollama. Make sure Ollama is running."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)