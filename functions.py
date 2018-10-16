#!/usr/bin/env python
def sign(number):
    return 1 if number >= 0 else -1


def col(color):
    color = color[1:-1].split(',')
    color = (int(n) for n in color)
    return tuple(color)


def backoff(player, object):
    if object.rect.left < player.pos.x < object.rect.right:
        player.pos.y = object.rect.y
    else:
        if player.pos.x < object.rect.left:
            player.pos.x =\
                object.rect.left - player.rect.width / 2
        if player.pos.x > object.rect.right:
            player.pos.x =\
                object.rect.right + player.rect.width / 2
    if player.pos.y == object.rect.top:
        player.touch_the_ground = True


def backoff2(player, object):
    print 'player.vel', player.vel
    print 2, 'abs(player.vel.x) > abs(player.vel.y)',\
        abs(player.vel.x) > abs(player.vel.y)
    if abs(player.vel.x) > abs(player.vel.y):
        if player.vel.x > 0:
            print 'player.vel.x > 0'
            player.pos.x =\
                object.rect.left - player.rect.width / 2
            player.vel.x = 0
            player.acc.x = 0
            # player.vel.x -= abs(player.vel.x)
        elif player.vel.x < 0:
            print 'player.vel.x < 0'
            player.pos.x =\
                object.rect.right + player.rect.width / 2
            player.vel.x = 0
            player.acc.x = 0
            # player.vel.x += abs(player.vel.x)
        else:
            print 'player.vel.x == 0', player.vel.x == 0
            exit(0)
    elif abs(player.vel.x) < abs(player.vel.y):
        if player.vel.y > 0:
            print 'player.vel.y > 0'
            player.pos.y = object.rect.y
            player.vel.y = 0
            player.acc.y = 0
        elif player.vel.y < 0 and not object.touch_the_ground:
            print 'player.vel.y < 0 and not player.touch_the_ground'
            print player.vel.y < 0 and not player.touch_the_ground
            print 'player.vel.y < 0'
            print player.vel.y < 0
            print 'not player.touch_the_ground'
            print not player.touch_the_ground
            player.pos.y = object.rect.bottom + player.rect.height
            print 'player.pos.y'
            print player.pos.y
            # exit(0)
            # player.vel.y += 300
            player.vel.y = 0
            player.acc.y = 0
    else:
        print 'abs(player.vel.x) == abs(player.vel.y)',\
            abs(player.vel.x) == abs(player.vel.y)
        exit()
    if player.pos.y == object.rect.top:
        player.touch_the_ground = True


def backoff3(player, object):

    pos = player.pos
    obj = object.rect

    left = pos.x + player.rect.width / 2 - obj.left
    right = obj.right - (pos.x - player.rect.width / 2)
    top = pos.y - obj.top
    bot = obj.bottom - (pos.y - player.rect.height)
    print 'left: %s, right: %s, top: %s, bot: %s' % (left, right, top, bot)
    minimum = min(left, right, top, bot)
    print minimum

    def reset_vel_and_acc(direction):
        setattr(player.vel, direction, 0)
        setattr(player.acc, direction, 0)

    def put_on_left():
        pos.x = obj.left - player.rect.width / 2
        reset_vel_and_acc('x')

    def put_on_right():
        pos.x = obj.right + player.rect.width / 2
        reset_vel_and_acc('x')

    def put_on_top():
        pos.y = obj.top
        player.touch_the_ground = True
        reset_vel_and_acc('y')

    def put_on_bot():
        pos.y = obj.bottom + player.rect.height
        reset_vel_and_acc('y')

    if left == minimum:
        put_on_left()
    if right == minimum:
        put_on_right()
    if top == minimum:
        put_on_top()
    if bot == minimum:
        if player.vel.y < 0:
            put_on_bot()
        elif player.vel.y > 0:
            put_on_top()
        elif player.vel.x > 0:
            put_on_left()
        elif player.vel.x < 0:
            put_on_right()


def apply_a_force(force, obj):
    pass
