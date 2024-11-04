# world[0]: layer 0 - background 1
# world[1]: layer 1 - character
# world[2]: layer 2 - background 2
world = [[], [], []]

def add_object(obj, depth):
    world[depth].append(obj)

def update():
    for layer in world:
        for obj in layer:
            obj.update()
    return None

def render():
    for layer in world:
        for obj in layer:
            obj.draw()
    return None

def remove_object(obj):
    for layer in world:
        if obj in layer:
            layer.remove(obj)
            return

    print(f'CRITICAL: 존재하지 않는 객체{obj}를 지우려 합니다.')
    pass