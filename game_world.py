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
        # 각 객체 업데이트
        for obj in layer:
            obj.update()

        # y 좌표에 따라 객체 정렬 (y가 큰 값이 먼저 오도록)
        layer.sort(key=lambda obj: -obj.y if hasattr(obj, 'y') else 0, reverse=False)

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

    # 객체를 찾지 못한 경우
    print(f'CRITICAL: 존재하지 않는 객체{obj}를 지우려 합니다.')
    pass


def change_object_layer(obj, layer_to):
    for layer in world:
        if obj in layer:
            layer.remove(obj)
            world[layer_to].append(obj)
            print(f'Object {obj} moved to layer {layer_to}')
            return

    # 객체를 찾지 못한 경우
    print(f'CRITICAL: 객체 {obj}를 찾을 수 없습니다..')

