from main_keras import MainKeras


if __name__ == '__main__':
    mk = MainKeras('zombie_kill_1.xml', n_games=25, max_retries=3, 
                    starting_zombies=1, XSize=10, ZSize=10)
    mk.run_dqn()