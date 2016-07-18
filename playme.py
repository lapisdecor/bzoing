import pyaudio
import wave
import time
import sys

class Playme():
    def __init__(self):
        self.wf = wave.open("alarm-clock-elapsed.wav", 'rb')

    def play(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(self.wf.getsampwidth()),
                    channels=self.wf.getnchannels(),
                    rate=self.wf.getframerate(),
                    output=True,
                    stream_callback=self.callback)

        stream.start_stream()

        while stream.is_active():
            time.sleep(0.1)

        stream.stop_stream()
        stream.close()
        self.wf.close()

        p.terminate()


    def callback(self, in_data, frame_count, time_info, status):
        data = self.wf.readframes(frame_count)
        return (data, pyaudio.paContinue)
