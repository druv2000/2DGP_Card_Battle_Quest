# game_world.py
from uniform_grid import UniformGrid

# world[0]: layer 0 - background
# world[1]: layer 1 - area_ui
# world[2]: layer 2 -
# world[3]: layer 3 - enemy_character
# world[4]: layer 4 - ally_character
# ...
# world[8]: layer 8 - effect
# world[9]: layer 9 - ui

world = [[] for _ in range(10)]
collision_pairs = {}
grid = UniformGrid(1600, 900, 100)  # 1600x900 게임 화면, 100x100 셀 크기



#======================================================================

def add_object(obj, depth):
    world[depth].append(obj)
    grid.add_object(obj)


def add_objects(ol, depth = 0): #list 추가하기
    world[depth] += ol

def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [[], []]

    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

# @profile
def update():
    for layer in world:
        for obj in layer:
            obj.update()
            grid.update_object(obj)
        # y 좌표에 따라 동일 레이어 내 객체 정렬
        layer.sort(key=lambda obj: -obj.y if hasattr(obj, 'y') else 0, reverse=False)

# @profile
def render():
    for layer in world:
        for obj in layer:
            obj.draw()

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            break
    grid.remove_object(o)


def remove_collision_object(o, group=None):
    if group:
        # 특정 그룹에서만 객체 제거
        if group in collision_pairs:
            if o in collision_pairs[group][0]:
                collision_pairs[group][0].remove(o)
            if o in collision_pairs[group][1]:
                collision_pairs[group][1].remove(o)
    else:
        # 모든 그룹에서 객체 제거
        groups_to_remove = []
        for group, pairs in collision_pairs.items():
            if o in pairs[0]:
                pairs[0].remove(o)
            if o in pairs[1]:
                pairs[1].remove(o)
            # 그룹이 비어있으면 제거 대상에 추가
            if not pairs[0] and not pairs[1]:
                groups_to_remove.append(group)

        # 비어있는 그룹 제거
        for group in groups_to_remove:
            del collision_pairs[group]

def change_object_layer(obj, layer_to):
    for layer in world:
        if obj in layer:
            layer.remove(obj)
            world[layer_to].append(obj)
            print(f'Object {obj} moved to layer {layer_to}')
            return
    print(f'CRITICAL: 객체 {obj}를 찾을 수 없습니다.')

def clear():
    for layer in world:
        layer.clear()

def collide(group, a, b):
    if not a.is_active or not b.is_active:
        remove_collision_object(a, group)
        remove_collision_object(b, group)
        print(f'    DEBUG: {a.is_active}, {b.is_active} -> so deleted')
        return False

    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            if not a.is_active:
                continue

            # UniformGrid를 사용하여 근처의 객체만 사용
            nearby_objects = grid.get_nearby_objects(a.x, a.y, a.collision_radius)

            for b in nearby_objects:
                if b in pairs[1] and b.is_active and a != b:
                    if collide(group, a, b):
                        print(f'{group} collide')
                        a.handle_collision(group, b)
                        b.handle_collision(group, a)


