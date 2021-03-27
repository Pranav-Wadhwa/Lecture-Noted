from youtube_transcript_api import YouTubeTranscriptApi
# pip install youtube_transcript_api
# 	https://pypi.org/project/youtube-transcript-api/
#import os
#os.environ["PAFY_BACKEND"] = "internal"
import pafy
# pip install pafy
# 	https://pypi.org/project/pafy/

CHUNK_LENGTH = 300

def get_transcript(video_id):
	raw = YouTubeTranscriptApi.get_transcript(video_id)
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
	url = "https://www.youtube.com/watch?v=%s" % video_crash_course_bool
	video = pafy.new(url)

	obj = {
		'title': video.title,
		'rating': video.rating,
		'viewcount': video.viewcount,
		'author': video.author,
		'duration': video.duration,
		'likes': video.likes,
		'dislikes': video.dislikes,
		'published': video.published,
		'thumbnail': video.thumb,
		# 'description': video.description, # for some reason this throws an error
	}

	return obj


video_coding_adventures = 'bqtqltqcQhw'
video_crash_course_bool = 'gI-qXk7XojA'
video_crash_course_disease = '1PLBmUVYYeg'

# print(get_metadata(video_crash_course_bool))

# trans = get_transcript(video_crash_course_disease)
# print(trans)
