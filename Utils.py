# TODO: Create helper function to see if snake takes double steps
# Example -> [310, 300] => [330, 300]

PREVIOUS_MOVE = None


def performing_double_steps(snake_head, food):
    PREVIOUS_MOVE = None

    if PREVIOUS_MOVE is None:
        PREVIOUS_MOVE = snake_head

    else:
        if abs(PREVIOUS_MOVE[0] - snake_head[0]) > 10 and PREVIOUS_MOVE[1] == snake_head[1]:
            print(f"double step in X [{PREVIOUS_MOVE[0]}] -> [{snake_head[0]}]")
        elif abs(PREVIOUS_MOVE[1] - snake_head[1]) > 10 and PREVIOUS_MOVE[0] == snake_head[0]:
            print(f"double step in Y [{PREVIOUS_MOVE[0]}] -> [{snake_head[0]}]")


def food_halo(food):
    X = food[0]
    Y = food[1]

    # Rings
    # [above, below, right, left, top-right-cor, top-left-cor, bottom-right-cor, bottom-left-cor]
    first_ring = [[X - 10, Y],
                  [X + 10, Y],
                  [X, Y + 10],
                  [X, Y - 10],
                  [X - 10, Y + 10],
                  [X - 10, Y - 10],
                  [X + 10, Y + 10],
                  [X + 10, Y - 10]]

    second_ring = [[X - 20, Y],
                   [X + 20, Y],
                   [X, Y + 20],
                   [X, Y - 20],
                   [X - 20, Y + 20],
                   [X - 20, Y - 20],
                   [X + 20, Y + 20],
                   [X + 20, Y - 20]]

    return first_ring, second_ring
