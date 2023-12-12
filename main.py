# class Movie:
#    def __init__(self, title, mood):
#       self.title = title
#       self.mood = mood

#    def get_choice(self, movie_title):
#       self.movie_title = movie_title

Moviesdict = [{'Title': 'Dogtooth','mood': "sceptical"},
      {'Title':'Eat, Pray, Love', 'mood':'romantic'},
   {'Title':'Joker', 'mood':'depressed'},
    {'Title':'Cruella', 'mood':'powerful'}
]

def MatchMood (inputmood):
   for item in Moviesdict:
    if  inputmood == (item['mood']):
      return (item['Title'])
   return "None"
   
   

# Dogtooth = Movie ("Dogtooth", "sceptical")
# EatPrayLove = Movie("Eat,Pray, Love", "romantic")
# Joker = Movie ("Joker", "depressed")
# Cruella = Movie ("Cruella", "powerful")
# CinemaParadiso = Movie ("Cinema Paradiso", "emotional")
# LaVitaeBella = Movie ("LaVita e Bella", "general")
# Gomorrah = Movie ("Gomorrah", "sadistic")
# Parasites = Movie ("Parasites", "analytical")
# OldBoy    = Movie ("Old Boy", "spicy")
# Elemental = Movie ("Elemental", "childish")


Mood = input('How are you feeling today?')
print(MatchMood(Mood.strip()))