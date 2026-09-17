import random

from .state import used_usernames

ADJECTIVES = [
    "Jasny", "Ciemny", "Duzy", "Maly", "Szybki", "Wolny", "Glosny", "Cichy",
    "Wesoly", "Smutny", "Zloty", "Srebrny", "Dziki", "Spokojny", "Sprytny",
    "Leniwy", "Odwazny", "Tajemniczy", "Kolorowy", "Zwiny", "Puchaty", "Ostry",
    "Chytry", "Grubasny", "Chudy", "Zmeczony", "Radosny", "Straszny", "Slodki",
    "Kwasny", "Lodowaty", "Ognisty", "Wietrzny", "Deszczowy", "Sloneczny",
    "Ksiezycowy", "Gwiezdny", "Podniebny", "Podziemny", "Magiczny", "Niewidzialny",
    "Elegancki", "Niezniszczalny", "Legendarny", "Epicki", "Fenomenalny",
    "Turbo", "Super", "Mega", "Hiper", "Ultra",
]

NOUNS = [
    "Mis", "Kocur", "Piesek", "Lisek", "Wilk", "Orzel", "Sowa", "Zaba",
    "Krokodyl", "Slon", "Zyrafa", "Hipopotam", "Nosorozec", "Panda", "Koala",
    "Kangur", "Pingwin", "Delfin", "Rekin", "Wielorybik", "Waz", "Jaszczurka",
    "Zolw", "Bobr", "Wydra", "Jenot", "Borsuk", "Jez", "Kret", "Mysz",
    "Chomik", "Krolik", "Skunks", "Puma", "Tygrys", "Lampart", "Gepard",
    "Smok", "Jednorozec", "Feniks", "Goblin", "Trol", "Krasnal", "Rycerz",
    "Wojownik", "Czarodziej", "Pirat", "Ninja", "Samuraj", "Kosmita",
]

def generate_username() -> str:
    base = random.choice(ADJECTIVES) + random.choice(NOUNS)

    if base not in used_usernames:
        used_usernames.add(base)
        return base

    number = random.randint(1, 99)
    candidate = f"{base}{number}"
    while candidate in used_usernames:
        number = random.randint(1, 99)
        candidate = f"{base}{number}"

    used_usernames.add(candidate)
    return candidate
