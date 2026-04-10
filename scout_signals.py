import wfdb
import os

def scout():
    base_dir = 'data/raw/physionet_autonomic/'
    records_file = os.path.join(base_dir, 'RECORDS')
    
    with open(records_file, 'r') as f:
        record_ids = [line.strip() for line in f.readlines()[:20]] # Just check first 20

    print("🔎 Signal Discovery in Progress...")
    found_signals = set()
    
    for rid in record_ids:
        try:
            record_header = wfdb.rdheader(os.path.join(base_dir, rid))
            for name in record_header.sig_name:
                found_signals.add(name)
        except:
            continue
            
    print("\n--- Unique Signals Found in Dataset ---")
    for s in sorted(found_signals):
        print(f"- {s}")

if __name__ == "__main__":
    scout()