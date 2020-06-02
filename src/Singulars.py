class Singularizer:
    def singularize(phrases, lang_code):
        if lang_code == "deu":
            return Singularizer._singularize_deu(phrases)
        elif lang_code == "eng":
            return Singularizer._singularize_eng(phrases)
        elif lang_code == "fra":
            return Singularizer._singularize_fra(phrases)
        elif lang_code == "nld":
            return Singularizer._singularize_nld(phrases)
        else:
            raise TypeError("Not a supported language code for singularization")

    def _singularize_deu(phrases):
        new_wrds = []
        for phrase in phrases:
            new_phrase = []
            if phrase in sings_deutsch:
                new_wrds.append(sings_deutsch[phrase])
                continue
            for wrd in phrase.split():
                if wrd in sings_deutsch:
                    new_phrase.append(sings_deutsch[wrd])
                else:
                    new_phrase.append(wrd)
            new_wrds.append(" ".join(new_phrase))
        return new_wrds

    def _singularize_fra(phrases):
        new_wrds = []
        for phrase in phrases:
            new_phrase = []
            if phrase in sings_fra:
                new_wrds.append(sings_fra[phrase])
                continue
            if phrase[:8] == "ne sont ":
                phrase = "n'est " + phrase[8:]
            for wrd in phrase.split():
                if wrd in sings_fra:
                    new_phrase.append(sings_fra[wrd])
                else:
                    new_phrase.append(wrd)
            new_wrds.append(" ".join(new_phrase))
        # if phrases[0][-4:] == "lles":
        #     print(new_wrds)
        return new_wrds

    def _singularize_nld(phrases):
        return phrase

    def _singularize_eng(phrases):
        new_wrds = []
        for wrd in phrases:
            if wrd in eng_plurals:
                new_wrds.append(eng_plurals[wrd])
            elif "tasses" in wrd.split():
                new_wrds.append("tass tas")
            elif wrd.split()[0] == "are":
                new_wrds.append(" ".join(["is"] + wrd.split()[1:]))
            elif wrd[-6:] == "selves":
                new_wrds.append("themself")
            elif not len(wrd.split()) > 1 and wrd[-1] == "s":
                new_wrds.append(wrd[:-1])
            else:
                if len(wrd.split()) > 1:
                    new_wrds.append(" ".join([wrd.split()[0] + "s"] + wrd.split()[1:]))
                else:
                    new_wrds.append(wrd + "s")
        return new_wrds


sings_deutsch = {
    "Autoren": "Autor",
    "Piloten": "Pilot",
    "Chirurgen": "Chirurg",
    "Bauern": "Bauer",
    "Geschäftsführer": "Geschäftsführer",
    "Kunden": "Kunde",
    "Offiziere": "Offizier",
    "Lehrer": "Lehrer",
    "Gesetzgeber": "Gesetzgeber",
    "Berater": "Berater",
    "Wächter": "Wächter",
    "Köche": "Koche",
    "Architekten": "Architekt",
    "Schlittschuhläufer": "Schlittschuhläufer",
    "Tänzer": "Tänzer",
    "Minister": "Minister",
    "Taxifahrer": "Taxifahrer",
    "Assistenten": "Assistent",
    "Vorstände": "Vorstand",
    "Schauspieler": "Schauspieler",
    "Filme": "Film",
    "Bücher": "Buch",
    "Spiele": "Spiel",
    "Lieder": "Lied",
    "Bilder": "Bild",
    "Gemälde": "Gemälde",
    "Roman": "Romane",
    "Gedichte": "Gedicht",
    "Serien": "Serie",
    "lachen": "lacht",
    "sind": "ist",
    "seien": "sei",
    "mögen": "mag",
    "lieben": "liebt",
    "machen": "macht",
    "interessieren": "interessiert",
    "Mechaniker": "Mechaniker",
    "Banker": "Banker",
    "riefen": "rief",
    "dachten": "dachte",
    "sprechen": "spricht",
    "sehen": "sieht",
    "spielen": "spielt",
    "schreiben": "schreibt",
    "Brale": "Bral",
    "Kächer": "Kach",
    "Kloten": "Klot",
    "Mure": "Mur",
    "Nuhle": "Nuhl",
    "Pinder": "Pind",
    "Pische": "Pisch",
    "Punde": "Pund",
    "Raunen": "Raun",
    "Spande": "Spand",
    "Sperte": "Spert",
    "Vagen": "Vag",
    "Bnaupfen": "Bnaupf",
    "Bneike": "Bneik",
    "Bnöhke": "Bnöhk",
    "Fnahfen": "Fnahf",
    "Fneiken": "Fneik",
    "Fnöhke": "Fnöhk",
    "Plaupfen": "Plaupf",
    "Pleiken": "Pleik",
    "Pläke": "Pläk",
    "Pnähfe": "Pnähf",
    "Prönge": "Pröng",
    "Snauken": "Snauken",
    "Autorinnen": "Autorin",
    "Pilotinnen": "Pilotin",
    "Chirurginnen": "Chirurgin",
    "Bäuerinnen": "Bäuerin",
    "Geschäftsführerinnen": "Geschäftsführerin",
    "Kundinnen": "Kundin",
    "Offizierinnen": "Offizierin",
    "Lehrerinnen": "Lehrerin",
    "Gesetzgeberinnen": "Gesetzgeberin",
    "Beraterinnen": "Beraterin",
    "Wächterinnen": "Wächterin",
    "Köchinnen": "Köchin",
    "Architektinnen": "Architektin",
    "Schlittschuhläuferinnen": "Schlittschuhläuferin",
    "Tänzerinnen": "Tänzerin",
    "Ministerinnen": "Ministerin",
    "Taxifahrerinnen": "Taxifahrerin",
    "Assistentinnen": "Assistentin",
    "Vorsitzende": "Vorsitzender",
    "Schauspielerinnen": "Schauspielerin",
    "Serien": "Serie",
    "Zeitungen": "Zeitung",
    "Spielfiguren": "Spielfigur",
    "Kameras": "Kamera",
    "Symphonien": "Symphonie",
    "Farben": "Farben",
    "Leinwände": "Leinwand",
    "Seiten": "Seite",
    "Dichtungen": "Dichtung",
    "Texte": "Text",
    "Spielwürfel": "Spielwürfel",
    "Gesänge": "Gesang",
    "Stifte": "Stift",
    "Rahmen": "Rahmen",
    "Romane": "Romane",
    "Verse": "Verse",
    "Fernseher": "Fehrnseher",
    "Kaninchen": "Kaninchen",
    "Stinktiere": "Stinktier",
    "Mammuts": "Mammut",
    "Lamas": "Lama",
    "Rehe": "Reh",
    "Rentiere": "Rentier",
    "Kängurus": "Känguru",
    "Krokodile": "Krokodile",
    "Schweine": "Schwein",
    "Pferde": "Pferd",
    "Stachelschweine": "Stachelschwein",
    "Meerschweinchen": "Meerschweinchen",
    "Schafe": "Schaf",
    "Hühner": "Huhn",
    "Einhörner": "Einhörn",
    "Eichhörnchen": "Eichhörnchen",
    "Chamäleons": "Chamäleon",
    "Kamele": "Kamel",
    "Wiesel": "Wiesel",
    "Murmeltiere": "Murmeltier",
    "Stachelschweinnen": "Stachelschwein",
    "Meerschweinchen": "Meerschweinchen",
    "Schafen": "Schaf",
    "Hühnern": "Huhn",
    "Einhörnern": "Einhorn",
    "Eichhörnchen": "Eichhörnchen",
    "Chamäleons": "Chamäleon",
    "Kamelen": "Kamel",
    "Wieseln": "Wiesel",
    "Murmeltieren": "Murmeltier",
    "Seepferdchen": "Seepferdchen",
    "Nilpferde": "Nilpferd",
    "Walrosse": "Walross",
    "Zebras": "Zebra",
    "laufen": "läuft",
    "singen": "singt",
    "kennen": "kennt",
    "schätzen": "schätzt",
    "Kinderbücher": "Kinderbuch",
    "Programme": "Program",
    "Vorsitzenden": "Vorsitzenden",
    "Wächtern": "Wächter",
    "Koch": "den Köchen",
    "Schlittschuhläufern": "Schlittschuhläufer",
    "Tänzern": "Tänzer",
    "Ministern": "Minister",
    "Taxifahrern": "Taxifahrer",
    "Assistenten": "Assistenten",
    "Vorsitzenden": "Vorsitzender",
    "Schauspielern": "Schauspieler",
}

