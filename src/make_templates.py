import random
import pickle
import sys
import os
from Plurals import Pluralizer
from Singulars import Singularizer

from template.Terminals import (
    AgreementTerminalsDeu,
    AgreementTerminalsEng,
    AgreementTerminalsFra,
)
from template.Templates import (
    AgreementTemplateDeu,
    AgreementTemplateDeuF,
    AgreementTemplateFra,
    AgreementTemplateEng,
)
from template.TestCases import TestCase


class MakeAgreementTemplate:
    def __init__(self, terms, template, lang):
        self.terminals = terms.terminals
        self.rules = template.rules
        self.lang = lang

        if lang == "eng":
            self.closed_class_terms = ["D", "C"]
        elif lang == "deu":
            self.closed_class_terms = ["DF", "CF", "DM", "DN", "CM", "CN"]
        elif lang == "fra":
            self.closed_class_terms = ["C"]

    def get_case_name(self, preterms, match, vary, opt="sing", v_opt="sing"):
        sent = opt + "_"
        for j in range(len(match)):
            for i in range(len(match[j])):
                sent += preterms[match[j][i]] + "_"
        if len(vary) > 0:
            sent += v_opt + "_"
            for j in range(len(vary)):
                sent += preterms[vary[j]] + "_"
        return sent[:-1]

    def switch_numbers(self, base_sent, variables, preterms):
        new_sent = base_sent[:]
        for idx in variables:
            phrase = new_sent[idx]
            if self.lang == "eng":
                phrase = (phrase, preterms[idx][-1] == "V")
            new_sent[idx] = {
                "plur": Pluralizer.pluralize(phrase, self.lang),
                "sing": new_sent[idx],
            }
        return new_sent

    def indefinite(self, noun):
        if len(noun.split()) == 3:  # includes a complementizer, remove
            noun = " ".join(noun.split()[:2])
        if self.lang == "fra":
            if noun[:2] == "la":  # feminine
                return "une" + noun[2:]
            elif noun[2:] in [
                "architecte",
                "acteur",
                "assistant",
                "officier",
                "auteur",
            ]:
                # masculine, special case for l'
                return "un " + noun[2:]
            elif noun[2:] == "image":
                # feminine, special case for l'
                return "une " + noun[2:]
            else:
                return "un " + noun
        elif self.lang == "deu":
            if noun[:3] == "die":  # feminine
                return "eine" + noun[3:]
            elif noun[:3] in ["das", "der"]:  # masculine or neuter
                return "ein" + noun[3:]
            else:
                return "eine " + noun
        elif self.lang == "eng":
            return "a " + noun

    def make_variable_sents(self, preterms, match, vary, prime=False):
        all_sents = {}
        base_sent = [self.terminals[p] for p in preterms]
        prefixes = ["sing", "plur"]
        for i in range(2):
            s_grammatical = base_sent[:]
            p_grammatical = self.switch_numbers(base_sent, vary, preterms)

            s_ungrammatical = self.switch_numbers(s_grammatical, match[1], preterms)
            p_ungrammatical = self.switch_numbers(p_grammatical, match[1], preterms)

            if i == 1:
                s_ungrammatical = self.switch_numbers(s_grammatical, match[0], preterms)
                p_ungrammatical = self.switch_numbers(p_grammatical, match[0], preterms)
                s_grammatical = self.switch_numbers(
                    s_grammatical, match[0] + match[1], preterms
                )
                p_grammatical = self.switch_numbers(
                    p_grammatical, match[0] + match[1], preterms
                )
            all_sents[
                self.get_case_name(preterms, match, vary, opt=prefixes[i], v_opt="sing")
            ] = [s_grammatical, s_ungrammatical]
            if len(vary) > 0:
                all_sents[
                    self.get_case_name(
                        preterms, match, vary, opt=prefixes[i], v_opt="plur"
                    )
                ] = [p_grammatical, p_ungrammatical]
        return all_sents


