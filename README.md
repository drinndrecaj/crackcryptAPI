# CrackCrypt Hash Lookup

  Hash Cracking tool to check one or many hashes (MD5, SHA1, NTLM only) against the CrackCrypt.com API and retrieve plaintexts when they’re known.

## Features

- Query a single hash or batch-process a file of hashes  
- Outputs structured JSON results  
- Built-in rate limiting (default 1 sec/request) to respect API quotas  
- Progress indicators for batch jobs  


## Installation

1. Clone this repository:  
   git clone https://github.com/drinndrecaj/crackcrypt.git  
   cd crackcrypt  

2. Create and activate a virtual environment:  
   python3 -m venv venv  
   source venv/bin/activate  

3. Install dependencies:  
   pip install requests  

## Usage

python crackcrypt.py [--hash HASH | --input FILE] --alg ALGORITHM [--output FILE]

### Arguments

- -H, --hash     Single hex-encoded hash to check  
- -i, --input    Path to a file containing one hash per line  
- -a, --alg      Hash algorithm (e.g. md5, sha1, sha256) **(required)**  
- -o, --output   Optional path to write JSON results; if omitted, prints to stdout  

## Examples

Check a single MD5 hash and print to console:  
python crackcrypt.py -H 21232f297a57a5a743894a0e4a801fc3 -a md5

Batch-check SHA1 hashes from a file and save output:  
python crackcrypt.py -i hashes.txt -a sha1 -o results.json


## Output Format

Results are a JSON array of objects with the fields:

[
  {
    "hash":      "21232f297a57a5a743894a0e4a801fc3",
    "alg":       "md5",
    "found":     true,
    "plaintext": "admin",    // or null if not found
    "elapsed":   0.123              // API lookup time in seconds
  }
]

## License

MIT License © Crackcrypt.com
