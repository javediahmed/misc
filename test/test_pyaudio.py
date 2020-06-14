import pyaudio
pyau = pyaudio.PyAudio()
for i in range(pyau.get_device_count()):
  dev = pyau.get_device_info_by_index(i)
  print((i,dev['name'],dev['maxInputChannels']))

breakpoint()
