import os
import whisper
import ffmpeg
import json

def transcribe_media(media_dir, output_dir=None):
    model = whisper.load_model("tiny")  

    if output_dir is None:
        output_dir = media_dir 

    for root, _, files in os.walk(media_dir):
        for file in files:
            if file.lower().endswith(('.mp3', '.mp4', '.wav', '.mov', '.avi', '.webm')):
                media_path = os.path.abspath(os.path.join(root, file)) 
                print(f"Attempting to transcribe: {media_path}")
                print(f"File exists: {os.path.exists(media_path)}")
                base_name = os.path.splitext(file)[0]
                if output_dir is None:
                    output_dir = os.path.abspath(media_dir) 
                output_path_txt = os.path.abspath(os.path.join(output_dir, f"{base_name}.txt")) 
                output_path_json = os.path.abspath(os.path.join(output_dir, f"{base_name}.json")) 
                try:
                   
                    
                    result = model.transcribe(media_path)

                    # Save as text
                    with open(output_path_txt, "w", encoding="utf-8") as f:
                        f.write(result["text"])

                    # Save as JSON
                    with open(output_path_json, "w", encoding="utf-8") as f:
                        json.dump(result, f, indent=4, ensure_ascii=False) 

                    print(f"Transcribed: {media_path}")

                except Exception as e:
                    print(f"Error transcribing {media_path}: {e}")
            elif file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                print(f"Skipping non-media file: {file}")
            else:
                print(f"Unsupported file type: {file}")

if __name__ == "__main__":
    media_directory = input("Enter the directory containing media files: ")
    media_directory = os.path.abspath(media_directory) # Convert input to absolute path
    output_directory = input("Enter the output directory (or press Enter to use the same directory): ")
    if not output_directory:
        output_directory = media_directory # Use the same (absolute) path
    else:
        output_directory = os.path.abspath(output_directory) # Make sure output_dir is also absolute
    transcribe_media(media_directory, output_directory)
    print("Transcription complete.")
