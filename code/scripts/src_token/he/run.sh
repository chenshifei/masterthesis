#!/bin/bash

# Job name:
#SBATCH --job-name=en+de+fr+he_src_token
#
# Project:
#SBATCH --account=nn9447k
#SBATCH --partition=accel --gres=gpu:1
#
# Wall time limit:
#SBATCH --time=7-00:00:00
#
# Other parameters:
#SBATCH --mem-per-cpu=16G
#SBATCH --ntasks=1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=shifei.chen.2701@student.uu.se

## Set up job environment:
set -o errexit  # Exit the script on any error
set -o nounset  # Treat any unset variables as an error

module --quiet purge  # Reset the modules to the system default
module load PyTorch/1.3.1-fosscuda-2019b-Python-3.7.4
module list

cd $USERWORK

source thesis_env/bin/activate

export DEFAULT_REPORT_PATH="output/reports/{EXP}"

xnmt --dynet-gpu exp_settings/src_token/merged+he.yaml
