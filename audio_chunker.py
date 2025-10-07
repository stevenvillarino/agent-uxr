#!/usr/bin/env python3
"""
Audio Chunking for Large Files
Splits large audio files into smaller chunks for processing
"""

import os
import subprocess
import tempfile
from datetime import timedelta

def get_audio_duration(file_path):
    """Get duration of audio file in seconds using ffprobe"""
    try:
        cmd = [
            'ffprobe', 
            '-v', 'quiet', 
            '-show_entries', 'format=duration', 
            '-of', 'csv=p=0', 
            file_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        duration = float(result.stdout.strip())
        return duration
    except Exception as e:
        raise Exception(f"Could not get audio duration: {e}")

def chunk_audio_file(input_file, chunk_duration_minutes=10, output_dir=None):
    """
    Split audio file into chunks of specified duration
    
    Args:
        input_file: Path to input audio file
        chunk_duration_minutes: Duration of each chunk in minutes
        output_dir: Directory to save chunks (uses temp dir if None)
    
    Returns:
        List of chunk file paths
    """
    try:
        if output_dir is None:
            output_dir = tempfile.gettempdir()
        
        # Get total duration
        total_duration = get_audio_duration(input_file)
        chunk_duration_seconds = chunk_duration_minutes * 60
        
        print(f"🎵 Audio file duration: {total_duration/60:.1f} minutes")
        print(f"✂️ Splitting into {chunk_duration_minutes}-minute chunks...")
        
        # Calculate number of chunks needed
        num_chunks = int((total_duration / chunk_duration_seconds)) + 1
        
        chunk_files = []
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        
        for i in range(num_chunks):
            start_time = i * chunk_duration_seconds
            
            # Don't create chunk if start time exceeds duration
            if start_time >= total_duration:
                break
                
            chunk_filename = f"{base_name}_chunk_{i+1:02d}.mp3"
            chunk_path = os.path.join(output_dir, chunk_filename)
            
            # Use ffmpeg to extract chunk
            cmd = [
                'ffmpeg',
                '-i', input_file,
                '-ss', str(start_time),
                '-t', str(chunk_duration_seconds),
                '-acodec', 'mp3',
                '-ab', '128k',  # Good quality for speech
                '-ar', '22050',  # Sufficient for speech
                '-y',  # Overwrite if exists
                chunk_path
            ]
            
            print(f"📦 Creating chunk {i+1}/{num_chunks}: {chunk_filename}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Failed to create chunk {i+1}: {result.stderr}")
                continue
            
            if os.path.exists(chunk_path):
                file_size = os.path.getsize(chunk_path) / (1024 * 1024)
                print(f"✅ Chunk {i+1} created: {file_size:.1f}MB")
                chunk_files.append(chunk_path)
            else:
                print(f"❌ Chunk {i+1} file not created")
        
        print(f"🎉 Successfully created {len(chunk_files)} chunks")
        return chunk_files
        
    except FileNotFoundError:
        raise Exception("FFmpeg not found. Install with: brew install ffmpeg")
    except Exception as e:
        raise Exception(f"Audio chunking failed: {str(e)}")

def cleanup_chunks(chunk_files):
    """Clean up temporary chunk files"""
    for chunk_file in chunk_files:
        try:
            if os.path.exists(chunk_file):
                os.unlink(chunk_file)
                print(f"🧹 Cleaned up: {os.path.basename(chunk_file)}")
        except Exception as e:
            print(f"⚠️ Could not clean up {chunk_file}: {e}")

if __name__ == "__main__":
    # Test with the provided file
    test_file = "/Users/stevenvillarino/Desktop/Danette_GMT20250902-180911_Recording.m4a"
    
    if os.path.exists(test_file):
        print(f"🎵 Testing chunking with: {test_file}")
        
        try:
            chunks = chunk_audio_file(test_file, chunk_duration_minutes=5)
            print(f"\n📊 Created {len(chunks)} chunks:")
            for i, chunk in enumerate(chunks, 1):
                size_mb = os.path.getsize(chunk) / (1024 * 1024)
                print(f"  {i}. {os.path.basename(chunk)} ({size_mb:.1f}MB)")
            
            # Cleanup test chunks
            cleanup_chunks(chunks)
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
    else:
        print(f"❌ Test file not found: {test_file}")