import pysrt 
from translate import Translator


def translate_text(text, to_lang,from_lang):
	translate = Translator(to_lang=to_lang , from_lang=from_lang)
	text = translate.translate(text)
	return text 

def subtrans(file_name,from_lang,to_lang,output_name):

	subs = pysrt.open(file_name)

	for sub in subs:
		sub.text = translate_text(sub.text,to_lang=to_lang,from_lang=from_lang)

	subs.save(output_name)