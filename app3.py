import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

# 初期設定
maze = np.array(
    [
        [1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1],
    ]
)

player_pos = [1, 1]  # プレイヤー初期位置
goal_pos = [5, 5]  # ゴール位置


# 描画関数
def draw_maze():
    plt.clf()
    fig, ax = plt.subplots()
    ax.imshow(maze, cmap="gray", vmin=0, vmax=1)

    # プレイヤーを描画
    player_rect = Rectangle((player_pos[1] - 0.5, player_pos[0] - 0.5), 1, 1, color="blue")
    ax.add_patch(player_rect)

    # ゴールを描画
    goal_rect = Rectangle((goal_pos[1] - 0.5, goal_pos[0] - 0.5), 1, 1, color="green")
    ax.add_patch(goal_rect)

    plt.title("Matplotlib Maze Game")
    plt.axis("off")
    plt.draw()
    plt.pause(0.1)


# プレイヤーの移動関数
def move_player(key):
    global player_pos

    new_pos = player_pos.copy()

    if key == "up":
        new_pos[0] -= 1
    elif key == "down":
        new_pos[0] += 1
    elif key == "left":
        new_pos[1] -= 1
    elif key == "right":
        new_pos[1] += 1

    # 移動先が通路か確認
    if maze[new_pos[0], new_pos[1]] == 0:
        player_pos = new_pos


# メインループ
def main():
    print("Starting Matplotlib Maze Game...")
    plt.ion()
    draw_maze()

    try:
        while True:
            print("Use arrow keys (w=up, s=down, a=left, d=right) to move, q to quit.")
            key = input("Enter move: ").strip().lower()

            if key == "q":
                print("Game Quit.")
                break

            if key in ["w", "s", "a", "d"]:
                key_map = {"w": "up", "s": "down", "a": "left", "d": "right"}
                move_player(key_map[key])

                draw_maze()

                if player_pos == goal_pos:
                    print("Game Clear! Congratulations!")
                    break
            else:
                print("Invalid input. Please use w, a, s, d, or q.")

    except KeyboardInterrupt:
        print("\nGame interrupted. Exiting...")

    finally:
        plt.ioff()
        plt.show()


if __name__ == "__main__":
    main()
