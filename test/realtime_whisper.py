import whisper
import pyaudio
import numpy as np
import threading
import queue

# Whisperモデルのロード
model = whisper.load_model("base")

# 音声入力の設定
CHUNK = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 16000

# 音声データを格納するキュー
audio_queue = queue.Queue()

# 音声認識の結果を格納する変数
transcription = ""

def audio_callback(in_data, frame_count, time_info, status):
    audio_data = np.frombuffer(in_data, dtype=np.float32)
    audio_queue.put(audio_data)
    return (in_data, pyaudio.paContinue)

def process_audio():
    global transcription
    audio_data = np.array([])
    
    while True:
        # キューから音声データを取得
        if not audio_queue.empty():
            audio_data = np.append(audio_data, audio_queue.get())
        
        # 一定量のデータが溜まったら処理
        if len(audio_data) > RATE * 5:  # 5秒分のデータ
            # Whisperで音声認識
            result = model.transcribe(audio_data)
            transcription = result["text"]
            print("認識結果:", transcription)
            
            # 処理済みデータをクリア
            audio_data = np.array([])

# 音声入力のセットアップ
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                stream_callback=audio_callback)

# 音声処理スレッドの開始
processing_thread = threading.Thread(target=process_audio)
processing_thread.start()

print("リアルタイム音声認識を開始します。Ctrl+Cで終了します。")

# メインループ
try:
    while True:
        pass
except KeyboardInterrupt:
    print("音声認識を終了します。")

# クリーンアップ
stream.stop_stream()
stream.close()
p.terminate()
