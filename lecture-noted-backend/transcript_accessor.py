from youtube_transcript_api import YouTubeTranscriptApi
# pip install youtube_transcript_api
#   https://pypi.org/project/youtube-transcript-api/
#import os
#os.environ["PAFY_BACKEND"] = "internal"
import pafy
# pip install pafy
#   https://pypi.org/project/pafy/

import requests
import speech_recognition as sr


CHUNK_LENGTH = 300

def get_mp3_transcript(url, path):
    #print(url)
    response = requests.get(url)
    #print(response)
    with open(path, 'wb') as f:
        f.write(response.content)
        #print(response.content)

    r = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio_text = r.record(source)

        text = r.recognize_google(audio_text, language="en-IN")

        #print(text)

        return text



# returns [(chunk, start_time)]
def get_chunky_transcript(video_id):
    raw = YouTubeTranscriptApi.get_transcript(video_id)
    #try:
    #    raw = YouTubeTranscriptApi.get_transcript(video_id)
    #except:
    #    return None, None
    chunks = []
    times = []
    cur_chunk = ''
    cur_len = 0

    for line in raw:
        text = strip_text(line['text'])

        if cur_len + text.count(' ') > CHUNK_LENGTH:
            chunks.append(cur_chunk)
            cur_len = 0
            cur_chunk = ''

        if cur_len == 0:
            times.append(str(line['start']))

        cur_chunk += text + ' '
        cur_len += text.count(' ')

    # after loop add last bit
    chunks.append(cur_chunk)

    return chunks, times

# depreciated
def get_transcript(video_id):
    try:
        raw = YouTubeTranscriptApi.get_transcript(video_id)
    except:
        return -1
    trans = ''

    for i in raw:
        trans += strip_text(i['text']) + ' '

    return trans

def strip_text(text):
    return text.replace('\n', ' ').replace('\t', ' ')

def chunk(text):
    text = text.split(" ")
    toreturn = []

    for i in range(0, len(text)//CHUNK_LENGTH+1):
        toreturn.append(' '.join(text[i*200:min((i+1)*200, len(text))]))

    return toreturn


def get_metadata(video_id):
    url = "https://www.youtube.com/watch?v=%s" % video_id
    video = pafy.new(url)

    obj = {
        'title': video.title,
        'rating': video.rating,
        'viewcount': video.viewcount,
        'author': video.author,
        'duration': video.duration,
        'likes': video.likes,
        'dislikes': video.dislikes,
        # 'published': video.published,
        # 'thumbnail': video.thumb,
        # 'description': video.description, # for some reason this throws an error
    }

    return obj


video_coding_adventures = 'bqtqltqcQhw'
video_crash_course_bool = 'gI-qXk7XojA'
video_crash_course_disease = '1PLBmUVYYeg'

# print(get_metadata(video_crash_course_bool))

# chunks, times = get_chunky_transcript(video_crash_course_disease)
# print(chunks, times)
