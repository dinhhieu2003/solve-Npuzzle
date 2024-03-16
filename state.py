def transform(state, action, M, N):
    # type(state) = tuple
    fake_state = [*state]
    blank_index = fake_state.index(0)
    match action:
        case 'u':
            if blank_index >= N:
                fake_state[blank_index], fake_state[blank_index - N] = \
                    fake_state[blank_index - N], fake_state[blank_index]
        case 'd':
            if blank_index + N <= M * N - 1:
                fake_state[blank_index], fake_state[blank_index + N] = \
                    fake_state[blank_index + N], fake_state[blank_index]
        case 'l':
            if blank_index % N != 0:
                fake_state[blank_index], fake_state[blank_index - 1] = \
                    fake_state[blank_index - 1], fake_state[blank_index]
        case 'r':
            if blank_index % N != N - 1:
                fake_state[blank_index], fake_state[blank_index + 1] = \
                    fake_state[blank_index + 1], fake_state[blank_index]
    return tuple(fake_state)

def transform_cost(state, action, M, N, fn, cost, g):
    # type(state) = tuple
    fake_state = [*state]
    blank_index = fake_state.index(0)
    match action:
        case 'u':
            if blank_index >= N:
                fake_state[blank_index], fake_state[blank_index - N] = \
                    fake_state[blank_index - N], fake_state[blank_index]
        case 'd':
            if blank_index + N <= M * N - 1:
                fake_state[blank_index], fake_state[blank_index + N] = \
                    fake_state[blank_index + N], fake_state[blank_index]
        case 'l':
            if blank_index % N != 0:
                fake_state[blank_index], fake_state[blank_index - 1] = \
                    fake_state[blank_index - 1], fake_state[blank_index]
        case 'r':
            if blank_index % N != N - 1:
                fake_state[blank_index], fake_state[blank_index + 1] = \
                    fake_state[blank_index + 1], fake_state[blank_index]
    return tuple(fake_state), fn(cost, tuple(fake_state), g+1), g+1

def get_neighbor(current_state, M, N):
    actions = ['u', 'd', 'l', 'r']
    neighbor = []
    for action in actions:
        fake_state = transform(current_state, action,M ,N)
        neighbor.append((fake_state, action))
    return neighbor

def get_neighbor_cost(current_state, M, N, fn, cost, g):
    actions = ['u', 'd', 'l', 'r']
    neighbor = []
    for action in actions:
        fake_state, state_cost, g = transform_cost(current_state, action, M, N, fn, cost, g)
        neighbor.append((state_cost, (fake_state, action, g)))
    return neighbor