import os  # Used for handling file paths and directory traversal.
import whisper # A speech-to-text model for transcribing media files.
import ffmpeg # A media processing library (though not directly used in the code).
import json # Used to store transcription results in JSON format.

def transcribe_media(media_dir, output_dir=None): # Directory containing media files (audio/video).
   # Directory where transcriptions will be saved (defaults to media_dir).

    model = whisper.load_model("tiny")  # Loads the "tiny" version of Whisper (a lightweight model for transcription).

    if output_dir is None:
        output_dir = media_dir 

    for root, _, files in os.walk(media_dir): # os.walk(media_dir): Recursively traverses all files in media_dir.
        for file in files:
            if file.lower().endswith(('.mp3', '.mp4', '.wav', '.mov', '.avi', '.webm')):# Filters audio/video files based on their extensions.
                media_path = os.path.abspath(os.path.join(root, file)) # Gets the absolute path of the media file.
                print(f"Attempting to transcribe: {media_path}") # Prints debug messages to confirm file processing.
                print(f"File exists: {os.path.exists(media_path)}")

                base_name = os.path.splitext(file)[0] #Extracts the file name (without extension).
                if output_dir is None:
                    output_dir = os.path.abspath(media_dir) 
                output_path_txt = os.path.abspath(os.path.join(output_dir, f"{base_name}.txt")) #  Plain text transcription.
                output_path_json = os.path.abspath(os.path.join(output_dir, f"{base_name}.json")) # Detailed JSON transcription.
                try:
                   
                    
                    result = model.transcribe(media_path) # Uses Whisper to transcribe the audio/video file.

                    # Save as text
                    with open(output_path_txt, "w", encoding="utf-8") as f:
                        f.write(result["text"])

                    # Save as JSON
                    with open(output_path_json, "w", encoding="utf-8") as f:
                        json.dump(result, f, indent=4, ensure_ascii=False) 

                    print(f"Transcribed: {media_path}")

                except Exception as e: # Catches errors (e.g., unsupported file format, corrupted media).
                    print(f"Error transcribing {media_path}: {e}")
            elif file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')): # Skips image files.
                print(f"Skipping non-media file: {file}")
            else:
                print(f"Unsupported file type: {file}") # 

if __name__ == "__main__":
    media_directory = input("Enter the directory containing media files: ")
    media_directory = os.path.abspath(media_directory) 
    output_directory = input("Enter the output directory (or press Enter to use the same directory): ")
    if not output_directory:
        output_directory = media_directory 
    else:
        output_directory = os.path.abspath(output_directory) 
    transcribe_media(media_directory, output_directory)
    print("Transcription complete.")
