import math


def limit_within_range(card, mouse_x, mouse_y):
    # 카드 사용자의 위치
    user_x, user_y = card.user.x, card.user.y

    # 마우스 위치와 사용자 위치 사이의 거리 계산
    dx = mouse_x - user_x
    dy = mouse_y - user_y
    distance = math.sqrt(dx ** 2 + dy ** 2)

    # 거리가 범위를 초과하면 제한
    if distance > card.range:
        # 각도 계산
        angle = math.atan2(dy, dx)
        # 제한된 위치 계산
        limited_x = user_x + card.range * math.cos(angle)
        limited_y = user_y + card.range * math.sin(angle)
    else:
        # 범위 내에 있으면 마우스 위치 그대로 사용
        limited_x, limited_y = mouse_x, mouse_y

    return limited_x, limited_y