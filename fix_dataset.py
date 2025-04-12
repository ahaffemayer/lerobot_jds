from lerobot.common.datasets.lerobot_dataset import LeRobotDataset
import torch

NUM_COLS = 8
NUM_ROWS = 3
if __name__ == "__main__":
    dataset = LeRobotDataset(
        repo_id="lirislab/guess_who_so100",
    )
    hf_dataset = dataset.load_hf_dataset()
    grid_pos = [torch.zeros((2, ), dtype=torch.float32)] * len(hf_dataset)

    current_episode = -1
    idx = 0
    current_grid = (0, 0)
    for i, item in enumerate(hf_dataset):
        episode_id = item["episode_index"].item()
        if episode_id != current_episode:
            current_episode = episode_id
            idx += 1
            if current_episode == 45 or current_episode == 64:
                
            current_grid= ((current_episode // NUM_COLS) % NUM_ROWS, current_episode % NUM_COLS)
            print(f"current_grid {current_grid}")
        if current_episode >= 40:
            break
        # grid_pos[i] = f"({episode_id // NUM_COLS}, {episode_id % NUM_COLS})"

    # hf_dataset.remove_columns(["episode_id"])
    # hf_dataset = hf_dataset.add_column("grid_pos", grid_pos)