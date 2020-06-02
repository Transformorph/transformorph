class Pluralizer:
    def pluralize(phrases, lang_code):
        if lang_code == "deu":
            return Pluralizer._pluralize_deu(phrases)
        elif lang_code == "eng":
            return Pluralizer._pluralize_eng(phrases)
        elif lang_code == "fra":
            return Pluralizer._pluralize_fra(phrases)
        elif lang_code == "nld":
            return Pluralizer._pluralize_nld(phrases)
        else:
            raise TypeError("Not a supported language code for pluralization")

    def _pluralize_deu(phrases):
        new_wrds = []
        for phrase in phrases:
            new_phrase = []
            if phrase in plurals_deutsch:
                new_wrds.append(plurals_deutsch[phrase])
                continue
            for wrd in phrase.split():
                if wrd == "lache":
                    new_phrase.append("lachen")
                elif wrd == "schwimme":
                    new_phrase.append("schwimmen")
                elif wrd == "lächle":
                    new_phrase.append("lächeln")
                elif wrd in plurals_deutsch:
                    new_phrase.append(plurals_deutsch[wrd])
                else:
                    new_phrase.append(wrd)
            # print(phrase)
            new_wrds.append(" ".join(new_phrase))
        return new_wrds

    def _pluralize_fra(phrases):
        new_wrds = []
        for phrase in phrases:
            new_phrase = []
            if phrase in plurals_fra:
                new_wrds.append(plurals_fra[phrase])  # verbs and exceptions
                continue
            if phrase[:2] == "l'":
                phrase = "les " + phrase[2:]
            phrase = phrase.split()
            if phrase[0] == "la" or phrase[0] == "le":  # a noun!
                phrase[0] = "les"
            if phrase[0] == "les":
                if phrase[1][-1] in ["s", "z", "x"]:
                    pass  # no change needed!
                elif phrase[1][-3:] == "eau" or phrase[1][-2:] == "eu":
                    phrase[1] = phrase[1] + "x"
                elif phrase[1][-2:] == "al" or phrase[1][-3:] == "ail":
                    phrase[1] = phrase[1][:-2] + "aux"
                else:
                    phrase[1] = phrase[1] + "s"  # default case
                new_wrds.append(" ".join(phrase))
            else:  # verbs
                for wrd in phrase:
                    if wrd in plurals_fra:
                        new_phrase.append(plurals_fra[wrd])
                    else:
                        new_phrase.append(wrd)
                new_wrds.append(" ".join(new_phrase))
        return new_wrds

    def _pluralize_nld(phrases):
        return phrase

    def _pluralize_eng(phrases):
        phrases, is_verb = phrases  # gosh this is kind of gross isn't it
        new_wrds = []
        for wrd in phrases:
            if wrd in eng_plurals:
                new_wrds.append(eng_plurals[wrd])
            elif wrd.split()[0] == "is":
                new_wrds.append(" ".join(["are"] + wrd.split()[1:]))
            elif is_verb:
                if len(wrd.split()) > 1:
                    new_wrds.append(" ".join([wrd.split()[0][:-1]] + wrd.split()[1:]))
                else:
                    new_wrds.append(wrd[:-1])
            elif wrd[-4:] == "self":
                new_wrds.append("themselves")
            else:
                new_wrds.append(wrd + "s")
        return new_wrds


