# world[0]: layer 0 - background
# world[1]: layer 1 - team_color
# world[2]: layer 2 - main_weapon
# world[3]: layer 3 - character
# world[4]: layer 4 - sub_weapon
# ...
# world[8]: layer 8 - effect
# world[9]: layer 9 - ui
from damage_number import DamageNumberPool

world = [[] for _ in range(10)]
damage_number_pool = None

def init():
    global damage_number_pool
    damage_number_pool = DamageNumberPool(size=100)  # 크기는 필요에 따라 조정
    add_object(damage_number_pool, 8)  # 이펙트 레이어에 추가

def add_object(obj, depth):
    world[depth].append(obj)

# @profile
def update():
    for layer in world:
        for obj in layer:
            obj.update()
        # y 좌표에 따라 객체 정렬
        layer.sort(key=lambda obj: -obj.y if hasattr(obj, 'y') else 0, reverse=False)

# @profile
def render():
    for layer in world:
        for obj in layer:
            obj.draw()

def remove_object(obj):
    for layer in world:
        if obj in layer:
            layer.remove(obj)
            return
    print(f'CRITICAL: 존재하지 않는 객체{obj}를 지우려 합니다.')

def change_object_layer(obj, layer_to):
    for layer in world:
        if obj in layer:
            layer.remove(obj)
            world[layer_to].append(obj)
            print(f'Object {obj} moved to layer {layer_to}')
            return
    print(f'CRITICAL: 객체 {obj}를 찾을 수 없습니다.')