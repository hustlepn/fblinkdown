import os
from flask import Flask, request, render_template
import subprocess
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    video_url = request.form.get('url')
    links = {}
    status = None

    if video_url:
        status = "Processing video link..."
        try:
            result = subprocess.run(
                ['yt-dlp', '-j', video_url],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                raise Exception("yt-dlp failed: " + result.stderr)
            info = json.loads(result.stdout)
            for fmt in info.get('formats', []):
                url = fmt.get('url')
                note = fmt.get('format_note')
                if url and note:
                    links[note] = url
            if not links:
                status = "No downloadable formats found."
            else:
                status = "Success!"
        except Exception as e:
            status = f"Error: {str(e)}"

    return render_template('index.html', links=links, status=status)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