plurals_deutsch = {
    "der": "die",
    "den": "die",
    "das": "die",
    "die": "die",
    "Autor": "Autoren",
    "Pilot": "Piloten",
    "Chirurg": "Chirurgen",
    "Bauer": "Bauern",
    "Geschäftsführer": "Geschäftsführer",
    "Kunde": "Kunden",
    "Offizier": "Offiziere",
    "Lehrer": "Lehrer",
    "Gesetzgeber": "Gesetzgeber",
    "Berater": "Berater",
    "Wächter": "Wächter",
    "Koch": "Köche",
    "Architekt": "Architekten",
    "Schlittschuhläufer": "Schlittschuhläufer",
    "Tänzer": "Tänzer",
    "Minister": "Minister",
    "Taxifahrer": "Taxifahrer",
    "Assistent": "Assistenten",
    "Vorstand": "Vorstände",
    "Schauspieler": "Schauspieler",
    "Film": "Filme",
    "Buch": "Bücher",
    "Spiel": "Spiele",
    "Lied": "Lieder",
    "Bild": "Bilder",
    "Gemälde": "Gemälde",
    "Roman": "Romane",
    "Gedicht": "Gedichte",
    "Serie": "Serien",
    "lacht": "lachen",
    "schwimmt": "schwimmen",
    "lächelt": "lächeln",
    "ist": "sind",
    "sei": "seien",
    "mag": "mögen",
    "bewundert": "bewundern",
    "hasst": "hassen",
    "liebt": "lieben",
    "macht": "machen",
    "interessiert": "interessieren",
    "Mechaniker": "Mechaniker",
    "Banker": "Banker",
    "rief": "riefen",
    "dachte": "dachten",
    "wusste": "wussten",
    "spricht": "sprechen",
    "sieht": "sehen",
    "spielt": "spielen",
    "schreibt": "schreiben",
    "Bral": "Brale",
    "Kach": "Kächer",
    "Klot": "Kloten",
    "Mur": "Mure",
    "Nuhl": "Nuhle",
    "Pind": "Pinder",
    "Pisch": "Pische",
    "Pund": "Punde",
    "Raun": "Raunen",
    "Spand": "Spande",
    "Spert": "Sperte",
    "Vag": "Vagen",
    "Bnaupf": "Bnaupfen",
    "Bneik": "Bneike",
    "Bnöhk": "Bnöhke",
    "Fnahf": "Fnahfen",
    "Fneik": "Fneiken",
    "Fnöhk": "Fnöhke",
    "Plaupf": "Plaupfen",
    "Pleik": "Pleiken",
    "Pläk": "Pläke",
    "Pnähf": "Pnähfe",
    "Pröng": "Prönge",
    "Snauk": "Snauken",
    "Autorin": "Autorinnen",
    "Pilotin": "Pilotinnen",
    "Chirurgin": "Chirurginnen",
    "Bäuerin": "Bäuerinnen",
    "Geschäftsführerin": "Geschäftsführerinnen",
    "Kundin": "Kundinnen",
    "Offizierin": "Offizierinnen",
    "Lehrerin": "Lehrerinnen",
    "Gesetzgeberin": "Gesetzgeberinnen",
    "Beraterin": "Beraterinnen",
    "Wächterin": "Wächterinnen",
    "Köchin": "Köchinnen",
    "Architektin": "Architektinnen",
    "Schlittschuhläuferin": "Schlittschuhläuferinnen",
    "Tänzerin": "Tänzerinnen",
    "Ministerin": "Ministerinnen",
    "Taxifahrerin": "Taxifahrerinnen",
    "Assistentin": "Assistentinnen",
    "Vorsitzende": "Vorsitzende",
    "Vorsitzender": "Vorsitzende",
    "schätzt": "schätzen",
    "kennt": "kennen",
    "Schauspielerin": "Schauspielerinnen",
    "Serie": "Serien",
    "Zeitung": "Zeitungen",
    "Spielfigur": "Spielfiguren",
    "Kamera": "Kameras",
    "Symphonie": "Symphonien",
    "Farbe": "Farben",
    "Leinwand": "Leinwände",
    "Seite": "Seiten",
    "Dichtung": "Dichtungen",
    "Text": "Texte",
    "Spielwürfel": "Spielwürfel",
    "Gesang": "Gesänge",
    "Stift": "Stifte",
    "Rahmen": "Rahmen",
    "Roman": "Romane",
    "Vers": "Verse",
    "Fernseher": "Fehrnseher",
    "Kaninchen": "Kaninchen",
    "Stinktier": "Stinktiere",
    "Mammut": "Mammuts",
    "Lama": "Lamas",
    "Reh": "Rehe",
    "Rentier": "Rentiere",
    "Känguru": "Kängurus",
    "Krokodil": "Krokodile",
    "Schwein": "Schweine",
    "Pferd": "Pferde",
    "Stachelschwein": "Stachelschweine",
    "Meerschweinchen": "Meerschweinchen",
    "Schaf": "Schafe",
    "Huhn": "Hühner",
    "Einhorn": "Einhörner",
    "Eichhörnchen": "Eichhörnchen",
    "Chamäleon": "Chamäleons",
    "Kamel": "Kamele",
    "Wiesel": "Wiesel",
    "Murmeltier": "Murmeltiere",
    "dem Stachelschwein": "den Stachelschweinen",
    "dem Meerschweinchen": "den Meerschweinchen",
    "dem Schaf": "den Schafen",
    "dem Huhn": "den Hühnern",
    "dem Einhorn": "den Einhörnern",
    "dem Eichhörnchen": "den Eichhörnchen",
    "dem Chamäleon": "den Chamäleons",
    "dem Kamel": "den Kamelen",
    "dem Wiesel": "den Wieseln",  # TODO: check
    "dem Murmeltier": "den Murmeltieren",
    "Seepferdchen": "Seepferdchen",
    "Nilpferd": "Nilpferde",
    "Walross": "Walrosse",
    "Zebra": "Zebras",
    "läuft": "laufen",
    "singt": "singen",
    "Kinderbuch": "Kinderbücher",
    "Program": "Programme",
    "der Wächterin": "den Wächterinnen",
    "der Köchin": "den Köchinnen",
    "der Architektin": "den Architektinnen",
    "der Schlittschuhläuferin": "den Schlittschuhläuferinnen",
    "der Tänzerin": "den Tänzerinnen",
    "der Ministerin": "den Ministerinnen",
    "der Taxifahrerin": "den Taxifaherinnen",
    "der Assistentin": "den Assistentinnen",
    "der Vorsitzenden": "den Vorsitzenden",
    "der Schauspielerin": "den Schauspielerinnen",
    "dem Wächter": "den Wächtern",
    "dem Koch": "den Köchen",
    "dem Architekten": "den Architekten",
    "dem Schlittschuhläufer": "den Schlittschuhläufern",
    "dem Tänzer": "den Tänzern",
    "dem Minister": "den Ministern",
    "dem Taxifahrer": "den Taxifahrern",
    "dem Assistenten": "den Assistenten",
    "dem Vorsitzender": "den Vorsitzenden",
    "dem Schauspieler": "den Schauspielern",
}

