from lerobot.common.datasets.lerobot_dataset import LeRobotDataset
import torch
import numpy as np

NUM_COLS = 8
NUM_ROWS = 3
if __name__ == "__main__":
    dataset = LeRobotDataset(
        repo_id="lirislab/guess_who_lighting",
    )
    hf_dataset = dataset.hf_dataset
    grid_pos = [""] * len(dataset)

    current_episode = -1
    idx = 0
    current_grid = (0, 0)
    for i, item in enumerate(hf_dataset):
        episode_id = item["episode_index"].item()
        if episode_id != current_episode:
            current_episode = episode_id
            if current_episode == 45:
                idx -= 1
            current_grid= [(idx // NUM_COLS) % NUM_ROWS, idx % NUM_COLS]
            idx += 1
        grid_pos[i] = np.array(current_grid)

    hf_dataset = hf_dataset.remove_columns(['grid_position'])
    hf_dataset = hf_dataset.add_column('grid_position', grid_pos)

    dataset.hf_dataset = hf_dataset
    dataset.save_modified_dataset()
    
    