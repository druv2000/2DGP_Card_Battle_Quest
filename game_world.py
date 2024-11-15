# world[0]: layer 0 - background
# world[1]: layer 1 - team_color
# world[2]: layer 2 -
# world[3]: layer 3 - enemy_character
# world[4]: layer 4 - ally_character
# ...
# world[8]: layer 8 - effect
# world[9]: layer 9 - ui
from attack_animation import Mage_AttackBullet, Bowman_AttackBullet, Soldier_Mage_AttackBullet, None_AttackBullet
from object_pool import BulletPool, HitAnimationPool, DamageNumberPool, AttackAnimationPool

world = [[] for _ in range(10)]
damage_number_pool = None
mage_bullet_pool = None
bowman_bullet_pool = None
soldier_mage_bullet_pool = None
none_bullet_pool = None
hit_animation_pool = None
attack_animation_pool = None


def init():
    global damage_number_pool
    global mage_bullet_pool, bowman_bullet_pool, soldier_mage_bullet_pool, none_bullet_pool
    global hit_animation_pool
    global attack_animation_pool

    damage_number_pool = DamageNumberPool(size=1000)  # 크기는 필요에 따라 조정
    mage_bullet_pool = BulletPool(Mage_AttackBullet, size = 500)
    bowman_bullet_pool = BulletPool(Bowman_AttackBullet, size = 500)
    soldier_mage_bullet_pool = BulletPool(Soldier_Mage_AttackBullet, size = 500)
    none_bullet_pool = BulletPool(None_AttackBullet, size = 1000)
    hit_animation_pool = HitAnimationPool(size = 1500)
    attack_animation_pool = AttackAnimationPool(size = 1500)

    add_object(damage_number_pool, 8)  # 이펙트 레이어에 추가
    add_object(mage_bullet_pool, 7)
    add_object(bowman_bullet_pool, 7)
    add_object(soldier_mage_bullet_pool, 7)
    add_object(none_bullet_pool, 7)
    add_object(hit_animation_pool, 7)
    add_object(attack_animation_pool, 5)

def get_character_bullet(c):
    from character_list import Mage, Bowman, Soldier_mage

    global mage_bullet_pool, bowman_bullet_pool, soldier_mage_bullet_pool
    if isinstance(c, Mage):
        return mage_bullet_pool.get(c.x, c.y, c, c.target)
    elif isinstance(c, Bowman):
        return bowman_bullet_pool.get(c.x, c.y, c, c.target)
    elif isinstance(c, Soldier_mage):
        return soldier_mage_bullet_pool.get(c.x, c.y, c, c.target)
    else:
        return none_bullet_pool.get(c.x, c.y, c, c.target)

#======================================================================

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

def clear():
    for layer in world:
        layer.clear()