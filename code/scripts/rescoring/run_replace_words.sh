#!/bin/bash

# Job name:
#SBATCH --job-name=replace_words
# Project:
#SBATCH --account=nn9447k
#
# Wall time limit:
#SBATCH --time=14-00:00:00
#
# Other parameters:
#SBATCH --mem-per-cpu=128G
#SBATCH --partition=bigmem
#SBATCH --ntasks=1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=shifei.chen.2701@student.uu.se

## Set up job environment:
set -o errexit  # Exit the script on any error
set -o nounset  # Treat any unset variables as an error

module --quiet purge  # Reset the modules to the system default
module load SciPy-bundle/2019.10-intel-2019b-Python-3.7.4
module list

cd $USERWORK

source thesis_env/bin/activate

cd scripts/rescoring

python3 replace_words.py ../../corpus/preproc/lexicon_replacement/en+de+da+no_en+de+da+no/test.tok.norm.src.sv ../../embeddings/wiki.sv.align.vec ../../embeddings/wiki.no.align.vec --output ../../corpus/preproc/lexicon_replacement/en+de+da+no_en+de+da+no/test.tok.norm.src.sv.0 --threshold 0 --langid __sv__

# python3 replace_words.py ../../corpus/preproc/lexicon_replacement/en+de+da+no_en+de+da+no/test.tok.norm.src.sv ../../embeddings/wiki.sv.align.vec ../../embeddings/wiki.no.align.vec --output ../../corpus/preproc/lexicon_replacement/en+de+da+no_en+de+da+no/test.tok.norm.src.sv.0.25 --threshold 0.25 --langid __sv__

# python3 replace_words.py ../../corpus/preproc/lexicon_replacement/en+de+da+no_en+de+da+no/test.tok.norm.src.sv ../../embeddings/wiki.sv.align.vec ../../embeddings/wiki.no.align.vec --output ../../corpus/preproc/lexicon_replacement/en+de+da+no_en+de+da+no/test.tok.norm.src.sv.0.5 --threshold 0.5 --langid __sv__

# python3 replace_words.py ../../corpus/preproc/lexicon_replacement/en+de+da+no_en+de+da+no/test.tok.norm.src.sv ../../embeddings/wiki.sv.align.vec ../../embeddings/wiki.no.align.vec --output ../../corpus/preproc/lexicon_replacement/en+de+da+no_en+de+da+no/test.tok.norm.src.sv.1 --threshold 1 --langid __sv__

# python3 replace_words.py ../../corpus/preproc/lexicon_replacement/en+de+da+no_en+de+da+no/test.tok.norm.src.sv ../../embeddings/wiki.sv.align.vec ../../embeddings/wiki.no.align.vec --output ../../corpus/preproc/lexicon_replacement/en+de+da+no_en+de+da+no/test.tok.norm.src.sv.2 --threshold 2 --langid __sv__

# python3 replace_words.py ../../corpus/preproc/lexicon_replacement/en+de+da+no_en+de+da+no/test.tok.norm.src.sv ../../embeddings/wiki.sv.align.vec ../../embeddings/wiki.no.align.vec --output ../../corpus/preproc/lexicon_replacement/en+de+da+no_en+de+da+no/test.tok.norm.src.sv.3 --threshold 3 --langid __sv__

# python3 replace_words.py ../../corpus/preproc/lexicon_replacement/en+de+da+no_en+de+da+no/test.tok.norm.src.sv ../../embeddings/wiki.sv.align.vec ../../embeddings/wiki.no.align.vec --output ../../corpus/preproc/lexicon_replacement/en+de+da+no_en+de+da+no/test.tok.norm.src.sv.3 --threshold 3 --langid __sv__
