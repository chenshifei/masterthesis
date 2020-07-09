#!/bin/bash

# Job name:
#SBATCH --job-name=build_corpus
#
# Project:
#SBATCH --account=nn9447k
#
# Wall time limit:
#SBATCH --time=1-00:00:00
#
# Other parameters:
#SBATCH --mem-per-cpu=4G
#SBATCH --partition=normal
#SBATCH --ntasks=1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=shifei.chen.2701@student.uu.se

## Set up job environment:
set -o errexit  # Exit the script on any error
set -o nounset  # Treat any unset variables as an error

module --quiet purge  # Reset the modules to the system default
module load Python/3.7.4-GCCcore-8.3.0
module list

cd $USERWORK/corpus

python3 ted_reader.py -i original/ -s en de da he he he -t he he he en de da -ncp -ttok --save_data_dir data/tgt_token

