import pyaudio
import socket

# 配置参数
CHUNK = 1024
FORMAT = pyaudio.paInt16  # 16位PCM格式
CHANNELS = 2              # 立体声
RATE = 44100              # 采样率
UDP_IP = "192.168.124.5"
UDP_PORT = 5005

# 初始化音频流并检测系统音频捕获设备
p = pyaudio.PyAudio()

# 查找系统音频捕获设备（如Windows的立体声混音）
device_index = None
for i in range(p.get_device_count()):
    dev_info = p.get_device_info_by_index(i)
    print(f"设备 {i}: {dev_info['name']}")
    if 'Stereo Mix' in dev_info['name'] or '立体声混音' in dev_info['name'] or '系统音频' in dev_info['name']:  # 匹配常见系统音频设备名称（如Stereo Mix/立体声混音）
        device_index = i
        break
if device_index is None:
    raise RuntimeError("未找到系统音频捕获设备，请检查是否启用立体声混音或相关音频接口")

# 打开指定设备的输入流
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=CHUNK)

# 创建UDP套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        data = stream.read(CHUNK)  # 读取音频数据
        sock.sendto(data, (UDP_IP, UDP_PORT))  # 发送数据
except KeyboardInterrupt:
    pass

# 释放资源
stream.stop_stream()
stream.close()
p.terminate()
sock.close()