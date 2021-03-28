import openai
import os

try:
    from credentials import CREDENTIALS
except:
    CREDENTIALS = os.environ

# returns a list of strings, returns None if failed
def summarize(text):
	chat_log = f'''I was listening to a lecture with the following text:
	"""
	{text}
	"""
	I summarized this text into a couple of bullet points that were easily understandable:

	1.

	'''
	prompt = chat_log
	response = completion.create(
		prompt=prompt, engine="davinci", temperature=0.7,
		top_p=1, frequency_penalty=0, presence_penalty=0.1, best_of=1,
		max_tokens=80)
	answer = response.choices[0].text.strip()
	#print('raw:', answer, '\n')
	answer = process_text(answer)
	return answer

def process_text(text):
	points = []
	# first is usually just the line up to the next number
	cur_point = 1
	cur_str = f'{cur_point + 1}.'
	while cur_str in text:
		ind = text.index(f'{cur_point + 1}.')
		point = text[:ind].strip()
		text = text[ind + len(cur_str):]

		if(len(point)==0):
                    continue
		point = clean_point(point)
		points.append(point)

		cur_point += 1
		cur_str = f'{cur_point + 1}.'

	if len(points) == 0:
		return None
	return points

def clean_point(text):
        if text[0] == '-' or text[0] == '*':
            text = text[1:].strip()
        text = text.replace('\t', '')
        return text

#####
# Testing
#####

def ask(question, chat_log=None):
	if chat_log is None:
		chat_log = '''Human: Hello, how are you?
		AI: I am doing great. How can I help you today?
		'''
	prompt = f'{chat_log}Human: {question}\nAI:'
	response = completion.create(
		prompt=prompt, engine="davinci", stop=['\nHuman'], temperature=0.9,
		top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
		max_tokens=150)
	answer = response.choices[0].text.strip()
	return answer

def start_chat():
	start_chat_log = '''Human: Hello, how are you?
	AI: I am doing great. How can I help you today?
	'''

	inp = ''
	while inp != '-1':
		print(start_chat_log)
		inp = input('Input (-1 to quit): ')
		if inp == '-1':
			break
		a = ask(inp, start_chat_log)
		# update log
		start_chat_log = f'{start_chat_log}Human: {inp}\nAI: {a}\n'

openai.organization = CREDENTIALS['open-ai-organization-id']
openai.api_key = CREDENTIALS['open-ai-api-key']
completion = openai.Completion()

sample_text = '''Hi, I’m Carrie Anne and welcome to Crash Course Computer 
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

#print(summarize(sample_text))

sample_response = '''Binary is a way to represent true and false using electricity.

	2.

	1’s and 0’s can be used to represent true and false.

	3.

	1’s and 0’s can be used to represent true and false.


	In the end, I thought this was a good representation of what she said.

	Later on, I wanted to remember all the important points, so I took out my notebook '''

# print(clean_text(sample_response))
