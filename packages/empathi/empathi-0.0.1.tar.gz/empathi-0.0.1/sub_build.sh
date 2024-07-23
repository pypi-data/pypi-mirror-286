#!/bin/bash
#SBATCH --job-name=build
#SBATCH --output=/project/def-eroussea/projects/test/build.stdout
#SBATCH --error=/project/def-eroussea/projects/test/build.stderr
#SBATCH --account=def-eroussea
#SBATCH --time=6:00:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G


source /project/def-eroussea/projects/test/env_empathi/bin/activate

python3 -m build
