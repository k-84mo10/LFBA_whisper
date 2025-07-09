import sounddevice as sd
from scipy.io.wavfile import write

# 設定
duration = 5  # 録音時間（秒）
samplerate = 44100  # サンプリングレート
device_index = 4  # 使用するマイクのインデックス

# 録音
print(f"録音開始（デバイス {device_index}）...")
recording = sd.rec(
    int(duration * samplerate),
    samplerate=samplerate,
    channels=1,
    dtype='int16',
    device=device_index
)
sd.wait()
print("録音終了。保存中...")

# WAVとして保存
write("output.wav", samplerate, recording)

print("保存完了: output.wav")
