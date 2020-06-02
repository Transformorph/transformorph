class AgreementTemplateEng:
    def __init__(self):
        self.rules = {
            "obj_rel_across": (
                (
                    ["D", "MS", "C", "D", "ES", "EV", "MV"],
                    ["D", "IS", "IC", "D", "ES", "EV", "IV"],
                ),
                {"match": ([1], [6]), "vary": [4, 5]},
            ),
            "obj_rel_within": (
                (
                    ["D", "MS", "C", "D", "ES", "EV", "MV"],
                    ["D", "IS", "IC", "D", "ES", "EV", "IV"],
                ),
                {"match": ([4], [5]), "vary": [1]},  # , 6]},
            ),
            "subj_rel": (
                (["D", "MS", "C", "EV", "D", "ES", "MV"],),
                {"match": ([1, 3], [6]), "vary": [5]},
            ),
            "prep": (
                (["D", "MS", "P", "D", "ES", "MV"], ["D", "IS", "IP", "D", "ES", "IV"]),
                {"match": ([1], [5]), "vary": [4]},
            ),
            "obj_rel_no_comp_across": (
                (
                    ["D", "MS", "D", "ES", "EV", "MV"],
                    ["D", "IS", "D", "ES", "EV", "IV"],
                ),
                {"match": ([1], [5]), "vary": [3, 4]},
            ),
            "obj_rel_no_comp_within": (
                (
                    ["D", "IS", "D", "ES", "EV", "IV"],
                    ["D", "MS", "D", "ES", "EV", "MV"],
                ),
                {"match": ([3], [4]), "vary": [1]},  # , 5]},
            ),
            "simple_agrmt": (
                (["D", "MS", "MV"], ["D", "IS", "IV"]),
                {"match": ([1], [2]), "vary": []},
            ),
            "sent_comp": (
                (["D", "BS", "BV", "D", "MS", "MV"],),
                {"match": ([4], [5]), "vary": [1]},
            ),
            "vp_coord": (
                (["D", "MS", "MV", "AND", "MV"],),
                {"match": ([1, 2], [4]), "vary": []},
            ),
            "long_vp_coord": (
                (["D", "MS", "LMV", "AND", "LMV"],),
                {"match": ([1, 2], [4]), "vary": []},
            ),
        }


class AgreementTemplateFra:
    def __init__(self):
        self.rules = {
            "obj_rel_across": (
                (
                    ["MS", "C", "ES", "EV", "MV"],
                    ["MSF", "C", "ES", "EV", "MVF"],
                    ["IS", "C", "ES", "EV", "IV"],
                    ["ISF", "C", "ES", "EV", "IVF"],
                ),
                {"match": ([0], [4]), "vary": [2, 3]},
            ),
            "obj_rel_within": (
                (
                    ["MS", "C", "ES", "EV", "MV"],
                    ["MSF", "C", "ES", "EV", "MVF"],
                    ["IS", "C", "ES", "EV", "IV"],
                    ["ISF", "C", "ES", "EV", "IVF"],
                ),
                {"match": ([2], [3]), "vary": [0]},  # , 6]},
            ),
            "subj_rel": (
                (["MS", "C", "EV", "ES", "MV"], ["MSF", "C", "EV", "ES", "MVF"]),
                {"match": ([0, 2], [4]), "vary": [3]},
            ),
            "prep": (
                (
                    ["MS", "P", "ES", "MV"],
                    ["MSF", "P", "ES", "MVF"],
                    ["IS", "IP", "ES", "IV"],
                    ["ISF", "IP", "ES", "IVF"],
                ),
                {"match": ([0], [3]), "vary": [2]},
            ),
            "simple_agrmt": (
                (["MS", "MV"], ["IS", "IV"], ["ISF", "IVF"], ["MSF", "MVF"]),
                {"match": ([0], [1]), "vary": []},
            ),
            "sent_comp": (
                (["BS", "BV", "C", "MS", "MV"], ["BS", "BV", "C", "MSF", "MVF"]),
                {"match": ([3], [4]), "vary": [0]},
            ),
            "vp_coord": (
                (["MS", "MV", "AND", "MV"], ["MSF", "MVF", "AND", "MVF"]),
                {"match": ([0, 1], [3]), "vary": []},
            ),
            "long_vp_coord": (
                (["MS", "LMV", "AND", "LMV"], ["MSF", "LMV", "AND", "LMV"]),
                {"match": ([0, 1], [3]), "vary": []},
            ),
        }


