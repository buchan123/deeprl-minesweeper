from gym.envs.registration import register

register(
    id='minesweeper-v0',
    entry_point='gym_minesweeper.envs:Minesweeper',
)
