from PIL import Image
from io import BytesIO
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class Render:

    def __init__(self, mode_num):
        self.canvas = None
        self.theme = []
        img = Image.open(f'{CURRENT_DIR}/theme/{mode_num}{mode_num}.png')
        self.sl = 720 / mode_num
        for i in range(mode_num):  # 剪切图片
            for j in range(mode_num):
                self.theme.append(img.crop((j * self.sl, i * self.sl, (j + 1) * self.sl, (i + 1) * self.sl)))
        self.mode = mode_num

    def draw_puzzle(self, puzzle):  # 画图
        self.canvas = Image.new('RGB', (720, 720))
        for i in range(self.mode * self.mode):
            y, x = i % self.mode, i // self.mode
            xx, yy = int(x * self.sl), int(y * self.sl)
            self.canvas.paste(self.theme[puzzle[y][x] - 1], (xx, yy))

    def get_buf(self, puzzle):  # img转数据流
        self.draw_puzzle(puzzle)
        buf = BytesIO()
        self.canvas.save(buf, format='png')
        return buf


if __name__ == '__main__':
    from puzzle_py import PuzzleCore
    mode = 5
    ctx = Render(mode)
    pz = PuzzleCore(mode)
    ctx.draw_puzzle(pz.get_puzzle())
    ctx.canvas.save(f'{CURRENT_DIR}/test5.png')
