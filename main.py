import streamlit as st
import pyaudio
import wave
import pyrebase
import requests
from firebase_admin import credentials, initialize_app, storage

def stt(api_key, audio_file_path):
    url = "https://studio.mohir.ai/api/v1/stt"

    headers = {
        "Authorization": api_key
    }

    files = {
        "file": (audio_file_path, open(audio_file_path, "rb"))
    }

    try:
        response = requests.post(url, headers=headers, files=files)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()['result']['text']
    except Exception as e:
        print(f"Error occurred during STT: {e}")
        return None

#firebasega ulanish
config = {
  "apiKey": "AIzaSyAXsdkGflC9PT9y6id8PvJ0qZexzmiVj_I",
  "authDomain": "iotproject-f6380.firebaseapp.com",
  "databaseURL": "https://iotproject-f6380-default-rtdb.firebaseio.com/",
  "projectId": "iotproject-f6380",
  "storageBucket": "iotproject-f6380.appspot.com",
  "seriveAccount":"ServiceAccount.json"

}
firebase = pyrebase.initialize_app(config)
database = firebase.database()

def record_audio(file_path, duration=5, sample_rate=44100, chunk=1024, channels=2, format=pyaudio.paInt16):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=format,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk)

    st.write("Yozilmoqda...")
    frames = []
    for i in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    st.write("Yozib olindi!")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(file_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(format))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

st.title("ovozli boshqaruv!")

duration = st.sidebar.slider("Ovoz yozish vaqti", 1, 10, 3)
file_path = "voice.wav"

if st.button("Ovozni yuborish"):
        record_audio(file_path, duration=duration)
        st.audio(file_path, format='audio/wav')
        t = stt(api_key="48d50009-2fd8-4c53-a3ae-6c71951cef55:79b36c75-ebd3-4c33-96d8-3241f388e2a3", audio_file_path=file_path)
        st.success("model ishlashi tugatildi tugallandi:")
        st.write(t.replace("'",""))
        database.child("text").set(t.replace("'",""))

