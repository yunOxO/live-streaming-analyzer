# 直播流解析

## 🏗 框架结构

```BASH
🏗 框架结构
video_monitor/
│── collector.py        # 采集程序：拉流、切片
│── processor.py        # 后台处理：音视频解析
│── tasks/             
│    ├── video_analyzer.py   # 视频解析逻辑（OCR/物体检测）
│    ├── audio_analyzer.py   # 音频转写逻辑（Whisper/ASR）
│── output/             # 临时存储片段文件
│── results/            # 存储解析结果
```

