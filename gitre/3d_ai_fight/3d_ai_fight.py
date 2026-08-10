from ursina import *

app = Ursina()

'''--- adatok eltűntetése ---'''
window.fps_counter.enabled = False
window.exit_button.enabled = False
window.entity_counter.enabled = False
window.collider_counter.enabled = False

'''--- változók ---'''
magassag = 0
eses = False
tamado_hp = 20
player_hp = 100
all = True
jatek_megy = True
nyeres = False
vesztes = False

'''--- fullscreen mód ---'''
window.fullscreen = True

'''--- kamerabeállítások ---'''
camera.position = Vec3(499, 0, 499)
kamera_mozgasvektora = Vec3(0, 0, 0)
camera.rotation_x = 0
camera.rotation_y = 0
camera.lens.fov = 130
scene.fog_density = 0
scene.fog_color = color.rgb(120, 130, 140)
Sky(color = color.blue)

'''--- enitity-k ---'''
tamado = Entity(model = '3d_ai_fight_kepek/robot_1.glb', position = Vec3(-499, 0, -499), collider = 'box')

placc = Entity(model = 'plane', position = Vec3(0, -10, 0), scale = Vec3(1000, 1, 1000), texture = '3d_ai_fight_kepek/fu.png', texture_scale = (50, 50))
fal_1 = Entity(model = 'cube', position = Vec3(500, 0, 0), scale = Vec3(1, 50, 1000), texture = '3d_ai_fight_kepek/ko.png', texture_scale = (15.36, 1.024))
fal_2 = Entity(model = 'cube', position = Vec3(-500, 0, 0), scale = Vec3(1, 50, 1000), texture = '3d_ai_fight_kepek/ko.png', texture_scale = (15.36, 1.024))
fal_3 = Entity(model = 'cube', position = Vec3(0, 0, 500), scale = Vec3(1000, 50, 1), texture = '3d_ai_fight_kepek/ko.png', texture_scale = (15.36, 1.024))
fal_4 = Entity(model = 'cube', position = Vec3(0, 0, -500), scale = Vec3(1000, 50, 1), texture = '3d_ai_fight_kepek/ko.png', texture_scale = (15.36, 1.024))

kereszt = Text('+', scale = 2, color = color.white)
hp = Text(f'{player_hp}', scale = 1.5, color = color.white, position = (-0.8, 0.49))
bos_bar = Text(f'      Robot     \n{"-" * tamado_hp}', scale = 3, color = color.red, position = (-0.15, 0.49))
szoveg_1 = Text('Gratulálok, nyertél!\nEnterrel újrakezdheted\na játékot', scale = 4, color = color.green, position = (-0.4, 0))
szoveg_2 = Text('Vesztettél!\nEnterrel újrakezdheted\na játékot', scale = 4, color = color.red, position = (-0.4, 0))
szoveg_1.enabled = False
szoveg_2.enabled = False

ranezes = raycast(camera.world_position, camera.forward, distance = 8, ignore = [camera])

speed_tamado = 1
speed_player = 1.5
sensitivity = 100
mouse.locked = True

'''--- függvények ---'''
def utes_1():
    global tamado_hp
    ranezes = raycast(camera.world_position, camera.forward, distance=10, ignore=[camera])
    if ranezes.hit and ranezes.entity == tamado:
        tamado_hp -= 1

def utes_2():
    global tamado_hp
    ranezes = raycast(camera.world_position, camera.forward, distance=10, ignore=[camera])
    if ranezes.hit and ranezes.entity == tamado:
        tamado_hp -= 2

def input(key):
    global bos_bar
    if key == 'left mouse down' and magassag == 0 and not all:
        utes_1()
        destroy(bos_bar)
        bos_bar = Text(f'      Robot     \n{"-" * tamado_hp}', scale=3, color=color.red, position=(-0.15, 0.49))
    elif key == 'left mouse up' and not all:
        utes_2()
        destroy(bos_bar)
        bos_bar = Text(f'      Robot     \n{"-" * tamado_hp}', scale=3, color=color.red, position=(-0.15, 0.49))

