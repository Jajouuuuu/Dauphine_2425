#!/usr/bin/env python3
"""
Data Splitting Script
Splits large JSON files into smaller chunks for testing and development.
"""

import json
import os
from pathlib import Path
import math

def split_json_file(input_file, output_dir, num_chunks=3):
    """Split a JSON file into multiple smaller files"""
    
    print(f"📂 Processing {input_file}...")
    
    # Read the original file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Determine the data structure
    if "movies" in data:
        items = data["movies"]
        data_type = "movies"
    elif "games" in data:
        items = data["games"]
        data_type = "games"
    else:
        print(f"❌ Unknown data structure in {input_file}")
        return
    
    total_items = len(items)
    chunk_size = math.ceil(total_items / num_chunks)
    
    print(f"📊 Total {data_type}: {total_items:,}")
    print(f"📦 Chunk size: ~{chunk_size:,} items each")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Split and save chunks
    for i in range(num_chunks):
        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, total_items)
        chunk_items = items[start_idx:end_idx]
        
        if not chunk_items:  # Skip empty chunks
            continue
        
        # Create output filename
        base_name = Path(input_file).stem
        output_file = output_path / f"{base_name}_part{i+1}.json"
        
        # Create chunk data with same structure
        chunk_data = {data_type: chunk_items}
        
        # Save chunk
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chunk_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved {len(chunk_items):,} {data_type} to {output_file}")
    
    print(f"🎉 Split {input_file} into {num_chunks} parts!")
    print()

def main():
    """Main splitting routine"""
    print("📊 JSON Data Splitter")
    print("=" * 30)
    print()
    
    # Input files
    movies_file = "data/processed/movies.json"
    games_file = "data/processed/games.json"
    
    # Output directory
    output_dir = "data/processed/chunks"
    
    # Check if input files exist
    files_to_process = []
    
    if os.path.exists(movies_file):
        files_to_process.append(movies_file)
        print(f"✅ Found: {movies_file}")
    else:
        print(f"⚠️  Not found: {movies_file}")
    
    if os.path.exists(games_file):
        files_to_process.append(games_file)
        print(f"✅ Found: {games_file}")
    else:
        print(f"⚠️  Not found: {games_file}")
    
    if not files_to_process:
        print("❌ No data files found to process!")
        return
    
    print(f"📁 Output directory: {output_dir}")
    print()
    
    # Process each file
    for file_path in files_to_process:
        split_json_file(file_path, output_dir, num_chunks=3)
    
    # Show results
    print("📋 Summary:")
    print("=" * 20)
    
    chunk_files = list(Path(output_dir).glob("*.json"))
    chunk_files.sort()
    
    for chunk_file in chunk_files:
        try:
            with open(chunk_file, 'r') as f:
                chunk_data = json.load(f)
            
            if "movies" in chunk_data:
                count = len(chunk_data["movies"])
                data_type = "movies"
            elif "games" in chunk_data:
                count = len(chunk_data["games"])
                data_type = "games"
            else:
                count = "unknown"
                data_type = "unknown"
            
            file_size = chunk_file.stat().st_size / (1024 * 1024)  # MB
            print(f"📄 {chunk_file.name}: {count:,} {data_type} ({file_size:.1f}MB)")
            
        except Exception as e:
            print(f"❌ Error reading {chunk_file}: {e}")
    
    print()
    print("🎯 Usage Instructions:")
    print("=" * 25)
    print("1. Use the chunk files to test your RAG system:")
    print(f"   - Movies: {output_dir}/movies_part1.json")
    print(f"   - Games:  {output_dir}/games_part1.json")
    print()
    print("2. Update your chat app to use smaller files:")
    print("   repository = JSONMediaRepository(")
    print(f"       movies_path='{output_dir}/movies_part1.json',")
    print(f"       games_path='{output_dir}/games_part1.json'")
    print("   )")
    print()
    print("3. When ready, use part2, part3, or original files")
    print()
    print("🚀 Ready to test with smaller dataset!")

if __name__ == "__main__":
    main() 