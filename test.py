import random

class Markov(object):
	
	def __init__(self, stuff):
		self.text = stuff
		
	
	def get_words_top(self):
		data = random.choice(self.text["meme-top"])
		words = data.split()
		return words
		
	
	def get_words_bottom(self):
		data = random.choice(self.text["meme-bottom"])
		words = data.split()
		return words
		
	
	def triples(self, words):
		""" Generates triples from the given data string. So if our string were
				"What a lovely day", we'd generate (What, a, lovely) and then
				(a, lovely, day).
		"""
		
		if len(words) < 3:
			return
		
		for i in range(len(words) - 2):
			yield (words[i], words[i+1], words[i+2])
				
	def generate_markov_text(self):
	    top_words = self.get_words_top()
	    bottom_words = self.get_words_bottom()
	    
        top_seed = random.randint(0, len(top_words))
        bottom_seed = random.randint(0, len(bottom_words))
        top_seed_word, top_next_word = top_words[top_seed], top_words[top_seed+1]
        bottom_seed_word, bottom_next_word = bottom_words[top_seed], bottom_words[bottom_seed+1]
        tw1, tw2 = top_seed_word, top_next_word
        bw1, bw2 = bottom_seed_word, bottom_next_word
        tgen_words = []
        bgen_words = []
        for i in xrange(random.randint(0, 15)):
			tgen_words.append(tw1)
			tw1, tw2 = tw2, random.choice(self.triples(top_words))
        tgen_words.append(tw2)
        for i in xrange(random.randint(0, 15)):
			bgen_words.append(bw1)
			bw1, bw2 = bw2, random.choice(self.triples(bottom_words))
        tgen_words.append(tw2)
        return [' '.join(tgen_words), ' '.join(bgen_words)]
        
