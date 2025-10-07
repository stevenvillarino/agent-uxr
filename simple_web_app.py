#!/usr/bin/env python3
"""
Simple web server for Agent-UXR on port 5000
"""

import os
import sys
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Add the current directory to the path to import from main modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_enhanced import get_insights_from_llm, format_marp_presentation

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Agent-UXR - UX Research Analysis</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100 min-h-screen">
        <div class="container mx-auto px-4 py-8">
            <div class="max-w-4xl mx-auto">
                <h1 class="text-4xl font-bold text-center mb-8 text-gray-800">
                    🧠 Agent-UXR
                </h1>
                <p class="text-center text-xl text-gray-600 mb-8">
                    Transform user research into actionable UX insights
                </p>
                
                <div class="bg-white rounded-lg shadow-lg p-8">
                    <h2 class="text-2xl font-semibold mb-6">Analyze Your Research</h2>
                    
                    <form id="analysisForm" class="space-y-6">
                        <div>
                            <label for="transcript" class="block text-sm font-medium text-gray-700 mb-2">
                                Paste your user interview transcript:
                            </label>
                            <textarea 
                                id="transcript" 
                                name="transcript" 
                                rows="10" 
                                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                                placeholder="Paste your user interview transcript here..."
                            ></textarea>
                        </div>
                        
                        <button 
                            type="submit" 
                            class="w-full bg-indigo-600 text-white py-3 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 font-medium"
                        >
                            🚀 Analyze with AI
                        </button>
                    </form>
                    
                    <div id="results" class="mt-8 hidden">
                        <h3 class="text-xl font-semibold mb-4">Analysis Results</h3>
                        <div id="analysis-content" class="bg-gray-50 p-4 rounded-md">
                            <!-- Results will appear here -->
                        </div>
                    </div>
                    
                    <div id="loading" class="mt-8 hidden text-center">
                        <p class="text-gray-600">🤖 Analyzing with GPT-4o...</p>
                    </div>
                </div>
                
                <div class="mt-8 text-center">
                    <p class="text-gray-500">
                        ✅ Real GPT-4o analysis • ✅ Whisper transcription • ✅ API connected
                    </p>
                </div>
            </div>
        </div>

        <script>
            document.getElementById('analysisForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const transcript = document.getElementById('transcript').value;
                if (!transcript.trim()) {
                    alert('Please enter a transcript to analyze');
                    return;
                }
                
                document.getElementById('loading').classList.remove('hidden');
                document.getElementById('results').classList.add('hidden');
                
                try {
                    const response = await fetch('/analyze', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ transcript: transcript })
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        document.getElementById('analysis-content').innerHTML = `
                            <h4 class="font-semibold text-lg mb-3">📋 Executive Summary</h4>
                            <p class="mb-4">${result.insights.summary}</p>
                            
                            <h4 class="font-semibold text-lg mb-3">🎯 Key Themes</h4>
                            <ul class="list-disc pl-5 mb-4">
                                ${result.insights.themes.map(theme => `<li class="mb-2">${theme}</li>`).join('')}
                            </ul>
                            
                            <h4 class="font-semibold text-lg mb-3">🚨 Pain Points</h4>
                            <ul class="list-disc pl-5 mb-4">
                                ${result.insights.pain_points.map(pain => `<li class="mb-2">${pain}</li>`).join('')}
                            </ul>
                            
                            <h4 class="font-semibold text-lg mb-3">💡 Recommendations</h4>
                            <ul class="list-disc pl-5">
                                ${result.insights.recommendations.map(rec => `<li class="mb-2">${rec}</li>`).join('')}
                            </ul>
                        `;
                        document.getElementById('results').classList.remove('hidden');
                    } else {
                        alert('Analysis failed: ' + result.error);
                    }
                } catch (error) {
                    alert('Error: ' + error.message);
                } finally {
                    document.getElementById('loading').classList.add('hidden');
                }
            });
        </script>
    </body>
    </html>
    """

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        transcript = data.get('transcript', '')
        
        if not transcript:
            return jsonify({'success': False, 'error': 'No transcript provided'})
        
        # Use the enhanced analysis function
        insights = get_insights_from_llm(transcript)
        
        if insights:
            return jsonify({
                'success': True,
                'insights': insights
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to analyze transcript. Check your OpenAI API key.'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("🚀 Starting Agent-UXR Web Interface...")
    print("📝 Real API analysis enabled!")
    print("🌐 Open http://localhost:5000 in your browser")
    app.run(debug=True, host='127.0.0.1', port=5000)