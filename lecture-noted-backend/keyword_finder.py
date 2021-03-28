from rake_nltk import Rake 

r = Rake()

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

r.extract_keywords_from_text(text)

print(r.get_ranked_phrases())