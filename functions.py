#!/usr/bin/env python
def sign(number):
    return 1 if number >= 0 else -1


def col(color):
    color = color[1:-1].split(',')
    color = (int(n) for n in color)
    return tuple(color)


def backoff(object1, object2):
    object1, object2 = object2, object1
    print 'backoff'
    print object1.id, object2.id

    pos = object1.pos
    obj = object2.rect

    left = pos.x + object1.rect.width / 2 - obj.left
    right = obj.right - (pos.x - object1.rect.width / 2)
    top = pos.y - obj.top
    bot = obj.bottom - (pos.y - object1.rect.height)
    # print 'left: %s, right: %s, top: %s, bot: %s' % (left, right, top, bot)
    minimum = min(left, right, top, bot)
    # print minimum

    def reset_vel_and_acc(direction):
        setattr(object1.vel, direction, 0)
        setattr(object1.acc, direction, 0)

    def put_on_left():
        print 'put_on_left'
        print 12, pos
        pos.x = obj.left - object1.rect.width / 2
        print 13, pos
        object1.touch_right = object2
        print 14, pos
        reset_vel_and_acc('x')
        print 15, pos

    def put_on_right():
        print 'put_on_right'
        print 16, pos
        pos.x = obj.right + object1.rect.width / 2
        print 17, pos
        object1.touch_left = object2
        print 18, pos
        reset_vel_and_acc('x')
        print 19, pos

    def put_on_top():
        pos.y = obj.top
        object1.touch_bot = object2
        reset_vel_and_acc('y')

    def put_on_bot():
        pos.y = obj.bottom + object1.rect.height
        reset_vel_and_acc('y')

    if left == minimum:
        put_on_left()
    if right == minimum:
        put_on_right()
    if top == minimum:
        put_on_top()
    if bot == minimum:
        if object1.vel.y < 0:
            put_on_bot()
        elif object1.vel.y > 0:
            put_on_top()
        elif object1.vel.x > 0:
            put_on_left()
        elif object1.vel.x < 0:
            put_on_right()


def backoff3(player, object):

    pos = player.pos
    obj = object.rect

    left = pos.x + player.rect.width / 2 - obj.left
    right = obj.right - (pos.x - player.rect.width / 2)
    top = pos.y - obj.top
    bot = obj.bottom - (pos.y - player.rect.height)
    # print 'left: %s, right: %s, top: %s, bot: %s' % (left, right, top, bot)
    minimum = min(left, right, top, bot)
    # print minimum

    def reset_vel_and_acc(direction):
        setattr(player.vel, direction, 0)
        setattr(player.acc, direction, 0)

    def put_on_left():
        pos.x = obj.left - player.rect.width / 2
        player.touch_right = object
        reset_vel_and_acc('x')

    def put_on_right():
        pos.x = obj.right + player.rect.width / 2
        player.touch_left = object
        reset_vel_and_acc('x')

    def put_on_top():
        pos.y = obj.top
        player.touch_bot = object
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
