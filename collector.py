import cv2
import time
import os
import queue
import threading
from datetime import datetime
from logger import logger

segment_time = 10  # 每段10秒
url = "https://pull-m1.wxlivecdn.com/trtc_1400419933/orig_2042823482672149837_jf430.flv?cdntagname=jf430&combuf=n%2BCgfRQjJKy%2FvcQGzbe%2FRR0GHBf0dcidw2y8nQcNRpMMWOqU%2FHL8ieu2ILHuC81dbM21EmdNWltLS7efYRiyqtBEoUmVCxXE3f2TAZrpjxoXFEv5kNtW8p7kz7o6OlL7%2B28q%2B4wI4UVeWXgiTwDVqVKhWCvAE1OSEV0lqd1i3nFRGAIMBHqdvS2b2lQSqD1RrcBwX6scfsq6QIFP92Jf5tufS%2FM5ysCSMoH8JBpv&expt=&extbuf=l1WjKdnb%2BuAm4AscRnRAP2s983mRHDuWW25jBcqimYk6A7mgcJ6KAW3MB8JEcktFdUQSCwRHOjnk7ZQPH3YMXayB0XycV104FKfnkM1npuYtHkzjUDzIYSjN3sbpStXQH9PWRqrpYQOwELHgT1rTJvxCAyXCYcVS%2BsiBTil2%2BA9WCfYX9zA6houMo%2F0exGcdO%2F8X5vQ7pwNu8w%3D%3D&gid=0&openid=2C70997CA5CE67265EAF940638A26769&q=4&sc=4&sv=2&txSecret=60a8d3b17a2250c5ef816cfc457c2530&txTime=68BA3CD1&vcodec=1&wu=1&wxns=1&wxtoken=e70e702cef8c9eb5f13d48412eff4242"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# 简单队列（可替换为 Redis / Kafka）
task_queue = queue.Queue()

def collect_stream():
    cap = cv2.VideoCapture(url)
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 25
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    out = None
    start_time = time.time()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            logger.error('视频流结束或读取失败。')
            break

        if out is None:
            # 用当前时间命名文件：20250903_173025.mp4
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(output_dir, f"segment_{timestamp}.mp4")
            out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
            start_time = time.time()

        out.write(frame)

        if time.time() - start_time >= segment_time:
            out.release()
            logger.info(f"[Collector] Saved {filename}")
            task_queue.put(filename)   # 投递到队列
            out = None

    cap.release()

if __name__ == "__main__":
    threading.Thread(target=collect_stream).start()