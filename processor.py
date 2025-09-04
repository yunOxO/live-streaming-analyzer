import os
import subprocess
import queue
import time
import whisper
from datetime import datetime
from tasks.video_analyzer import analyze_video
from tasks.audio_analyzer import analyze_text
from collector import task_queue

results_dir = "results"
os.makedirs(results_dir, exist_ok=True)

model = whisper.load_model("base")


def extract_audio(video_file, audio_file):
    cmd = [
        'ffmpeg', '-y',
        '-i', video_file,
        '-vn', '-acodec', 'pcm_s16le',
        '-ar', '16000', '-ac', '1',
        audio_file
    ]
    subprocess.run(cmd, check=True)


def process_task(video_file):
    print(f"[Processor] Processing {video_file}")
    base_name = os.path.splitext(os.path.basename(video_file))[0]

    # 1. 提取音频，保持同样的时间戳命名
    audio_file = os.path.join("output", f"{base_name}.wav")
    extract_audio(video_file, audio_file)

    # 2. 音频识别
    result = model.transcribe(audio_file, language="zh")
    text = result["text"]

    # 3. 视频解析
    video_result = analyze_video(video_file)

    # 4. 文本敏感词检测
    audio_analysis = analyze_text(text)

    # 5. 保存结果，加上相同时间戳
    result_file = os.path.join(results_dir, f"{base_name}.json")
    with open(result_file, "w", encoding="utf-8") as f:
        f.write(str({
            "timestamp": base_name.replace("segment_", ""),
            "video": video_result,
            "audio_text": text,
            "audio_analysis": audio_analysis
        }))

    print(f"[Processor] Finished {video_file}")
    os.remove(video_file)
    os.remove(audio_file)

if __name__ == "__main__":
    while True:
        try:
            video_file = task_queue.get(timeout=5)
            process_task(video_file)
        except queue.Empty:
            time.sleep(1)