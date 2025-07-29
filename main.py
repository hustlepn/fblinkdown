from flask import Flask, request, render_template
import subprocess
import json
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    video_url = request.form.get('url')
    links = {}
    info = {}
    status = None

    if video_url:
        try:
            # Run yt-dlp with custom user-agent to support Instagram
            result = subprocess.run(
                ['yt-dlp', '-j', '--user-agent', 'Mozilla/5.0', video_url],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode != 0 or not result.stdout:
                raise Exception("yt-dlp returned no data")

            info = json.loads(result.stdout)

            for fmt in info.get('formats', []):
                if fmt.get('url') and fmt.get('format_note'):
                    label = fmt['format_note']
                    links[label] = fmt['url']

            if not links:
                status = "⚠️ No downloadable formats found. Please try a different link."

        except Exception as e:
            print("Error:", e)
            status = "⚠️ Could not fetch video. Make sure it's public and try again."

    return render_template('index.html', links=links, info=info, status=status)

# For Railway or local testing
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
