import whisper
import pyaudio
import numpy as np
import threading
import queue
import resampy  # ← pip install resampy が必要

# Whisperモデルのロード
model = whisper.load_model("base")

# 音声入力の設定
CHUNK = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 1
INPUT_RATE = 48000  # ← USB MIC の実サンプルレート
TARGET_RATE = 16000  # ← Whisperが期待するレート

# 音声データを格納するキュー
audio_queue = queue.Queue()

def audio_callback(in_data, frame_count, time_info, status):
    audio_data = np.frombuffer(in_data, dtype=np.float32)
    audio_queue.put(audio_data)
    return (in_data, pyaudio.paContinue)

def process_audio():
    audio_data = np.array([], dtype=np.float32)
    
    while True:
        if not audio_queue.empty():
            audio_data = np.append(audio_data, audio_queue.get())
        
        if len(audio_data) > INPUT_RATE * 5:  # 5秒分
            print("解析開始")
            # リサンプリング
            audio_16k = resampy.resample(audio_data, sr_orig=INPUT_RATE, sr_new=TARGET_RATE)
            audio_16k = audio_16k.astype(np.float32)

            # Whisperで認識
            result = model.transcribe(audio_16k)
            print("認識結果:", result["text"])
            
            audio_data = np.array([], dtype=np.float32)

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=INPUT_RATE,  # ← USB MICが対応しているレート
                input=True,
                input_device_index=4,
                frames_per_buffer=CHUNK,
                stream_callback=audio_callback)

threading.Thread(target=process_audio, daemon=True).start()
print("リアルタイム音声認識を開始します。Ctrl+Cで終了します。")

try:
    while True:
        pass
except KeyboardInterrupt:
    print("音声認識を終了します。")
    stream.stop_stream()
    stream.close()
    p.terminate()