def update():
    global kamera_mozgasvektora, magassag, eses, speed_player, player_hp, tamado_hp, hp, all, jatek_megy, nyeres, vesztes, szoveg, bos_bar
    if held_keys['escape']:
        quit()

    if jatek_megy:
        '''--- követ a gyerök ---'''
        tamado.look_at(camera)
        if distance(tamado.position, camera.position) > 2:
            tamado.position += tamado.forward * speed_tamado
        tamado.y = 0

        '''--- forgás ---'''
        camera.rotation_y += mouse.velocity[0] * sensitivity
        camera.rotation_x -= mouse.velocity[1] * sensitivity

        '''--- mozgás ---'''
        kamera_mozgasvektora = Vec3(0, 0, 0)
        all = True
        if held_keys['up arrow'] or held_keys['w']:
            kamera_mozgasvektora += camera.forward
            all = False
        if held_keys['down arrow'] or held_keys['s']:
            kamera_mozgasvektora -= camera.forward
            all = False
        if held_keys['left arrow'] or held_keys['a']:
            kamera_mozgasvektora -= camera.right
            all = False
        if held_keys['right arrow'] or held_keys['d']:
            kamera_mozgasvektora += camera.right
            all = False
        camera.y = magassag

        camera.position += kamera_mozgasvektora.normalized() * speed_player

        camera.rotation_x = clamp(camera.rotation_x, -85, 85)

        '''--- ne menj ki ---'''
        if camera.x > 499:
            camera.x = 499
        if camera.x < -499:
            camera.x = -499
        if camera.z > 499:
            camera.z = 499
        if camera.z < -499:
            camera.z = -499

        if tamado.x > 499:
            tamado.x = 499
        if tamado.x < -499:
            tamado.x = -499
        if tamado.z > 499:
            tamado.z = 499
        if tamado.z < -499:
            tamado.z = -499

        '''--- ugrás ---'''
        if held_keys['space']:
            magassag += 1
        else:
            magassag -= 1
        if magassag <= 0:
            magassag = 0
            eses = False
        if magassag > 20:
            magassag = 20
            eses = True
        if eses:
            held_keys['space'] = False

        '''--- bugmentesítés ---'''
        tamado.rotation_z = 0

        '''ugrásnál gyorsabb'''
        if magassag > 0:
            speed_player += 0.01
        else:
            speed_player = 1.5

    '''--- játékos támad ---'''
    if tamado_hp <= 0:
        jatek_megy = False
        nyeres = True
        vesztes = False

    '''--- szörny támad ---'''
    if distance(tamado.position, camera.position) < 5:
        player_hp -= 1
        destroy(hp)
        hp = Text(f'{player_hp}', scale=1.5, color=color.white, position=(-0.8, 0.49))
    if player_hp <= 0:
        jatek_megy = False
        nyeres = False
        vesztes = True

    if not jatek_megy:
        if nyeres:
            camera.y = -500
            hp.enabled = False
            bos_bar.enabled = False
            szoveg_1.enabled = True
            camera.look_at((0, -1000, 0))
            kereszt.elabed = False

        if vesztes:
            camera.y = -500
            hp.enabled = False
            bos_bar.enabled = False
            szoveg_2.enabled = True
            camera.look_at((0, -1000, 0))
            kereszt.elabed = False

        if held_keys['enter']:
            camera.position = Vec3(499, 0, 499)
            tamado.position = Vec3(-499, 0, -499)
            player_hp = 100
            tamado_hp = 20
            hp.enabled = True
            bos_bar.enabled = True
            szoveg_1.enabled = False
            szoveg_2.enabled = False
            nyeres = False
            vesztes = False
            jatek_megy = True
            kereszt.elabed = True
            destroy(bos_bar)
            bos_bar = Text(f'      Robot     \n{"-" * tamado_hp}', scale=3, color=color.red, position=(-0.15, 0.49))
            destroy(hp)
            hp = Text(f'{player_hp}', scale=1.5, color=color.white, position=(-0.8, 0.49))
            camera.look_at((0, 0, 100))
            camera.rotation_z = 0

app.run()