import cv2

def analyze_video(video_file):
    cap = cv2.VideoCapture(video_file)
    frame_count = 0
    result = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        if frame_count % 30 == 0:   # 间隔30帧处理一次
            result.append(f"Frame {frame_count} analyzed")
    cap.release()

    return result