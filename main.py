from random import choice

#Creating a list of fav movies
movies = [['Eat, Pray, Love', 'Joker', 'Cruella'], 
          ['Cinema Paradiso', 'La Vita e Bella','Gomorrah'],
           ['Dogtooth', 'Parasites', 'Old Boy'] ]

#input mood
print('What mood are you in?')
mood = input()

#loop through and find a matching mood

for item in movies:
    if item[1] == mood:
        print(mood + 'movie: ' + item[0])
