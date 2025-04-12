#!/bin/sh

#SBATCH --job-name=train_act_guesswho
#SBATCH --output=logs/train_act_guesswho.%j.out
#SBATCH --error=logs/train_act_guesswho.%j.err 

#SBATCH --partition=gpu
#SBATCH --gres=gpu:quadro_rtx_6000:1
#SBATCH --nodes=1
#SBATCH --mem=180G
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH -t 20:00:00

echo ${SLURM_NODELIST}

source ~/.bashrc
conda activate hack
export PYTHONPATH=.
export HYDRA_FULL_ERROR=1

srun python lerobot/scripts/train.py \
    --dataset.repo_id="[lirislab/whoso100]" \
    --policy.type=act \
    --output_dir="/home/achapin/lerobot_jds/outputs/train/guess_who_test" \
    --job_name=guess_who_test  \
    --policy.use_vae=true \
    --policy.device=cuda \
    --num_workers=8 \
    --wandb.enable=true \
    --wandb.project="MistralHack" \
    --steps 50000
