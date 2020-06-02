import os
import pickle
import logging
import argparse
import numpy as np
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelWithLMHead
from tqdm import tqdm


logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description="Parameters for testing a language model")

parser.add_argument(
    "--data_dir",
    type=str,
    default="../data/",
    help="Location of the pickled stimuli files.",
)
parser.add_argument(
    "--output_dir",
    type=str,
    default="../results/",
    help="Folder for experimental results.",
)
parser.add_argument(
    "--cuda", type=int, default=-1, help="GPU to use. (Default: cpu = -1)"
)
parser.add_argument(
    "--batch_size", type=int, default=64, help="Batch size. Default=64."
)
parser.add_argument(
    "--experiments",
    type=str,
    nargs="+",
    default="all",
    help="Which languages/genders to run; any of eng, deu, deu_fem, deu_masc, deu_neut, nld, fra. Default: all.",
)
parser.add_argument(
    "--models",
    type=str,
    nargs="+",
    default="all",
    help="List of models to test in the relevant experiments. Can be set to all to test all relevant models. Possible values: deu, deu_dmbz, nld, camembert, flaubert, all",
)
parser.add_argument(
    "--prime",
    type=str,
    default="both",
    help="Whether to include a priming sentence before the stimulus. (Default both, can chose false or true)",
)
parser.add_argument(
    "--prefix",
    type=str,
    default="both",
    help="Should stimuli include bidirectional information or only prefix cues. (Default both, can choose false or true)",
)
parser.add_argument(
    "--wug",
    type=str,
    default="both",
    help='Select whether or not to look at nonce words. (Options: "true", "false", "both")',
)

args = parser.parse_args()

model_dict = {
    "deu_dbmdz": "bert-base-german-dbmdz-cased",  # from dbmdz
    "deu": "bert-base-german-cased",  # deepset.ai model
    "nld": "bert-base-dutch-cased",  # model from https://github.com/wietsedv/bertje/
    "camembert": "camembert-base",
    "flaubert": "flaubert-base-cased",
    "eng": "bert-base-cased",
}
lang2models = {
    "eng": ["eng"],
    "deu": ["deu", "deu_dbmdz"],
    "fra": ["camembert", "flaubert"],
    "nld": ["nld"],
}

lang2pref = {"eng": "This is a ", "deu": "Das ist ", "fra": "C'est "}


def load_model(model, device):
    logging.info(f"Loading {model} model...")
    tokenizer = AutoTokenizer.from_pretrained(model_dict[model])
    model = AutoModelWithLMHead.from_pretrained(model_dict[model])
    model.eval()
    model.to(device)
    logging.info(f"{model} model loaded.")
    return model, tokenizer


def batchify(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx : min(ndx + n, l)]


def get_bert_probability(tokenizer, mask, model, texts, targets, device):
    device = torch.device(device)
    mask_id = tokenizer.convert_tokens_to_ids(mask)

    batch = tokenizer.batch_encode_plus(
        texts, add_special_tokens=False, return_tensors="pt", pad_to_max_length=True
    )
    batch.to(device)
    masked_indices = (batch["input_ids"] == mask_id).nonzero()[:, 1].view(-1, 1)

    with torch.no_grad():
        outputs = model(
            input_ids=batch["input_ids"], attention_mask=batch["attention_mask"]
        )
        predictions = outputs[0]
        masked_indices = masked_indices.unsqueeze(-1).expand(
            len(texts), 1, predictions.size(-1)
        )
        temp = torch.gather(predictions, 1, masked_indices)
        result = torch.nn.functional.softmax(temp, dim=-1)

    try:
        tgts = tokenizer.batch_encode_plus(
            targets, add_special_tokens=False, return_tensors="pt"
        )["input_ids"][:, 0].to(device)
    except ValueError:
        print(texts)
        print(targets)
        raise ValueError

    return torch.gather(result.squeeze(), 1, tgts.view(-1, 1)).squeeze()


# finds index of first difference between 2 strings
def find_diff(s1, s2):
    for idx, (w1, w2) in enumerate(zip(s1, s2)):
        if w1 != w2:
            return idx