eng_plurals = {
    "tors": "tor",
    "gutches": "gutch",
    "luns": "lun",
    "nizzes": "niz",
    "cras": "cra",
    "heafs": "heaf",
    "zibs": "zib",
    "biks": "bik",
    "spows": "spow",
    "nazzes": "naz",
    "bods": "bod",
}

# unfortunately we need to list out nouns to restore their genderss
sings_fra = {
    "disaient": "disait",
    "pensaient": "pensait",
    "savaient": "savait",
    "parlent": "parle",
    "aiment": "aime",
    "apprécient": "apprécie",
    "connaissent": "connaît",
    "servent": "sert",
    "ont": "a",
    "écrivent": "écrit",
    "bons": "bon",
    "grands": "grand",
    "jeunes": "jeune",
    "petits": "petit",
    "courent": "court",
    "chantent": "chante",
    "jouent": "joue",
    "grandes": "grande",
    "vielles": "vieille",
    "petites": "petite",
    "sont": "est",
    "nouveaux": "nouveau",
    "populaires": "populaire",
    "rendent": "rend",
    "intéressent": "intéresse",
    "bonnes": "bonne",
    "mauvaises": "mauvaise",
    "nouvelles": "nouvelle",
    "les auteurs": "l'auteur",
    "les pilotes": "le pilote",
    "les chirurgiens": "le chirurgien",
    "les fermiers": "le fermier",
    "les gérants": "le gérant",
    "les officiers": "l'officier",
    "les professeurs": "le professeur",
    "les sénateurs": "le sénateur",
    "les conseillers": "le conseiller",
    "les clientes": "la cliente",
    "les elques": "le elque",
    "les tradantains": "le tradantain",
    "les mobeaux": "le mobeau",
    "les quentouvres": "le quentouvre",
    "les voins": "le voin",
    "les ruttachâts": "le ruttachât",
    "les maldèmes": "le maldème",
    "les démins": "le démin",
    "les vertaintours": "le vertaintour",
    "les frirèmes": "le frirème",
    "les foités": "le foité",
    "les quentouvraux": "le quentouvrail",
    "les neleaux": "le neleau",
    "les déminaux": "le déminal",
    "les bouchanceaux": "le bouchanceau",
    "les vertaintouraux": "le vertaintourail",
    "les foiteux": "le foiteau",
    "les ressiers": "le ressier",
    "les nelles": "la nelle",
    "les pelquis": "la pelquis",
    "les gâtris": "la gâtris",
    "les prièrepettes": "la prièrepette",
    "les films": "le film",
    "les livres": "le livre",
    "les jeux": "le jeu",
    "les romans": "le roman",
    "les poèmes": "le poème",
    "impopulaires": "impopulaire",
    "les chansons": "la chanson",
    "les peintures": "la peinture",
    "les images": "l'image",
    "les séries": "la série",
    "les mécaniciens": "le mécanicien",
    "les banquier": "le banquier",
}
