# world[0]: layer 0 - background
# world[1]: layer 1 - team_color
# world[2]: layer 2 - main_weapon
# world[3]: layer 3 - character
# world[4]: layer 4 - sub_weapon
# ...
# world[8]: layer 8 - effect
# world[9]: layer 9 - ui
world = [[] for _ in range(10)]

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