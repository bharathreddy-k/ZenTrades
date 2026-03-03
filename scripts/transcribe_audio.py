import os
import sys
from pathlib import Path

# Check if whisper is installed
try:
    import whisper
except ImportError:
    print("❌ ERROR: 'openai-whisper' is not installed.")
    print("\n📦 Please install it first:")
    print("   pip install openai-whisper")
    print("   pip install torch")
    sys.exit(1)


def transcribe_audio_file(audio_path, output_dir, model_name="base"):
    """
    Transcribe a single audio file using Whisper.
    
    Args:
        audio_path: Path to the audio file
        output_dir: Directory to save the transcript
        model_name: Whisper model to use (tiny, base, small, medium, large)
    """
    # Check if file exists
    if not os.path.exists(audio_path):
        print(f"❌ ERROR: Audio file not found: {audio_path}")
        return None
    
    print(f"\n{'='*60}")
    print(f"Processing: {audio_path}")
    print(f"File size: {os.path.getsize(audio_path) / (1024*1024):.2f} MB")
    print(f"{'='*60}")
    
    try:
        # Load Whisper model
        print(f"Loading Whisper model '{model_name}'...")
        model = whisper.load_model(model_name)
        
        # Transcribe
        print("Transcribing audio... (this may take a few minutes)")
        result = model.transcribe(str(audio_path))
    except Exception as e:
        print(f"\n❌ ERROR during transcription: {e}")
        if "ffmpeg" in str(e).lower():
            print("\n💡 FFmpeg is not installed. Whisper requires FFmpeg to process audio.")
            print("   Download: https://ffmpeg.org/download.html")
            print("   Or use: winget install ffmpeg")
        return None
    
    # Extract filename without extension
    filename = Path(audio_path).stem
    
    # Determine output directory based on filename
    if "demo" in filename.lower():
        target_dir = "../dataset/demo"
    elif "onboarding" in filename.lower():
        target_dir = "../dataset/onboarding"
    else:
        target_dir = output_dir
    
    # Create directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    # Save transcript
    output_file = os.path.join(target_dir, f"{filename}.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result["text"])
    
    print(f"✅ Transcript saved to: {output_file}")
    print(f"Duration: ~{result.get('duration', 'unknown')} seconds")
    print(f"Language detected: {result.get('language', 'unknown')}")
    
    return output_file


def transcribe_directory(input_dir, output_dir="../dataset/demo", model_name="base"):
    """
    Transcribe all audio files in a directory.
    
    Args:
        input_dir: Directory containing audio files
        output_dir: Default output directory
        model_name: Whisper model to use
    """
    supported_formats = [".mp3", ".m4a", ".wav", ".mp4", ".flac"]
    
    audio_files = []
    for ext in supported_formats:
        audio_files.extend(Path(input_dir).glob(f"*{ext}"))
    
    if not audio_files:
        print(f"❌ No audio files found in {input_dir}")
        return
    
    print(f"\n🎵 Found {len(audio_files)} audio file(s)")
    
    for audio_file in audio_files:
        try:
            transcribe_audio_file(audio_file, output_dir, model_name)
        except Exception as e:
            print(f"❌ Error processing {audio_file}: {e}")
    
    print(f"\n{'='*60}")
    print("✅ All transcriptions complete!")
    print(f"{'='*60}")


def main():
    """
    Main function to handle transcription.
    Modify the paths below based on your needs.
    """
    
    # Option 1: Transcribe a specific file
    # Uncomment and modify this section for single file transcription
    
    specific_file = r"c:\Users\Bharath\Downloads\audio1975518882.m4a"
    
    print(f"🔍 Checking file: {specific_file}")
    
    if os.path.exists(specific_file):
        print(f"✅ File found!")
        # You can choose model size: "tiny", "base", "small", "medium", "large"
        # "base" is a good balance of speed and accuracy
        result = transcribe_audio_file(specific_file, "../dataset/demo", model_name="base")
        if result:
            print(f"\n✅ SUCCESS! Transcript saved.")
        else:
            print(f"\n❌ Transcription failed. Check errors above.")
    else:
        print(f"❌ File not found: {specific_file}")
        print("\n💡 Please check:")
        print("   1. Is the file path correct?")
        print("   2. Does the file exist in that location?")
        print("\n📁 Current files in Downloads folder:")
        downloads_dir = r"c:\Users\Bharath\Downloads"
        if os.path.exists(downloads_dir):
            audio_files = [f for f in os.listdir(downloads_dir) if f.lower().endswith(('.m4a', '.mp3', '.wav'))]
            if audio_files:
                for f in audio_files[:10]:  # Show first 10
                    print(f"   - {f}")
            else:
                print("   (No audio files found)")
        else:
            print("   (Downloads folder not accessible)")
    
    
    # Option 2: Transcribe all files from a directory
    # Uncomment this section if you want to process multiple files
    
    # raw_audio_dir = "../dataset/raw_audio"
    # 
    # if os.path.exists(raw_audio_dir):
    #     print("🎯 Transcribing all files from raw_audio directory...")
    #     transcribe_directory(raw_audio_dir, model_name="base")
    # else:
    #     print(f"❌ Directory not found: {raw_audio_dir}")
    #     print("Creating directory... Please add audio files and run again.")
    #     os.makedirs(raw_audio_dir, exist_ok=True)


if __name__ == "__main__":
    # Make sure we're in the scripts directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("\n" + "="*60)
    print("🎙️  WHISPER AUDIO TRANSCRIPTION")
    print("="*60)
    
    main()
