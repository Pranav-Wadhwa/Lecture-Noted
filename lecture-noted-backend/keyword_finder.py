from rake_nltk import Metric, Rake 
from summa import keywords

import requests
import urllib
import json
import os

import nltk

try:
    from credentials import CREDENTIALS
except:
    CREDENTIALS = os.environ

key = CREDENTIALS["pixabay-api"]

r = Rake(punctuations='“”–’,.!\'', ranking_metric=Metric.WORD_DEGREE, max_length=2)

def get_images(text):
	words = get_keywords(text)
	#print(words)
	images = []
	for word in words:
		image_url = pixabay_images(word)
		if not image_url:
			continue
		images.append({'keyword':word, 'image':image_url})

	return images


def get_keywords(text):
	r.extract_keywords_from_text(text)

	rake_phrases = r.get_ranked_phrases()
	textrank_words = keywords.keywords(text).split('\n')

	final_words = []

	for word in textrank_words:
		if word in rake_phrases:
			final_words.append(word)

	#print(rake_phrases, textrank_words)

	return final_words[0:min(len(final_words), 4)] # consider returning rake_phrases
        
	#return rake_phrases[0:min(len(rake_phrases), 4)]
	
def pixabay_images(search):
	encoded = urllib.parse.urlencode({'q':search})
	url = 'https://pixabay.com/api/?key=%s&%s' % (key, encoded)
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

text = """Climate change includes both global warming driven by human emissions of greenhouse gases and the resulting large-scale shifts in weather patterns. Though there have been previous periods of climatic change, since the mid-20th century humans have had an unprecedented impact on Earth's climate system and caused change on a global scale.[2]

The largest driver of warming is the emission of greenhouse gases, of which more than 90% are carbon dioxide (CO
2) and methane.[3] Fossil fuel burning (coal, oil, and natural gas) for energy consumption is the main source of these emissions, with additional contributions from agriculture, deforestation, and manufacturing.[4] The human cause of climate change is not disputed by any scientific body of national or international standing.[5] Temperature rise is accelerated or tempered by climate feedbacks, such as loss of sunlight-reflecting snow and ice cover, increased water vapour (a greenhouse gas itself), and changes to land and ocean carbon sinks.

Temperature rise on land is about twice the global average increase, leading to desert expansion and more common heat waves and wildfires.[6] Temperature rise is also amplified in the Arctic, where it has contributed to melting permafrost, glacial retreat and sea ice loss.[7] Warmer temperatures are increasing rates of evaporation, causing more intense storms and weather extremes.[8] Impacts on ecosystems include the relocation or extinction of many species as their environment changes, most immediately in coral reefs, mountains, and the Arctic.[9] Climate change threatens people with food insecurity, water scarcity, flooding, infectious diseases, extreme heat, economic losses, and displacement. These impacts have led the World Health Organization to call climate change the greatest threat to global health in the 21st century.[10] Even if efforts to minimize future warming are successful, some effects will continue for centuries, including rising sea levels, rising ocean temperatures, and ocean acidification.[11]"""


# print(get_images(text))