class AgreementTemplateNld:
    def __init__(self):
        self.rules = {
            "obj_rel_across": (
                (["MSC", "ES", "EV", "MV"], ["ISC", "ES", "EV", "IV"]),
                {"match": ([0], [3]), "vary": [1, 2]},
            ),
            "obj_rel_within": (
                (["ISC", "ES", "EV", "IV"], ["MSC", "ES", "EV", "MV"]),
                {"match": ([1], [2]), "vary": [0, 3]},
            ),
            "prep": (
                (["MS", "P", "ESD", "MV"], ["MS", "IP", "ESD", "IV"]),
                {"match": ([0], [3]), "vary": [2]},
            ),
            "simple_agrmt": (
                (["MS", "MV"], ["IS", "IV"]),
                {"match": ([0], [1]), "vary": []},
            ),
            "sent_comp": (
                (["BS", "BV", "MS", "MV"],),
                {"match": ([2], [3]), "vary": [0]},
            ),
            "vp_coord": (
                (["MS", "MV", "AND", "MV"],),
                {"match": ([0, 1], [3]), "vary": []},
            ),
            "long_vp_coord": (
                (["MS", "LMV", "AND", "LMV"],),
                {"match": ([0, 1], [3]), "vary": []},
            ),
        }


class AgreementTemplateDeu:
    def __init__(self):
        self.rules = {
            "obj_rel_across": (
                (["MSC", "ES", "EV", "MV"], ["ISC", "ES", "EV", "IV"]),
                {"match": ([0], [3]), "vary": [1, 2]},
            ),
            "obj_rel_within": (
                (["ISC", "ES", "EV", "IV"], ["MSC", "ES", "EV", "MV"]),
                {"match": ([1], [2]), "vary": [0, 3]},
            ),
            "prep": (
                (["MS", "P", "ESD", "MV"], ["MS", "IP", "ESD", "IV"]),
                {"match": ([0], [3]), "vary": [2]},
            ),
            "simple_agrmt": (
                (["MS", "MV"], ["IS", "IV"]),
                {"match": ([0], [1]), "vary": []},
            ),
            "sent_comp": (
                (["BS", "BV", "MS", "MV"],),
                {"match": ([2], [3]), "vary": [0]},
            ),
            "vp_coord": (
                (["MS", "MV", "AND", "MV"],),
                {"match": ([0, 1], [3]), "vary": []},
            ),
            "long_vp_coord": (
                (["MS", "LMV", "AND", "LMV"],),
                {"match": ([0, 1], [3]), "vary": []},
            ),
        }


class AgreementTemplateDeuF:
    def __init__(self):
        self.rules = {
            "obj_rel_across": (
                (
                    ["DF", "MSF", "CF", "DF", "ESF", "EV", "MV"],
                    ["DF", "ISF", "CF", "DF", "ESF", "EV", "IV"],
                ),
                {"match": ([1], [6]), "vary": [4, 5]},
            ),
            "obj_rel_within": (
                (
                    ["DF", "ISF", "CF", "DF", "ESF", "EV", "IV"],
                    ["DF", "MSF", "CF", "DF", "ESF", "EV", "MV"],
                ),
                {"match": ([4], [5]), "vary": [1]},
            ),
            "prep": (
                (["DF", "MSF", "P", "ESFD", "MV"], ["DF", "MSF", "IP", "ESFD", "IV"]),
                {"match": ([1], [4]), "vary": [3]},
            ),
            "simple_agrmt": (
                (["DF", "MSF", "MV"], ["DF", "ISF", "IV"]),
                {"match": ([1], [2]), "vary": []},
            ),
            "sent_comp": (
                (["DF", "BSF", "BV", "DF", "MSF", "MV"],),
                {"match": ([4], [5]), "vary": [1]},
            ),
            "vp_coord": (
                (["DF", "MSF", "MV", "AND", "MV"],),
                {"match": ([1, 2], [4]), "vary": []},
            ),
            "long_vp_coord": (
                (["DF", "MSF", "LMV", "AND", "LMV"],),
                {"match": ([1, 2], [4]), "vary": []},
            ),
        }

        # TO CREATE NEW CONSTRUCTIONS, PLEASE FOLLOW THIS FORMAT:
        # 'name': ([list of preterminals], {dict containing ('match', 'vary') indices formatted as below})
        # {'match':([first indices (subject)], [second indices (verb/anaphor)]), 'vary':[list of indices for words to vary in number (attractors)},
