import datetime
import pyaudio
import time
import audioop

p = pyaudio.PyAudio()
WIDTH = 2
RATE = int(p.get_default_input_device_info()['defaultSampleRate'])
DEVICE = p.get_default_input_device_info()['index']
rms = 1
print(p.get_default_input_device_info())

def callback(in_data, frame_count, time_info, status):
    global rms
    rms = audioop.rms(in_data, WIDTH) / 32767
    return in_data, pyaudio.paContinue

def detectTrigger():
    stream = p.open(format=p.get_format_from_width(WIDTH),
                    input_device_index=DEVICE,
                    channels=1,
                    rate=RATE,
                    input=True,
                    output=False,
                    stream_callback=callback)

    stream.start_stream()
    time.sleep(3)
    print("ready to shoot")
    while stream.is_active():
        if rms>0.5:
            print(datetime.datetime.now())
            print("shot!")
            stream.stop_stream()
    stream.close()
    p.terminate()
    return True
