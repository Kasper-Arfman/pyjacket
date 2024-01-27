"""
Search for sequences free from <taboo> sequence, and filter for size
Author: Kasper Arfman (8/9/2023)
"""
import re

DNA_PATH = r'D:\Data\DNA\genomes'
FILES = [
    fr'{DNA_PATH}\Arabidopsis_chr1.txt',
    fr'{DNA_PATH}\Arabidopsis_chr2.txt',
    fr'{DNA_PATH}\Arabidopsis_chr3.txt',
    fr'{DNA_PATH}\Arabidopsis_chr4.txt',
    fr'{DNA_PATH}\Arabidopsis_chr5.txt',
    ]
ENZYMES = {
    'SapI': r'GCTCTTC',
    'AfeI': r'AGCGCT',
}

TABOO = 'TGTC'
SIZE_FILTER = lambda s: 1400 <= len(s) <= 1600
GC_FILTER = lambda s: .30 <= gc_content(s) <= .70

def exclude(x: str, r=False, rc=True):   
    xrev = rev(x)
    if r and rc:
        pattern = fr"{x}|{xrev}|{revcom(x)}|{revcom(xrev)}"
    elif r:
        pattern = fr"{x}|{xrev}"  
    elif rc:
        pattern = fr"{x}|{revcom(x)}"
    else:
        pattern = fr"{x}"
    
    def f(template: str):
        return not re.search(pattern, template, re.IGNORECASE)
    return f

def rev(s: str):
    """Reverse a string"""
    return s[::-1]

def complement(s: str):
    """Complement of DNA sequence, leaving unexpected characters untouched"""
    return s.translate(str.maketrans('ATCGatcg', 'TAGCtagc'))

def revcom(s: str):
    """Reverse complement of DNA sequence (case insensitive)"""
    return rev(complement(s))

def gc_content(seq):
    return (str.count(seq, 'C') + str.count(seq, 'G')) / len(seq)

def search_genome(files):
    seqs = []
    for file in files:
        chr = search_chromosome(file)
        seqs.extend(chr)
    return seqs

def search_chromosome(file):
    with open(file, 'r') as f:
        seq = f.read().replace('\n', '')

    seqs = re.split(f"{TABOO}|{revcom(TABOO)}|N", seq, flags=re.IGNORECASE)
    seqs = filter(SIZE_FILTER, seqs)
    seqs = filter(exclude(ENZYMES['SapI']), seqs)
    seqs = filter(exclude(ENZYMES['AfeI']), seqs)
    seqs = filter(GC_FILTER, seqs)
    seqs = map(str.lower, seqs)
    return list(seqs)


def main():
    seqs = search_genome(FILES)
    print(f"\n{len(seqs)} sequences passed the filter.")
    with open('result.txt', 'w') as f:
        s = '\n'.join(seqs)
        f.write(s)
        print('Saved result to', f.name)


if __name__ == '__main__':
    main()
    pass

