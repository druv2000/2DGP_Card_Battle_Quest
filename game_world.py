world = [[] for _ in range(10)]

def add_object(obj, depth):
    world[depth].append(obj)

def update():
    for layer in world:
        for obj in layer:
            obj.update()
        layer.sort(key=lambda obj: -obj.y if hasattr(obj, 'y') else 0, reverse=False)

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
    print(f'CRITICAL: 객체 {obj}를 찾을 수 없습니다..')