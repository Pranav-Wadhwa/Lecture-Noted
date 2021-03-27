from youtube_transcript_api import YouTubeTranscriptApi
# pip install youtube_transcript_api
# 	https://pypi.org/project/youtube-transcript-api/

def get_transcript(video):
	raw = YouTubeTranscriptApi.get_transcript(video)
	trans = ''

	for i in raw:
		trans += strip_text(i['text']) + ' '

	return trans

def strip_text(text):
	return text.replace('\n', ' ').replace('\t', ' ')


video_coding_adventures = 'bqtqltqcQhw'
video_crash_course_bool = 'gI-qXk7XojA'
video_crash_course_disease = '1PLBmUVYYeg'

trans = get_transcript(video_crash_course_disease)
print(trans)