def morph_recognition_test():
    results = []
    langs = list(set([exp[:3] for exp in args.experiments]))
    device = "cpu" if args.cuda == -1 else f"cuda:{args.cuda}"
    results = []
    granular_results = []
    if args.experiments == "all":
        experiments = ["deu", "deu_fem", "eng", "fra"]
    else:
        experiments = args.experiments
    if args.models == "all":
        models = model_dict.keys()
    else:
        models = args.models
    for experiment in experiments:
        logging.info(f"Running {experiment} experiment....")
        for model_name in models:
            #  experiment starts with iso code for lang
            if model_name not in lang2models[experiment[:3]]:
                continue
            if model_name == "camembert":
                mask = "<mask>"
                cls = "<s>"
                sep = "</s>"
            elif model_name == "flaubert":
                mask = "<special1>"
                cls = "</s>"
                sep = "</s>"
            else:
                mask = "[MASK]"
                cls = "[CLS]"
                sep = "[SEP]"
            logging.info(f"For {model_name} model.")
            model, tokenizer = load_model(model_name, device)
            wugs = [False, True] if args.wug == "both" else [bool(args.wug)]
            prime = [False, True] if args.prime == "both" else [bool(args.prime)]
            for prime in prime:
                pdir = "prime/" if prime else ""
                for wug in wugs:
                    wdir = "wug/" if wug else ""
                    directory = os.fsencode(
                        f"{args.data_dir}/{experiment[:3]}/{pdir}{wdir}"
                    )
                    prefixes = [False, True] if args.prefix == "both" else [False]
                    for prefix in prefixes:
                        type = "prefix" if prefix else "bidirectional"
                        for filename in os.listdir(directory):
                            if filename.endswith(b".pickle"):
                                with open(
                                    os.path.join(directory, filename), "rb"
                                ) as infile:
                                    cond_name = filename[:-7]
                                    condition = pickle.load(infile)
                                    n_sentences = 0
                                    n_correct = 0
                                    cond_size = sum(
                                        len(cond) for cond in iter(condition.values())
                                    )

                                    logging.info(
                                        f"Testing {str(cond_name)} condition..."
                                    )
                                    with tqdm(total=cond_size) as pbar:
                                        for case in condition.keys():
                                            for batch in batchify(
                                                condition[case], args.batch_size
                                            ):
                                                probes = []
                                                gram_tgts = []
                                                ungram_tgts = []
                                                grams = []
                                                for gram, ungram in batch:
                                                    n_sentences += 1
                                                    gram = (". " + sep + " ").join(
                                                        [
                                                            s.capitalize()
                                                            for s in gram.split(".")
                                                        ]
                                                    )
                                                    ungram = (". " + sep + " ").join(
                                                        [
                                                            s.capitalize()
                                                            for s in ungram.split(".")
                                                        ]
                                                    )
                                                    gram = gram.split(" ")
                                                    ungram = ungram.split(" ")
                                                    verb_idx = find_diff(gram, ungram)
                                                    gram_tgt = gram[verb_idx]
                                                    ungram_tgt = ungram[verb_idx]
                                                    gram[verb_idx] = mask
                                                    if prefix:
                                                        probe = (
                                                            cls
                                                            + " ".join(
                                                                gram[: verb_idx + 1]
                                                            )
                                                            + ". "
                                                            + sep
                                                        )
                                                    else:  # bidirectional
                                                        probe = (
                                                            cls
                                                            + " ".join(gram)
                                                            + ". "
                                                            + sep
                                                        )
                                                    probes.append(probe)
                                                    gram_tgts.append(gram_tgt)
                                                    ungram_tgts.append(ungram_tgt)
                                                    grams.append(gram)

                                                tgt_probs = get_bert_probability(
                                                    tokenizer,
                                                    mask,
                                                    model,
                                                    probes,
                                                    gram_tgts,
                                                    device,
                                                ).tolist()
                                                ungram_tgt_probs = get_bert_probability(
                                                    tokenizer,
                                                    mask,
                                                    model,
                                                    probes,
                                                    ungram_tgts,
                                                    device,
                                                ).tolist()
                                                for i in range(len(tgt_probs)):
                                                    if (
                                                        tgt_probs[i]
                                                        > ungram_tgt_probs[i]
                                                    ):
                                                        n_correct += 1
                                                    granular_results.append(
                                                        [
                                                            experiment,
                                                            not prefix,
                                                            wug,
                                                            prime,
                                                            model_name,
                                                            cond_name,
                                                            1
                                                            if tgt_probs[i]
                                                            > ungram_tgt_probs[i]
                                                            else 0,
                                                            grams[i],
                                                            case,
                                                        ]
                                                    )
                                                pbar.update(len(tgt_probs))
                                    results.append(
                                        [
                                            experiment,
                                            not prefix,
                                            wug,
                                            prime,
                                            model_name,
                                            cond_name,
                                            cond_size,
                                            n_correct / n_sentences,
                                        ]
                                    )
                                    results_df = pd.DataFrame(
                                        results,
                                        columns=[
                                            "Experiment",
                                            "Bidirectional",
                                            "Wug",
                                            "Prime",
                                            "Model",
                                            "Condition",
                                            "Condition Size",
                                            "Accuracy",
                                        ],
                                    )
                                    """
                                    granular_results_df = pd.DataFrame(
                                        granular_results,
                                        columns=[
                                            "Experiment",
                                            "Bidirectional",
                                            "Wug",
                                            "Prime",
                                            "Model",
                                            "Condition",
                                            "Correct",
                                            "Sentence",
                                            "Subcondition",
                                        ],
                                    )
                                    """
                                    pickle.dump(
                                        results_df,
                                        open(
                                            f"{args.output_dir}results_{'_'.join(args.experiments)}_prime_{args.prime}_wug_{args.wug}_prefix_{args.prefix}.pickle",
                                            "wb+",
                                        ),
                                    )
                                    if False:
                                        pickle.dump(
                                            granular_results_df,
                                            open(
                                                f"{args.output_dir}gran_results_{'_'.join(args.experiments)}_prime_{args.prime}_wug_{args.wug}_prefix_{args.prefix}.pickle",
                                                "wb+",
                                            ),
                                        )


morph_recognition_test()
