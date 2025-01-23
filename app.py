import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random


class MazeGame:
    def __init__(self, maze_size=21):
        self.maze_size = maze_size
        self.maze = self.generate_maze_wall_extension(maze_size)
        self.player_pos = self.find_start_pos()
        self.goal_pos = self.find_goal_pos()

        self.fig, self.ax = plt.subplots()
        self.player = None
        self.goal = None

        self.draw_maze()
        self.draw_player()
        self.draw_goal()

        self.fig.canvas.mpl_connect("key_press_event", self.on_key_press)
        plt.show()

    def generate_maze_wall_extension(self, size):
        """
        壁伸ばし法で迷路を生成する関数。

        Args:
            size: 迷路の一辺のサイズ（正方形を想定）

        Returns:
            NumPy配列で表現された迷路（0: 通路, 1: 壁）
        """

        # 迷路を初期化（すべて通路）
        maze = np.zeros((size, size), dtype=int)

        # スタートとゴール地点を設定
        start_y = random.randint(1, size - 2)
        goal_y = random.randint(1, size - 2)
        start = (start_y, 0)
        goal = (goal_y, size - 1)

        # スタートからゴールまでの経路を生成
        def generate_path(start, goal):
            path = set()
            path.add(start)
            stack = [(start, [start])]
            visited = set()

            while stack:
                (y, x), current_path = stack.pop()
                if (y, x) == goal:
                    return set(current_path)

                if (y, x) not in visited:
                    visited.add((y, x))
                    # 上下左右の移動
                    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                    random.shuffle(directions)

                    for dy, dx in directions:
                        new_y, new_x = y + dy, x + dx
                        if 0 <= new_y < size and 0 <= new_x < size and (new_y, new_x) not in visited:
                            new_path = current_path + [(new_y, new_x)]
                            stack.append(((new_y, new_x), new_path))
            return path

        # スタートからゴールまでの経路を確保
        safe_path = generate_path(start, goal)

        # 外周をランダムな壁にする（一部通路を残す）
        for i in range(size):
            if (
                random.random() < 0.6 and (i, 0) not in safe_path and (i, size - 1) not in safe_path
            ):  # 経路上にない場合のみ壁にする
                maze[i, 0] = 1  # 左端
                maze[i, -1] = 1  # 右端
            if (
                random.random() < 0.6 and (0, i) not in safe_path and (size - 1, i) not in safe_path
            ):  # 経路上にない場合のみ壁にする
                maze[0, i] = 1  # 上端
                maze[-1, i] = 1  # 下端

        # 壁を伸ばし始める座標の候補
        start_points = []
        for y in range(1, size - 1):
            for x in range(1, size - 1):
                if (y % 2 == 0 and x % 2 == 0) or random.random() < 0.3:
                    start_points.append((y, x))
        random.shuffle(start_points)

        for start_y, start_x in start_points:
            # 経路上の点はスキップ
            if (start_y, start_x) in safe_path:
                continue

            # 既に壁が生成されている場合はスキップ
            if maze[start_y, start_x] == 1:
                continue

            wall_probability = 0.5
            if start_y in [1, size - 2] or start_x in [1, size - 2]:
                wall_probability = 0.7

            if random.random() < wall_probability:
                maze[start_y, start_x] = 1
                current_y, current_x = start_y, start_x

                extend_count = 0
                max_extends = 3

                while extend_count < max_extends:
                    directions = []
                    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        new_y, new_x = current_y + dy, current_x + dx
                        if (
                            0 < new_y < size - 1
                            and 0 < new_x < size - 1
                            and maze[new_y, new_x] == 0
                            and (new_y, new_x) not in safe_path
                        ):  # 経路上でない場合のみ壁を伸ばせる
                            directions.append((dy, dx))

                    if not directions:
                        break

                    dy, dx = random.choice(directions)
                    new_y, new_x = current_y + dy, current_x + dx

                    wall_probability = 0.5
                    if new_y in [1, size - 2] or new_x in [1, size - 2]:
                        wall_probability = 0.7

                    if random.random() < wall_probability:
                        maze[new_y, new_x] = 1
                        current_y, current_x = new_y, new_x
                        extend_count += 1

        # 通路の確保（迷路が解けることを保証）
        def ensure_solvable():
            path_count = np.sum(maze == 0)
            desired_path_ratio = 0.4
            while path_count / (size * size) < desired_path_ratio:
                y = random.randint(1, size - 2)
                x = random.randint(1, size - 2)
                if maze[y, x] == 1 and (y, x) not in safe_path:  # 経路上でない場合のみ通路に変更
                    maze[y, x] = 0
                    path_count += 1

        ensure_solvable()

        # スタートとゴールを設定
        maze[start_y, 0] = 0
        maze[goal_y, -1] = 0

        return maze

    def find_start_pos(self):
        """
        迷路のスタート位置(左端の列の通路)を探す。
        """
        for i in range(self.maze_size):
            if self.maze[i, 0] == 0:  # 左端の列で通路を探す
                return (i, 0)
        return None  # 見つからない場合（ここには到達しないはず）

    def find_goal_pos(self):
        """
        迷路のゴール位置(右端の列の通路)を探す。
        """
        for i in range(self.maze_size):
            if self.maze[i, self.maze_size - 1] == 0:  # 右端の列で通路を探す
                return (i, self.maze_size - 1)
        return None  # 見つからない場合（ここには到達しないはず）

    def draw_maze(self):
        """
        迷路を描画する。
        """
        self.ax.imshow(self.maze, cmap="gray_r", origin="upper")
        self.ax.set_xticks([])
        self.ax.set_yticks([])

    def draw_player(self):
        """
        プレイヤーを描画する。
        """
        y, x = self.player_pos
        self.player = patches.Circle((x + 0.5, y + 0.5), 0.4, color="red")
        self.ax.add_patch(self.player)

    def draw_goal(self):
        """
        ゴールを描画する。
        """
        y, x = self.goal_pos
        self.goal = patches.Rectangle((x + 0.2, y + 0.2), 0.6, 0.6, color="green")
        self.ax.add_patch(self.goal)

    def on_key_press(self, event):
        """
        キーボードが押されたときのイベントを処理する。
        """
        new_y, new_x = self.player_pos
        if event.key == "up":
            new_y -= 1
        elif event.key == "down":
            new_y += 1
        elif event.key == "left":
            new_x -= 1
        elif event.key == "right":
            new_x += 1

        if self.is_valid_move(new_y, new_x):
            self.player_pos = (new_y, new_x)
            self.update_player_position()

            if self.player_pos == self.goal_pos:
                self.show_game_clear()

    def is_valid_move(self, y, x):
        """
        移動先が有効かどうかを判定する。
        """
        if 0 <= y < self.maze_size and 0 <= x < self.maze_size and self.maze[y, x] == 0:
            return True
        return False

    def update_player_position(self):
        """
        プレイヤーの位置を更新する。
        """
        y, x = self.player_pos
        self.player.set_center((x + 0.5, y + 0.5))
        self.fig.canvas.draw()

    def show_game_clear(self):
        """
        ゲームクリアのメッセージを表示する。
        """
        self.ax.text(
            self.maze_size / 2,
            self.maze_size / 2,
            "Game Clear!",
            fontsize=20,
            color="blue",
            ha="center",
            va="center",
        )
        self.fig.canvas.draw()


if __name__ == "__main__":
    game = MazeGame(21)  # 迷路サイズ21x21(必ず奇数)
