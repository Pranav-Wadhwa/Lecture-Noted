from rake_nltk import Metric, Rake 
from summa import keywords

import requests
import urllib
import json


r = Rake(punctuations='“”–’,.!\'', ranking_metric=Metric.WORD_DEGREE, max_length=2)

def get_images(text):
	words = get_keywords(text)

	images = []
	for i in words:
		images.append(pixabay_images(words))

	return images


def get_keywords(text):
	r.extract_keywords_from_text(text)

	rake_phrases = r.get_ranked_phrases()
	textrank_words = keywords.keywords(text)

	final_words = []

	for word in textrank_words:
		if word in rake_phrases:
			final_words.append(word)

	return word
	
def pixabay_images(search):
	encoded = urllib.parse.urlencode({'q':search})
	url = 'https://pixabay.com/api/?key=20893913-450d8427454318b9dafb155ca&%s' % encoded
	image_json = requests.get(url).text
	image_dict = json.loads(image_json)
	hits = image_dict['hits']
	if len(hits) == 0:
		return None
	else:
		return hits[0]['largeImageURL']


text = '''Hi, I’m Carrie Anne and welcome to Crash Course Computer 
Science! Today we start our journey up the ladder of abstraction, where we 
leave behind the simplicity of being able to see every switch and gear, but 
gain the ability to assemble increasingly complex systems. INTRO Last episode, 
we talked about how computers evolved from electromechanical devices, that 
often had decimal representations of numbers – like those represented by teeth 
on a gear – to electronic computers with transistors that can turn the flow of 
electricity on or off. And fortunately, even with just two states of electricity, 
we can represent important information. We call this representation Binary -- 
which literally means “of two states”, in the same way a bicycle has two wheels 
or a biped has two legs. You might think two states isn’t a lot to work with, 
and you’d be right! But, it’s exactly what you need for representing the values 
“true” and “false”. In computers, an “on” state, when electricity is flowing, 
represents true. The off state, no electricity flowing, represents false. We 
can also write binary as 1’s and 0’s instead of true’s and false’s – they are 
just different expressions of the same signal – but we’ll talk more about that 
in the next episode.'''

text = '''Gravity is a long range attractive force between all objects with mass.
Every massive object attracts every other in the universe.
The strength of gravity decreases by the square of the distance between two objects - 
so if you're twice as far away, gravity is only one fourth as strong!'''

print(get_images(text))