class MakeTestCase:
    def __init__(self, template, test_case, wug=False, prime=False):
        self.template = template
        self.test_case = test_case
        self.wug = wug
        self.prime = prime
        self.sent_templates = self.get_rules()

    def wuggify(self, preterms, match):
        new_preterms = []
        for idx, preterm in enumerate(preterms):
            mtch = False
            for m in match:
                if idx in m:
                    mtch = True
            if len(preterm) > 1 and preterm[1] == "S" and mtch:
                if len(preterm) <= 2:
                    p = "NS"
                else:
                    p = "NS" + preterm[2:]
                if p not in self.template.terminals:
                    p = "NSB"
                new_preterms.append(p)
            else:
                new_preterms.append(preterm)
        return new_preterms

    def primify(self, sent):
        sent, prime = sent
        return self.template.terminals["PRM"][0] + " " + prime + ". " + sent

    def get_rules(self):
        sent_templates = {}
        patterns, templates = self.template.rules[self.test_case]
        for preterminals in patterns:
            if self.wug == True:
                preterminals = self.wuggify(preterminals, templates["match"])
            if templates is not None:
                sents = self.template.make_variable_sents(
                    preterminals, templates["match"], templates["vary"], self.prime
                )
                for k in sents.keys():
                    if k not in sent_templates:
                        sent_templates[k] = []
                    gram = list(self.expand_sent(sents[k][0], match=templates["match"]))
                    ungram = list(
                        self.expand_sent(sents[k][1], match=templates["match"])
                    )
                    if self.prime:
                        gram = [self.primify(s) for s in gram]
                        ungram = [self.primify(s) for s in ungram]
                    else:
                        gram = [s[0] for s in gram]
                        ungram = [s[0] for s in ungram]
                    for i in range(len(gram)):
                        sent_templates[k].append((gram[i], ungram[i]))
            else:
                print("hhhhhhhh")
                sents = self.template.make_variable_sents(
                    preterminals,
                    simple=self.test_case.startswith("simple"),
                    prime=self.prime,
                )
                for k in sents.keys():
                    if k not in sent_templates:
                        sent_templates[k] = []
                    gram = list(self.expand_sent(sents[k][0]), match=templates["match"])
                    intrusive = list(
                        self.expand_sent(
                            sents[k][1],
                            partial="",
                            switch_ds=not self.test_case.startswith("simple"),
                            match=templates["match"],
                        )
                    )
                    ungram = list(
                        self.expand_sent(sents[k][2]), match=templates["match"]
                    )
                    for i in range(len(gram)):
                        sent_templates[k].append((gram[i], intrusive[i], ungram[i]))
        return sent_templates

    def expand_sent(
        self, sent, partial="", idx=0, switch_ds=False, lel=False, match=[]
    ):

        if len(sent) == 1:
            try:
                wrds = sent[0]["plur"]
                sings = sent[0]["sing"]
            except TypeError:  # then its a list
                wrds = sent[0]
                sings = wrds
            for wrd in wrds:
                try:
                    if self.template.lang == "eng":
                        p = Pluralizer.pluralize(([wrd], True), self.template.lang)[0]
                        p1 = Pluralizer.pluralize(([wrd], False), self.template.lang)[0]
                    else:
                        p = Pluralizer.pluralize([wrd], self.template.lang)[0]
                        p1 = "PLACEHOLDER"
                    sing = Singularizer.singularize([wrd], self.template.lang)[0]
                except KeyError:
                    sing = wrd
                closed_class = (
                    sum(
                        [
                            1 if wrd in self.template.terminals[term] else 0
                            for term in self.template.closed_class_terms
                        ]
                    )
                    > 0
                )

                # We want to avoid repeating words/phrases multiple times in the sentences
                # but some words are allowed to repeat, such as determiners or complementizers
                # We also need to check that the phrase isn't repeated save for number
                # e.g. 'the man who the guards like likes pizza'
                # not all sentences with repeating phrases are bad, but many seem implausible
                # so we do not generate them!
                # bad = False
                # if wrd.split()[0] == "is":
                #     bad = "are" in partial
                # elif wrd.split()[0] == "are":
                #     bad = "is" in partial
                if (
                    closed_class
                    or wrd not in partial.split(".")[-1]
                    and p not in partial.split(".")[-1]
                    and p1 not in partial.split(".")[-1]
                    and sing not in partial.split(".")[-1]
                ):
                    if idx == match[0][0]:
                        yield (partial + wrd, self.template.indefinite(sings[i]))
                    else:
                        yield (partial + wrd, "None")
                else:
                    yield "None"
        else:
            try:
                wrds = sent[0]["plur"]
                sings = sent[0]["sing"]
            except TypeError:  # then its a list
                wrds = sent[0]
                sings = wrds
            for i, wrd in enumerate(wrds):
                for x in self.expand_sent(
                    sent=sent[1:],
                    partial=partial + wrd + " ",
                    switch_ds=switch_ds,
                    match=match,
                    idx=idx + 1,
                    lel=lel,
                ):
                    if x != "None":
                        if idx == match[0][0]:
                            yield (x[0], self.template.indefinite(sings[i]))
                        else:
                            yield x


def main():
    testcase = TestCase()
    experiments = [
        (
            MakeAgreementTemplate(
                AgreementTerminalsDeu(), AgreementTemplateDeu(), "deu"
            ),
            "deu",
        ),
        (
            MakeAgreementTemplate(
                AgreementTerminalsDeu(), AgreementTemplateDeuF(), "deu"
            ),
            "deu_fem",
        ),
        (
            MakeAgreementTemplate(
                AgreementTerminalsEng(), AgreementTemplateEng(), "eng"
            ),
            "eng",
        ),
        (
            MakeAgreementTemplate(
                AgreementTerminalsFra(), AgreementTemplateFra(), "fra"
            ),
            "fra",
        ),
    ]

    if len(sys.argv) != 2:
        print("Usage: python make_templates.py [template_dir]")
        sys.exit(1)

    out_dir = sys.argv[1]

    for experiment, experiment_name in experiments:
        print(experiment_name)
        for prime in [False, True]:
            if prime:
                prm = "prime/"
                print("prime")
            else:
                prm = ""
                print("no prime")
            for wug in [False, True]:
                if wug:
                    wg = "wug/"
                else:
                    wg = ""
                    print("real words")
                for case in testcase.all_cases[experiment_name[:3]]:
                    print("case:", case)
                    sents = MakeTestCase(experiment, case, wug=wug, prime=prime)
                    # print(sents.sent_templates)
                    os.makedirs(
                        os.path.dirname(
                            out_dir + "/" + experiment_name + "/" + prm + wg
                        ),
                        exist_ok=True,
                    )
                    with open(
                        out_dir
                        + "/"
                        + experiment_name
                        + "/"
                        + prm
                        + wg
                        + case
                        + ".pickle",
                        "wb",
                    ) as f:
                        pickle.dump(sents.sent_templates, f)


if __name__ == "__main__":
    main()
