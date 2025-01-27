import sys
import os
import logging

from module.game import Game


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/module")

if __name__ == "__main__":
    try:
        logging.info("Запуск игры...")
        game = Game()
        game.run()
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
    finally:
        logging.info("Игра завершена.")