eng_plurals = {
    "tor": "tors",
    "gutch": "gutches",
    "lun": "luns",
    "niz": "nizzes",
    "cra": "cras",
    "heaf": "heafs",
    "zib": "zibs",
    "bik": "biks",
    "tass": "tasses",
    "spow": "spows",
    "naz": "nazzes",
    "bod": "bods",
    "tas": "tasses",
}

plurals_fra = {
    "disait": "disaient",
    "pensait": "pensaient",
    "savait": "savaient",
    "parle": "parlent",
    "aime": "aiment",
    "apprécie": "apprécient",
    "connaît": "connaissent",
    "sert": "servent",
    "a": "ont",
    "écrit": "écrivent",
    "bon": "bons",
    "grand": "grands",
    "jeune": "jeunes",
    "petit": "petits",
    "court": "courent",
    "chante": "chantent",
    "joue": "jouent",
    "grande": "grandes",
    "vieille": "vielles",
    "petite": "petites",
    "est": "sont",
    "rit": "rient",
    "nouveau": "nouveaux",
    "populaire": "populaires",
    "impopulaire": "impopulaires",
    "rend": "rendent",
    "intéresse": "intéressent",
    "n'est": "ne sont",
    "bonne": "bonnes",
    "mauvaise": "mauvaises",
    "nouvelle": "nouvelles",
}
