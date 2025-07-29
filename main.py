from flask import Flask, request, render_template
import subprocess
import json
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    video_url = request.form.get('url')
    links = {}
    status = ""

    if video_url:
        try:
            # Use yt-dlp to get video info
            result = subprocess.run(
                ['yt-dlp', '-j', video_url],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            info = json.loads(result.stdout)

            for format in info.get('formats', []):
                # Only include formats with both audio and video (non-DASH)
                if (
                    format.get('url')
                    and format.get('format_note')
                    and format.get('acodec') != 'none'
                    and format.get('vcodec') != 'none'
                ):
                    label = format['format_note']
                    links[label] = format['url']

            status = "Success!" if links else "No valid formats found."

        except Exception as e:
            status = f"Error: {str(e)}"

    return render_template('index.html', links=links, status=status)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
