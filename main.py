import time
from pathlib import Path
from pynput.keyboard import Controller

K = Controller()


def play(music: str, interval: float = 0.1):
    music = music.replace('\n', '').lower()
    idx = 0
    while idx < len(music):
        if music[idx] == ' ':
            time.sleep(interval)
        else:
            keys = []
            if music[idx] == '(':
                idx += 1
                while music[idx] != ')':
                    keys.append(music[idx])
                    idx += 1
            else:
                keys.append(music[idx])
            for key in keys:
                K.press(key)
            time.sleep(interval / 2)
            for key in keys:
                K.release(key)
            time.sleep(interval / 2)
        idx += 1


if __name__ == '__main__':
    from argparse import ArgumentParser
    music_list = list[str]()
    for p in Path('data').iterdir():
        music_list.append(p.stem)
    parser = ArgumentParser()
    parser.add_argument('music', choices=music_list)
    parser.add_argument('--interval', '-I', type=float, default=0.1)
    args = parser.parse_args()
    music_file = Path('data') / Path(args.music)
    time.sleep(3)
    print('start')
    play(music_file.read_text(encoding='utf8'), args.interval)
