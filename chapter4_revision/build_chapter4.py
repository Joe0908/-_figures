"""Build only the five current Chapter 4 figures, in reading order."""
from pathlib import Path
import subprocess, sys
FILES=['F09_same_genome_different_programs.py','F10_minimal_regulatory_model.py',
       'F11_regulatory_grammar.py','F12_three_reading_conditions.py',
       'F13_regulatory_possibilities_to_identity.py']
if __name__=='__main__':
    for name in FILES:
        subprocess.run([sys.executable,str(Path(__file__).parent/name)],check=True)
