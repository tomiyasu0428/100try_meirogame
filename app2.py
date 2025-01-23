import matplotlib.pyplot as plt
import numpy as np

# 迷路の定義 (1が壁、0が通路)
maze = np.array(
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
)

# スタートとゴールの位置
start = (1, 1)
goal = (8, 8)

# プレイヤーの初期位置
player_pos = list(start)

# 迷路を描画
fig, ax = plt.subplots()
ax.imshow(maze, cmap="binary")

# プレイヤーとゴールを描画
(player,) = ax.plot(player_pos[1], player_pos[0], "ro")
(goal_marker,) = ax.plot(goal[1], goal[0], "go")


# キー入力によるプレイヤーの移動
def on_key(event):
    global player_pos
    if event.key == "up":
        new_pos = (player_pos[0] - 1, player_pos[1])
    elif event.key == "down":
        new_pos = (player_pos[0] + 1, player_pos[1])
    elif event.key == "left":
        new_pos = (player_pos[0], player_pos[1] - 1)
    elif event.key == "right":
        new_pos = (player_pos[0], player_pos[1] + 1)
    else:
        return

    # 移動先が壁でないか確認
    if maze[new_pos] == 0:
        player_pos = list(new_pos)
        player.set_data(player_pos[1], player_pos[0])
        fig.canvas.draw()

    # ゴールに到達したか確認
    if tuple(player_pos) == goal:
        print("ゴールに到達しました！")
        plt.close()


# キーイベントのリスナーを設定
fig.canvas.mpl_connect("key_press_event", on_key)

plt.show()
