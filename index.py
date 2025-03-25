from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_mp3', methods=['GET'])
def get_video():
    query = request.args.get('query', '')
    if query:
        api_url = f"https://coderx-api.onrender.com/v1/downloaders/coderx/download/ytmp3v2?query={query}"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                result = data.get('result', {})
                video_details = {
                    'title': result.get('title'),
                    'description': result.get('description'),
                    'image': result.get('image'),
                    'audio_url': result.get('download', {}).get('audio'),
                    'views': result.get('views')
                }
                return jsonify(video_details)
            else:
                return jsonify({'error': 'Video not found or failed to fetch data.'})
        else:
            return jsonify({'error': 'Failed to fetch data from API.'})
    return jsonify({'error': 'Query parameter is required.'})


@app.route('/get_facebook_video', methods=['GET'])
def get_facebook_video():
    url = request.args.get('url', '')
    if url:
        api_url = f"https://coderx-api.onrender.com/v1/downloaders/coderx/download/facebook?url={url}"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status'):
                video_details = {
                    'title': data['video'].get('title'),
                    'thumbnail': data['video'].get('thumbnail'),
                    'hdDownloadUrl': data['video'].get('hdDownloadUrl')
                }
                return jsonify(video_details)
            else:
                return jsonify({'error': 'Video not found or failed to fetch data.'})
        else:
            return jsonify({'error': 'Failed to fetch data from API.'})
    return jsonify({'error': 'URL parameter is required.'})


@app.route('/get_instagram_video', methods=['GET'])
def get_instagram_video():
    url = request.args.get('url', '')
    if url:
        api_url = f"https://coderx-api.onrender.com/v1/downloaders/coderx/download/instagram?url={url}"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 200 and data.get('success'):
                video_details = {
                    'creator': data['creator'],
                    'downloadUrl': data['downloadUrl'],
                    'type': data['type'],
                }
                return jsonify(video_details)
            else:
                return jsonify({'error': 'Video not found or failed to fetch data.'})
        else:
            return jsonify({'error': 'Failed to fetch data from API.'})
    return jsonify({'error': 'URL parameter is required.'})


if __name__ == '__main__':
    app.run(debug=True)
