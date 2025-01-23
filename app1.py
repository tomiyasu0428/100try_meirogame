import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

# 迷路のサイズ
maze_width = 10
maze_height = 10

# 迷路の初期化 (0: 通路, 1: 壁)
maze = [[0 for _ in range(maze_width)] for _ in range(maze_height)]

# スタートとゴールの位置を設定
start_x, start_y = 0, 0
goal_x, goal_y = maze_width - 1, maze_height - 1

# プレイヤーの初期位置
player_x, player_y = start_x, start_y

# 壁をランダムに配置（簡単にするために非常に少ない壁）
for i in range(maze_height):
    for j in range(maze_width):
        if random.random() < 0.2:  # 20%の確率で壁を生成
            maze[i][j] = 1

# スタートとゴールは壁にしない
maze[start_y][start_x] = 0
maze[goal_y][goal_x] = 0


# 描画関数
def draw_maze():
    global fig, ax  # draw_maze関数内で fig, ax を更新するから必要
    plt.close(fig)  # 前回の描画をクリア
    fig, ax = plt.subplots()
    ax.set_xlim(-1, maze_width)
    ax.set_ylim(-1, maze_height)
    ax.set_aspect("equal")

    # 迷路を描画
    for y in range(maze_height):
        for x in range(maze_width):
            if maze[y][x] == 1:
                ax.add_patch(patches.Rectangle((x, maze_height - 1 - y), 1, 1, facecolor="black"))

    # プレイヤーを描画
    player = patches.Circle((player_x + 0.5, maze_height - 1 - player_y + 0.5), 0.4, facecolor="red")
    ax.add_patch(player)

    # スタートとゴールを描画
    ax.add_patch(patches.Rectangle((start_x, maze_height - 1 - start_y), 1, 1, facecolor="green"))
    ax.add_patch(patches.Rectangle((goal_x, maze_height - 1 - goal_y), 1, 1, facecolor="blue"))

    plt.show()


# キーボードイベント処理
def on_key(event):
    global player_x, player_y, fig, ax

    if event.key == "up":
        if player_y > 0 and maze[player_y - 1][player_x] == 0:
            player_y -= 1
    elif event.key == "down":
        if player_y < maze_height - 1 and maze[player_y + 1][player_x] == 0:
            player_y += 1
    elif event.key == "left":
        if player_x > 0 and maze[player_y][player_x - 1] == 0:
            player_x -= 1
    elif event.key == "right":
        if player_x < maze_width - 1 and maze[player_y][player_x + 1] == 0:
            player_x += 1

    # ゴール判定
    if player_x == goal_x and player_y == goal_y:
        print("Congratulations! You reached the goal!")
        plt.close()  # ウィンドウを閉じる
        return

    draw_maze()


# `draw_maze()` の外で fig, ax を作成し、イベントハンドラを登録
fig, ax = plt.subplots()
fig.canvas.mpl_connect("key_press_event", on_key)

# 初期描画
draw_maze()
plt.show()
