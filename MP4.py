import os
import sys
import shutil
import requests
from pytube import YouTube
import moviepy.editor as mp

CURRENT_VERSION = "1.0.0"
LICENSE_KEYS = ["ATK", "ATK"]  # Replace with your actual license keys

def get_latest_version():
    url = "https://your-server.com/latest_version.txt"  # Replace with your URL
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip()
    return None

def download_update(download_url, output_path):
    response = requests.get(download_url, stream=True)
    with open(output_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

def replace_old_version(new_file_path, old_file_path):
    try:
        shutil.move(new_file_path, old_file_path)
        print("Update applied successfully.")
    except Exception as e:
        print(f"Error applying update: {e}")

def restart_application():
    os.execv(sys.executable, ['python'] + sys.argv)

def is_update_available(current_version):
    latest_version = get_latest_version()
    if latest_version and latest_version > current_version:
        return True
    return False

def auto_update():
    if is_update_available(CURRENT_VERSION):
        print("New version available. Downloading update...")
        download_url = "https://your-server.com/your_new_version.py"  # Replace with your URL
        output_path = "new_version.py"
        download_update(download_url, output_path)
        
        # Replace the old version with the new one
        replace_old_version(output_path, sys.argv[0])
        
        # Restart the application
        print("Restarting application...")
        restart_application()
    else:
        print("No updates available. You're on the latest version.")

def validate_license_key(license_key):
    if license_key in LICENSE_KEYS:
        return True
    else:
        print("Invalid license key. Please contact support.")
        return False

def download_video(video_url, download_type, download_path):
    try:
        yt = YouTube(video_url)
        if download_type == 'mp4':
            stream = yt.streams.get_highest_resolution()
            stream.download(output_path=download_path)
            print(f"Downloaded as MP4: {stream.title}")
        elif download_type == 'mp3':
            stream = yt.streams.filter(only_audio=True).first()
            downloaded_file = stream.download(output_path=download_path)
            base, ext = os.path.splitext(downloaded_file)
            mp3_file = base + '.mp3'
            audio_clip = mp.AudioFileClip(downloaded_file)
            audio_clip.write_audiofile(mp3_file)
            audio_clip.close()
            os.remove(downloaded_file)  # remove the original file
            print(f"Downloaded and converted to MP3: {yt.title}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    auto_update()
    
    license_key = input("Enter your license key: ")
    if not validate_license_key(license_key):
        return
    
    while True:
        video_url = input("Enter the YouTube video URL: ")
        download_type = input("Do you want to download as MP4 or MP3? ").strip().lower()
        
        if download_type not in ['mp4', 'mp3']:
            print("Invalid option. Please choose either 'MP4' or 'MP3'.")
            continue
        
        download_path = os.path.expanduser("~/Downloads")
        download_video(video_url, download_type, download_path)
        
        another = input("Do you want to download another video? (yes/no): ").strip().lower()
        if another != 'yes':
            print("Exiting the program. Thank you for using the downloader!")
            break

if __name__ == "__main__":
    main()
