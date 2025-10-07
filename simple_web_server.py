#!/usr/bin/env python3
"""
Fixed Web Server for Agent-UXR
Simple, stable web interface
"""

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import tempfile
import uuid
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

UPLOAD_FOLDER = tempfile.gettempdir()

def get_file_size_mb(file_path):
    """Get file size in MB"""
    size_bytes = os.path.getsize(file_path)
    return size_bytes / (1024 * 1024)

def simple_transcribe(audio_file_path):
    """Simple transcription for web interface"""
    try:
        file_size_mb = get_file_size_mb(audio_file_path)
        print(f"📁 Processing audio file: {file_size_mb:.1f}MB")
        
        if file_size_mb <= 24:
            # Direct API call
            print(f"📡 Using OpenAI Whisper API")
            with open(audio_file_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            
            return {
                'text': transcript,
                'service': 'OpenAI Whisper API',
                'success': True
            }
        else:
            return {
                'text': f"File too large ({file_size_mb:.1f}MB). Please use chunks under 25MB or use the command line tool for large files.",
                'service': 'Error',
                'success': False
            }
            
    except Exception as e:
        return {
            'text': f"Transcription failed: {str(e)}",
            'service': 'Error',
            'success': False
        }

def simple_analysis(transcript):
    """Simple UX analysis"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """You are a UX research expert. Analyze the transcript and provide:
1. A brief summary (2-3 sentences)
2. 5-7 key themes
3. Main user pain points
4. Actionable recommendations

Be specific and focus on actionable UX insights."""
                },
                {
                    "role": "user",
                    "content": f"Analyze this user research transcript:\n\n{transcript}"
                }
            ],
            max_tokens=1000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Analysis failed: {str(e)}"

@app.route('/')
def index():
    """Main page"""
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Agent-UXR - Simple Interface</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { background: #f5f5f5; padding: 20px; border-radius: 10px; margin: 20px 0; }
        .upload-area { border: 2px dashed #ccc; padding: 40px; text-align: center; margin: 20px 0; }
        button { background: #007cba; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #005a87; }
        .result { background: white; padding: 20px; border-radius: 5px; margin: 20px 0; white-space: pre-wrap; }
        .loading { color: #666; font-style: italic; }
        .error { color: red; }
        .success { color: green; }
    </style>
</head>
<body>
    <h1>🎵 Agent-UXR - Audio Analysis</h1>
    
    <div class="container">
        <h2>Upload Audio File</h2>
        <div class="upload-area">
            <input type="file" id="audioFile" accept=".mp3,.wav,.m4a,.mp4" />
            <p>Supported: MP3, WAV, M4A, MP4 (max 25MB)</p>
        </div>
        <button onclick="processAudio()">🎤 Transcribe & Analyze</button>
    </div>
    
    <div id="status" class="result" style="display: none;"></div>
    <div id="result" class="result" style="display: none;"></div>
    
    <script>
        function processAudio() {
            const fileInput = document.getElementById('audioFile');
            const statusDiv = document.getElementById('status');
            const resultDiv = document.getElementById('result');
            
            if (!fileInput.files[0]) {
                alert('Please select an audio file');
                return;
            }
            
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            
            statusDiv.style.display = 'block';
            statusDiv.className = 'result loading';
            statusDiv.textContent = '🎤 Processing audio... This may take 1-2 minutes.';
            
            resultDiv.style.display = 'none';
            
            fetch('/process', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                statusDiv.style.display = 'none';
                resultDiv.style.display = 'block';
                
                if (data.success) {
                    resultDiv.className = 'result success';
                    resultDiv.textContent = data.result;
                } else {
                    resultDiv.className = 'result error';
                    resultDiv.textContent = 'Error: ' + data.error;
                }
            })
            .catch(error => {
                statusDiv.style.display = 'none';
                resultDiv.style.display = 'block';
                resultDiv.className = 'result error';
                resultDiv.textContent = 'Error: ' + error.message;
            });
        }
    </script>
</body>
</html>
    '''

@app.route('/process', methods=['POST'])
def process():
    """Process uploaded audio file"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        audio_path = os.path.join(UPLOAD_FOLDER, f"audio_{uuid.uuid4().hex[:8]}_{filename}")
        file.save(audio_path)
        
        print(f"📁 Processing: {filename}")
        
        # Transcribe
        transcript_result = simple_transcribe(audio_path)
        
        if not transcript_result['success']:
            os.unlink(audio_path)
            return jsonify({'success': False, 'error': transcript_result['text']})
        
        transcript = transcript_result['text']
        print(f"✅ Transcription complete: {len(transcript)} characters")
        
        # Analyze
        print(f"🤖 Generating insights...")
        analysis = simple_analysis(transcript)
        
        # Clean up
        os.unlink(audio_path)
        
        # Format result
        result = f"""🎵 AUDIO ANALYSIS COMPLETE

📊 TRANSCRIPTION ({len(transcript)} characters)
{transcript}

🎯 UX ANALYSIS
{analysis}

📝 Processed with: {transcript_result['service']}
⏰ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return jsonify({'success': True, 'result': result})
        
    except Exception as e:
        print(f"❌ Processing error: {e}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("🚀 Starting Simple Agent-UXR Web Interface...")
    print("🌐 URL: http://127.0.0.1:8080")
    print("📝 Ready for audio files up to 25MB!")
    
    app.run(host='127.0.0.1', port=8080, debug=False)