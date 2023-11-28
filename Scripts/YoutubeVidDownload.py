import argparse
from pytube import YouTube


def download_youtube_video(video_url, output_path):
    try:
        yt = YouTube(video_url)
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        if video_stream:
            print(f"Downloading '{yt.title}'...")
            video_stream.download(output_path)
            print(f"Video downloaded successfully as '{yt.title}.mp4' in '{output_path}'")
        else:
            print("No stream available for download.")

    except Exception as e:
        print("An error occurred:", str(e))


def main():
    parser = argparse.ArgumentParser(description='Download YouTube videos as mp4 files')
    parser.add_argument('url', help='URL of the YouTube video')
    parser.add_argument('output_path', help='Path to save the downloaded video')

    args = parser.parse_args()
    download_youtube_video(args.url, args.output_path)


if __name__ == "__main__":
    main()
