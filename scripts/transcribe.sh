#!/bin/sh
# Downloads the audio of each TikTok in tiktok-videos-to-transcribe.txt and transcribes it with Whisper (offline).
# Output: transcripts/<videoId>.txt. Skips videos already done, so it is safe to run again.
cd "$(dirname "$0")/.."
mkdir -p transcripts/audio
while read -r url; do
  id=${url##*/}
  [ -s "transcripts/$id.txt" ] && continue
  [ -s "transcripts/audio/$id.m4a" ] || yt-dlp -q -x --audio-format m4a -o "transcripts/audio/%(id)s.%(ext)s" "$url" || { echo "download failed: $id"; continue; }
  whisper "transcripts/audio/$id.m4a" --model small --language en --output_format txt --output_dir transcripts --fp16 False >/dev/null 2>&1 || echo "transcribe failed: $id"
  echo "done: $id"
done < tiktok-videos-to-transcribe.txt
echo "ALL DONE: $(ls transcripts/*.txt | wc -l) transcripts"
