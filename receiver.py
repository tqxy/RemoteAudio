import pyaudio
import socket

# 配置参数
CHUNK = 1024
FORMAT = pyaudio.paInt16  # 16位PCM格式
CHANNELS = 2              # 立体声
RATE = 44100              # 采样率
UDP_IP = "0.0.0.0"       # 监听所有网络接口
UDP_PORT = 5005           # 与发送端端口保持一致

# 初始化音频流（输出模式）
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

# 创建UDP套接字并绑定端口
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("开始接收音频数据，按Ctrl+C停止...")
try:
    while True:
        data, addr = sock.recvfrom(CHUNK * 2 * 2)  # 匹配发送端数据大小（2声道*16位=4字节/采样点，CHUNK个采样点）
        stream.write(data)  # 播放接收到的音频数据
except KeyboardInterrupt:
    pass

# 释放资源
stream.stop_stream()
stream.close()
p.terminate()
sock.close()
print("已停止接收并释放资源")