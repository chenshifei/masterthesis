#!/bin/bash

# Job name:
#SBATCH --job-name=build_embeddings
#
# Project:
#SBATCH --account=nn9447k
#
# Wall time limit:
#SBATCH --time=1-00:00:00
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
module load Python/3.7.4-GCCcore-8.3.0
module list

cd $USERWORK

source thesis_env/bin/activate

cd embeddings

python3 merge_embeddings.py wiki.en.align.vec wiki.fr.align.vec wiki.de.align.vec wiki.he.align.vec --output wiki.merged+he.align.vec
