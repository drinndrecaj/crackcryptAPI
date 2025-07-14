import argparse
import json
import time
import requests
import sys

API_URL = "https://crackcrypt.com/api/v1/lookup"
RATE_LIMIT_DELAY = 1.0  # seconds between requests

def crack_hash(hash_value: str, alg: str) -> dict:
    payload = {"hash": hash_value, "alg": alg}
    resp = requests.post(API_URL, json=payload, headers={"Content-Type": "application/json"})
    resp.raise_for_status()
    data = resp.json()
    return {
        "hash":      hash_value,
        "alg":       alg,
        "found":     data.get("found", False),
        "plaintext": data.get("plaintext"),
        "elapsed":   data.get("elapsed"),
    }

def main():
    parser = argparse.ArgumentParser(
        description="Check one or many hashes via the CrackCrypt API"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--input", "-i",
        help="Path to a file containing one hash per line"
    )
    group.add_argument(
        "--hash", "-H",
        help="Single hex-encoded hash to check"
    )
    parser.add_argument(
        "--alg", "-a",
        required=True,
        help="Hash algorithm (e.g. md5, sha1, ...)"
    )
    parser.add_argument(
        "--output", "-o",
        help="(Optional) Path to write JSON results; if omitted, prints to stdout"
    )
    args = parser.parse_args()

    # Build list of hashes
    if args.hash:
        hashes = [args.hash.strip()]
    else:
        try:
            with open(args.input, "r") as f:
                hashes = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: file not found: {args.input}", file=sys.stderr)
            sys.exit(1)

    results = []
    for idx, h in enumerate(hashes, start=1):
        try:
            result = crack_hash(h, args.alg)
        except Exception as e:
            result = {"hash": h, "alg": args.alg, "error": str(e)}
        results.append(result)
        status = "FOUND" if result.get("found") else "NOT FOUND"
        print(f"[{idx}/{len(hashes)}] {h} → {status}")
        time.sleep(RATE_LIMIT_DELAY)

    output_json = json.dumps(results, indent=2)

    if args.output:
        try:
            with open(args.output, "w") as out:
                out.write(output_json)
            print(f"Done: {len(results)} hashes checked, results saved to {args.output}")
        except IOError as e:
            print(f"Error writing to {args.output}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Print to stdout
        print(output_json)

if __name__ == "__main__":
    main()
