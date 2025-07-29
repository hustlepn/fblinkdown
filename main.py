from flask import Flask, request, render_template
import subprocess
import json
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    video_url = request.form.get("url")
    links = {}
    status = None

    if video_url:
        try:
            result = subprocess.run(
                ["yt-dlp", "-j", video_url],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                status = "Failed to fetch video info. Please check the URL."
            else:
                info = json.loads(result.stdout)
                formats = info.get("formats", [])

                for f in formats:
                    # Filter only progressive formats (have both video and audio)
                    if f.get("acodec") != "none" and f.get("vcodec") != "none" and f.get("url"):
                        label = f"{f.get('format_note', '')} - {f.get('ext', '')} - {f.get('resolution', '')}"
                        links[label] = f["url"]

                if not links:
                    status = "No valid video formats found."

        except Exception as e:
            status = f"Error: {str(e)}"

    return render_template("index.html", links=links, status=status)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
