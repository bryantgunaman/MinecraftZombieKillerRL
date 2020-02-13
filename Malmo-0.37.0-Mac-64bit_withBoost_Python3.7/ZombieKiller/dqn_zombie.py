from main_keras import MainKeras


if __name__ == '__main__':
    with open('zombie_kill_1.xml', 'r') as file:
        mission_file = file.read().replace('\n', '')
        mk = MainKeras(mission_file, n_games=25, max_retries=3)
        mk.run_dqn()