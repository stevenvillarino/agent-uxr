#!/usr/bin/env python3
"""
Create Permanent Audio Chunks
This will create and save audio chunks without deleting them
"""

import os
import sys
from audio_chunker import chunk_audio_file

def create_permanent_chunks():
    """Create chunks and save them permanently"""
    
    input_file = "/Users/stevenvillarino/Desktop/Danette_GMT20250902-180911_Recording.m4a"
    output_dir = "/Users/stevenvillarino/Projects/stevenvillarino/agent-uxr/chunks"
    
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return
    
    # Create chunks directory
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🎵 Creating permanent chunks from: {input_file}")
    print(f"📁 Saving to: {output_dir}")
    print("=" * 60)
    
    try:
        # Create chunks without auto-cleanup
        chunk_files = chunk_audio_file(
            input_file, 
            chunk_duration_minutes=5,  # 5-minute chunks
            output_dir=output_dir
        )
        
        print(f"\n✅ Created {len(chunk_files)} permanent chunks:")
        print(f"📂 Location: {output_dir}")
        print("\n📋 Chunk List:")
        
        total_size = 0
        for i, chunk_file in enumerate(chunk_files, 1):
            size_mb = os.path.getsize(chunk_file) / (1024 * 1024)
            total_size += size_mb
            print(f"  {i:2d}. {os.path.basename(chunk_file)} ({size_mb:.1f}MB)")
        
        print(f"\n📊 Summary:")
        print(f"   Total chunks: {len(chunk_files)}")
        print(f"   Total size: {total_size:.1f}MB")
        print(f"   Average per chunk: {total_size/len(chunk_files):.1f}MB")
        print(f"   Location: {output_dir}")
        
        return chunk_files
        
    except Exception as e:
        print(f"❌ Failed to create chunks: {e}")
        return None

if __name__ == "__main__":
    create_permanent_chunks()