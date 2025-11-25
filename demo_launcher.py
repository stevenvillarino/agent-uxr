#!/usr/bin/env python3
"""
UXR Synthesizer Demo Launcher
This script launches the demo with sample data and placeholder functionality
"""

from flask import Flask, render_template, request, jsonify
import os
import sys

app = Flask(__name__)

@app.route('/')
def index():
    """Main demo page"""
    return render_template('index.html')

@app.route('/demo')
def demo_page():
    """Demo page with sample data"""
    return """
    <html>
    <head>
        <title>UXR Synthesizer - Demo Mode</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50 min-h-screen">
        <div class="container mx-auto px-4 py-8">
            <div class="text-center mb-8">
                <h1 class="text-4xl font-bold text-gray-900 mb-4">🔬 UXR Synthesizer</h1>
                <p class="text-xl text-gray-600 mb-6">AI-Powered Research Synthesis & Presentation Automation</p>
                <div class="bg-yellow-100 border border-yellow-400 text-yellow-800 px-4 py-3 rounded mb-6">
                    <strong>Demo Mode:</strong> To process actual files, please set up your OpenAI API key in the .env file
                </div>
            </div>
            
            <div class="max-w-4xl mx-auto">
                <div class="grid md:grid-cols-2 gap-8">
                    <!-- Features Overview -->
                    <div class="bg-white rounded-lg shadow-lg p-6">
                        <h2 class="text-2xl font-bold mb-4">🚀 Current Capabilities</h2>
                        <ul class="space-y-3">
                            <li class="flex items-start">
                                <span class="text-green-500 mr-2">✅</span>
                                <span>Text transcript processing</span>
                            </li>
                            <li class="flex items-start">
                                <span class="text-green-500 mr-2">✅</span>
                                <span>Audio transcription (Whisper + ElevenLabs)</span>
                            </li>
                            <li class="flex items-start">
                                <span class="text-green-500 mr-2">✅</span>
                                <span>Speaker diarization</span>
                            </li>
                            <li class="flex items-start">
                                <span class="text-green-500 mr-2">✅</span>
                                <span>AI-powered insight extraction</span>
                            </li>
                            <li class="flex items-start">
                                <span class="text-green-500 mr-2">✅</span>
                                <span>Automatic presentation generation</span>
                            </li>
                            <li class="flex items-start">
                                <span class="text-green-500 mr-2">✅</span>
                                <span>Web interface with real-time progress</span>
                            </li>
                        </ul>
                    </div>
                    
                    <!-- Sample Data -->
                    <div class="bg-white rounded-lg shadow-lg p-6">
                        <h2 class="text-2xl font-bold mb-4">📁 Sample Data Available</h2>
                        <div class="space-y-3">
                            <div class="border rounded p-3">
                                <h3 class="font-semibold">User Interview - Dashboard</h3>
                                <p class="text-sm text-gray-600">UX research session about dashboard usability</p>
                            </div>
                            <div class="border rounded p-3">
                                <h3 class="font-semibold">Focus Group - Mobile App</h3>
                                <p class="text-sm text-gray-600">Mobile app feedback session</p>
                            </div>
                            <div class="border rounded p-3">
                                <h3 class="font-semibold">Customer Support Call</h3>
                                <p class="text-sm text-gray-600">Support interaction analysis</p>
                            </div>
                            <div class="border rounded p-3">
                                <h3 class="font-semibold">Team Standup Meeting</h3>
                                <p class="text-sm text-gray-600">Team coordination meeting</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Setup Instructions -->
                <div class="bg-white rounded-lg shadow-lg p-6 mt-8">
                    <h2 class="text-2xl font-bold mb-4">⚙️ Quick Setup Instructions</h2>
                    <div class="grid md:grid-cols-2 gap-6">
                        <div>
                            <h3 class="font-semibold mb-2">1. Get OpenAI API Key</h3>
                            <p class="text-sm text-gray-600 mb-3">Required for AI analysis and processing</p>
                            <a href="https://platform.openai.com/api-keys" target="_blank" 
                               class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition">
                                Get OpenAI API Key →
                            </a>
                        </div>
                        <div>
                            <h3 class="font-semibold mb-2">2. Add to .env file</h3>
                            <code class="block bg-gray-100 p-2 rounded text-sm">
                                OPENAI_API_KEY=your_key_here
                            </code>
                        </div>
                    </div>
                    
                    <div class="mt-6 p-4 bg-blue-50 rounded">
                        <h3 class="font-semibold mb-2">💡 Optional: Enhanced Features</h3>
                        <p class="text-sm text-gray-600">
                            Add ElevenLabs API key for speaker diarization and enhanced audio processing.
                            <a href="https://elevenlabs.io/" class="text-blue-600 hover:underline">Get ElevenLabs API Key</a>
                        </p>
                    </div>
                </div>
                
                <!-- How It Works -->
                <div class="bg-white rounded-lg shadow-lg p-6 mt-8">
                    <h2 class="text-2xl font-bold mb-4">🔄 How It Works</h2>
                    <div class="flex flex-wrap justify-center items-center space-x-4 text-sm">
                        <div class="text-center">
                            <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-2 mx-auto">
                                <span class="text-2xl">📁</span>
                            </div>
                            <span>Upload File</span>
                        </div>
                        <span class="text-gray-400">→</span>
                        <div class="text-center">
                            <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-2 mx-auto">
                                <span class="text-2xl">🎵</span>
                            </div>
                            <span>Transcribe</span>
                        </div>
                        <span class="text-gray-400">→</span>
                        <div class="text-center">
                            <div class="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mb-2 mx-auto">
                                <span class="text-2xl">🧠</span>
                            </div>
                            <span>AI Analysis</span>
                        </div>
                        <span class="text-gray-400">→</span>
                        <div class="text-center">
                            <div class="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center mb-2 mx-auto">
                                <span class="text-2xl">📊</span>
                            </div>
                            <span>Generate Slides</span>
                        </div>
                    </div>
                </div>
                
                <div class="text-center mt-8">
                    <p class="text-gray-600 mb-4">Ready to get started? Set up your API keys and refresh this page!</p>
                    <button onclick="location.reload()" 
                            class="bg-black text-white px-6 py-3 rounded-lg hover:bg-gray-800 transition">
                        🔄 Refresh Demo
                    </button>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("🔬 UXR Synthesizer Demo")
    print("=" * 50)
    print("🚀 Starting demo server...")
    print("📱 Open: http://localhost:8080")
    print("⚙️  To use full functionality, add your OpenAI API key to .env file")
    print("=" * 50)
    
    try:
        app.run(host='0.0.0.0', port=8080, debug=True)
    except KeyboardInterrupt:
        print("\n👋 Demo stopped")