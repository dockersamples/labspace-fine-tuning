#!/usr/bin/env python
# prepare_pii_masking_for_unsloth.py
# Usage examples:
#   python prepare_pii_masking_for_unsloth.py --outdir data_out
#   python prepare_pii_masking_for_unsloth.py --langs en es --locales ES US --outdir data_out_esus
#   python prepare_pii_masking_for_unsloth.py --mode spans --outdir spans_out --eos "</s>"

import argparse
import json
import os
import random
from typing import List, Dict, Any, Optional

from datasets import load_dataset

INSTRUCTION_REDACTION = (
    "Mask all PII in the following text. Replace each entity with the exact "
    "UPPERCASE label in square brackets (e.g., [PERSON], [EMAIL], [PHONE], [USERNAME], "
    "[ADDRESS], [CREDIT_CARD], [TIME], etc.). Preserve all non-PII text, whitespace, "
    "and punctuation exactly. Return ONLY the redacted text.\n\n"
    "Text:\n{src}"
)

INSTRUCTION_SPANS = (
    "Extract all PII spans from the text and return a JSON array of objects with keys "
    '\"value\", \"start\", \"end\", and \"label\" (character offsets on the original text). '
    "Return [] if none.\n\n"
    "Text:\n{src}"
)

def row_passes_filters(ex: Dict[str, Any],
                       langs: Optional[set],
                       locales: Optional[set]) -> bool:
    if langs and ex.get("language") not in langs:
        return False
    if locales and ex.get("locale") not in locales:
        return False
    return True

def redact_pair(ex: Dict[str, Any], eos: Optional[str]) -> Optional[Dict[str, str]]:
    src = (ex.get("source_text") or "").strip()
    tgt = (ex.get("masked_text") or "").strip()
    if not src or not tgt:
        return None
    prompt = INSTRUCTION_REDACTION.format(src=src)
    response = tgt + (eos if eos and not tgt.endswith(eos) else "")
    return {"prompt": prompt, "response": response}

def spans_pair(ex: Dict[str, Any], eos: Optional[str]) -> Optional[Dict[str, str]]:
    src = (ex.get("source_text") or "").strip()
    if not src:
        return None
    mask = ex.get("privacy_mask")
    # Some loaders might deliver it already as a list; normalize.
    if isinstance(mask, str):
        try:
            mask = json.loads(mask)
        except Exception:
            mask = []
    if not isinstance(mask, list):
        mask = []
    prompt = INSTRUCTION_SPANS.format(src=src)
    tgt = json.dumps(mask, ensure_ascii=False)
    tgt = tgt + (eos if eos and not tgt.endswith(eos) else "")
    return {"prompt": prompt, "response": tgt}

def convert_split(split_name: str,
                  mode: str,
                  langs: Optional[set],
                  locales: Optional[set],
                  sample: Optional[int],
                  eos: Optional[str],
                  seed: int) -> List[Dict[str, str]]:
    ds = load_dataset("ai4privacy/pii-masking-400k", split=split_name)
    rows: List[Dict[str, str]] = []
    maker = redact_pair if mode == "redaction" else spans_pair

    for ex in ds:
        if not row_passes_filters(ex, langs, locales):
            continue
        pair = maker(ex, eos)
        if pair:
            rows.append(pair)

    # Optional sampling for quick experiments
    if sample is not None and sample > 0 and sample < len(rows):
        random.seed(seed)
        random.shuffle(rows)
        rows = rows[:sample]

    return rows

def save_json_list(rows: List[Dict[str, str]], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

def main():
    ap = argparse.ArgumentParser(description="Prepare ai4privacy/pii-masking-400k for Unsloth SFT.")
    ap.add_argument("--outdir", type=str, required=True, help="Output directory.")
    ap.add_argument("--mode", type=str, choices=["redaction", "spans"], default="redaction",
                    help="redaction: source_text->masked_text; spans: source_text->privacy_mask JSON.")
    ap.add_argument("--langs", nargs="*", default=None,
                    help="Filter languages (e.g., en es fr de it nl). Omit for all.")
    ap.add_argument("--locales", nargs="*", default=None,
                    help="Filter locales (e.g., US ES GB DE FR IT NL). Omit for all.")
    ap.add_argument("--sample_train", type=int, default=None,
                    help="Optionally subsample N train rows.")
    ap.add_argument("--sample_val", type=int, default=None,
                    help="Optionally subsample N validation rows.")
    ap.add_argument("--eos", type=str, default=None,
                    help="EOS token to append to responses (e.g., </s>).")
    ap.add_argument("--seed", type=int, default=3407)
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    langs = set(args.langs) if args.langs else None
    locales = set(args.locales) if args.locales else None

    # Convert both splits provided by the dataset
    print("Loading & converting train split…")
    train_rows = convert_split(
        "train", args.mode, langs, locales, args.sample_train, args.eos, args.seed
    )
    print(f"Train examples kept: {len(train_rows):,}")

    print("Loading & converting validation split…")
    val_rows = convert_split(
        "validation", args.mode, langs, locales, args.sample_val, args.eos, args.seed
    )
    print(f"Validation examples kept: {len(val_rows):,}")

    # Save JSON (list) that your current script expects
    train_path = os.path.join(args.outdir, f"pii_{args.mode}_train.json")
    val_path = os.path.join(args.outdir, f"pii_{args.mode}_val.json")
    save_json_list(train_rows, train_path)
    save_json_list(val_rows, val_path)

    # Also save tiny “combined” for quick smoke tests if val exists
    combo_path = os.path.join(args.outdir, f"pii_{args.mode}_small.json")
    small = (train_rows[:200] if len(train_rows) > 200 else train_rows) + \
            (val_rows[:50] if len(val_rows) > 50 else val_rows)
    save_json_list(small, combo_path)

    print("\nWrote:")
    print("  ", train_path)
    print("  ", val_path)
    print("  ", combo_path)
    print("\nPoint your existing script at one of these (e.g., pii_redaction_train.json).")

if __name__ == "__main__":
    main()
