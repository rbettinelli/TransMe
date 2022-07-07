# ------------------------------------------------------------------------
# R.Bettinelli - Python Script for Transcribing From MP4 Video To Text.
# ------------------------------------------------------------------------
# 07/07/2022 - Framework Version #1 - Get MP4 into WAV and TransScribe.
# ------------------------------------------------------------------------

import os
import sys
import pydub
from moviepy.video.io.VideoFileClip import VideoFileClip
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
from progress.bar import Bar


# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path):
    print("==> File Audio wav to Audio Chunks based on voice")
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)
    # split audio sound where silence is 700 milliseconds or more and get chunks
    chunks = split_on_silence(sound,
                              # experiment with this value for your target audio file
                              min_silence_len=500,
                              # adjust this per requirement
                              silence_thresh=sound.dBFS - 14,
                              # keep the silence for 1 second, adjustable as well
                              keep_silence=500,
                              )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    print("==> File voice Chunking..")
    x = 0
    lc = len(chunks)
    bar = Bar('Processing', max=lc)
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                # print("", end='')
                bar.next()
            else:
                text = f"{text.capitalize()}. "
                pc = (x / lc) * 100
                percentage = f"{pc:.0%}"
                # print(percentage, end='\r')
                bar.next()
                whole_text += text
    # return the text for all chunks detected
        x += 1
    bar.finish()
    return whole_text


# Main Routine.
if __name__ == '__main__':
    print(f"=================================")
    print(f"==> Transcribe Script - rb - 2022")
    print(f"=================================")
    print(f"==> Arguments count: {len(sys.argv)}")
    fln = sys.argv[1]

    # mp4 to mp3
    print("==> File Video mp4 To Audio mp3")
    video = VideoFileClip(fln + ".mp4")
    audio = video.audio
    audio.write_audiofile(fln + ".mp3")

    # Ensure ffmpeg Available and on the path.
    stf = r"C:\ffmpeg\ffmpeg.exe"
    pydub.AudioSegment.ffmpeg = stf
    pydub.AudioSegment.converter = stf

    # mp3 to wav
    print("==> File Audio mp4 To Audio wav")
    sound1 = pydub.AudioSegment.from_mp3(fln + ".mp3")
    sound1.export(fln + ".wav", format="wav")

    # Transcribe Functions.
    r = sr.Recognizer()
    myPath = fln + ".wav"
    output = get_large_audio_transcription(myPath)
    # Write output File
    print("==> File output...")
    with open(fln + '.txt', 'w') as f:
        f.write(output)

    print("==> Cleaning up...")
    os.remove(fln + ".wav")
    os.remove(fln + ".mp3")
