import time
from pathlib import Path
from pynput.keyboard import Controller

K = Controller()

class Player:
    def __init__(self, music: str, interval: float = 0.1) -> None:
        self.music = music.replace('\n', '').lower()
        self.interval = interval
        self.idx = 0
        self.end = len(self.music)

    def next(self) -> str:
        self.idx += 1
        return self.music[self.idx - 1]

    def until(self, ch: str) -> str:
        ret = []
        while (c := self.next()) != ch:
            ret.append(c)
        return ''.join(ret)
    
    @property
    def is_end(self):
        return self.idx >= self.end

    def sleep(self):
        time.sleep(self.interval)

    def half_sleep(self):
        time.sleep(self.interval / 2)

    def click(self, keys: str):
        for key in keys:
            K.press(key)
        self.half_sleep()
        for key in keys:
            K.release(key)
        self.half_sleep()

    def play(self):
        while not self.is_end:
            match self.next():
                case ' ':
                    self.sleep()
                case '#':
                    self.interval *= float(self.until('#'))
                case '$':
                    self.interval /= float(self.until('$'))
                case '(':
                    self.click(self.until(')'))
                case _ as key:
                    self.click(key)



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
    Player(music_file.read_text(encoding='utf8'), args.interval).play()
