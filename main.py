import pygame , time , json , sys , string , random , pathlib , math , random

pygame.init()
pygame.mixer.init()

WIDTH , HEIGHT = 1100 , 850
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

running = True

# sprites
class soul:
    sprite = pygame.image.load("SOUL.png").convert_alpha()
    sprite = pygame.transform.scale(sprite , (32 , 32))
    hitbox = pygame.Rect(450 , 430 , 25 , 25)
    hp = 92

class wall:
    def __init__(self , x , y , width , height):
        self.hitbox = pygame.Rect(x , y , width , height)

walls = [wall(400 , 310 , 10 , 300) , wall(700 , 300 , 10 , 300) , wall(400 , 300 , 300 , 10) , wall(410 , 600 , 300 , 10)]

FightMenuAssets = {}
FightMenuOrder = ["FIGHT" , "ACT" , "ITEM" , "MERCY"]
for name in FightMenuOrder:
    normal = pygame.image.load(f"assets/gui/{name}_BTN.png").convert_alpha()
    normal = pygame.transform.scale(normal , (230 , 90))
    active = pygame.image.load(f"assets/gui/{name}_A_BTN.png").convert_alpha()
    active = pygame.transform.scale(active , (230 , 90))
    FightMenuAssets[name] = {"normal": normal,
                    "active": active
                    }

SansSprites = {
    "heads": {},
    "torsos": {},
    "legs": {}
}

for file in pathlib.Path("assets/sans/heads").iterdir():
    sprite = pygame.image.load(file).convert_alpha()
    sprite = pygame.transform.scale(sprite , (125 , 125))
    sprite.set_colorkey((0 , 0 , 0))
    SansSprites["heads"][file.stem] = sprite

for file in pathlib.Path("assets/sans/torsos").iterdir():
    sprite = pygame.image.load(file).convert_alpha()
    if file.stem == "shrug":
        size = (275 , 100)
    else:
        size = (230 , 100)
    sprite = pygame.transform.scale(sprite , size)
    sprite.set_colorkey((0 , 0 , 0))
    SansSprites["torsos"][file.stem] = sprite

for file in pathlib.Path("assets/sans/legs").iterdir():
    sprite = pygame.image.load(file).convert_alpha()
    sprite = pygame.transform.scale(sprite , (160 , 90))
    sprite.set_colorkey((0 , 0 , 0))
    SansSprites["legs"][file.stem] = sprite

current_sans_frame = 0

SansSpritesAttack = {}
for attack in ["bone"]:
    sprite = pygame.image.load(f"assets/sans/attacks/{attack}.png").convert_alpha()
    sprite = pygame.transform.scale(sprite , (20 , 200))
    sprite.set_colorkey((0 , 0 , 0))
    hitbox = sprite.get_rect()
    SansSpritesAttack[attack] = {"sprite": sprite , "hitbox": hitbox}

SansSounds = {}
for sound in ["MEGALOVANIA"]:
    SansSounds[sound] = pygame.mixer.music.load(f"assets/sans/sounds/{sound}.mp3")

battle = True
played_theme = False

last_time = time.time()

font = pygame.font.Font("assets/fonts/DeterminationSansWebRegular-369X.ttf" , 65)
hpText = font.render(f"{soul.hp}/92" , True , (255 , 255 , 255) , None)
krText = font.render("KR" , True , (255 , 255 , 255) , None)

bar = pygame.Rect(450 , 655 , soul.hp * 2, 50)

def damageSoul(amount):
    global bar , hpText , soul
    bar = pygame.Rect(450 , 655 , soul.hp * 2, 50)
    hpText = font.render(f"{soul.hp}/92" , True , (255 , 255 , 255) , None)
    soul.hp -= amount
    pygame.mixer.Sound("assets/dmgTaken.mp3").play()
    

def nameSelection():
    global font
    letterSelected = "a"
    selected_index = 0
    name = ""
    upper_color = (255, 255, 255)
    finish_color = (255, 255, 255)
    letters = string.ascii_lowercase
    upper = False
    fadeOut = False
    bgColor = (0 , 0 , 0)
    bgTheme = pygame.mixer.Sound("assets/menu/startMenu.mp3")
    playedIntroNoise = False
    bgTheme.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if selected_index >= 26:
                        selected_index += 1
                    elif selected_index == 27:
                        pass
                    else:
                        selected_index = (selected_index + 1) % 27
                elif event.key == pygame.K_LEFT:
                    if selected_index == 26:
                        pass
                    else:
                        selected_index = (selected_index - 1) % 27
                elif event.key == pygame.K_DOWN:
                    if selected_index + 9 >= 25:
                        if selected_index >= 22:
                            selected_index = 27
                        else:
                            selected_index = 26
                    else:
                        selected_index = min(selected_index + 9, 25)
                elif event.key == pygame.K_UP:
                    if selected_index >= 26:
                        selected_index -= 5
                    else:
                        selected_index = max(selected_index - 9, -1)
                elif event.key == pygame.K_RETURN:
                    if selected_index == 26:
                        if upper:
                            letters = [letter.lower() for letter in letters]
                            upper = False
                        else:
                            letters = [letter.upper() for letter in letters]
                            upper = True
                    elif selected_index >= 27:
                        if len(name) < 3:
                            pygame.mixer.Sound("assets/menu/error.mp3").play()
                        else:
                            fadeOut = True
                    else:
                        if len(name) < 6:
                            name += letters[selected_index]

        if fadeOut:
            selected_index = -1
            bgTheme.stop()
            bgColor = tuple(min(255, c + 1.8) for c in bgColor)
            if not playedIntroNoise:
                pygame.mixer.Sound("assets/menu/introNoise.mp3").play()
                playedIntroNoise = True
            if bgColor == (255 , 255 , 255):
                time.sleep(1)
                with open(f"{pathlib.Path(__file__).resolve().parent}/config.json" , "w") as file:
                    config = {
                        "name": name,
                        "lvl": 19
                    }
                    json.dump(config , file)
                break

        screen.fill(bgColor)
      
        for i , letter in enumerate(letters):
            if selected_index == i:
                color = (255 , 255 , 0)
            else:
                color = (255 , 255 , 255)
         
            if i < 9:
                screen.blit(font.render(letter , True , color , None) , ((i + 1) * random.randint(99 , 100) , random.randint(299 , 300)))
            elif i < 18:
                screen.blit(font.render(letter , True , color, None) , ((i - 8) * random.randint(99 , 100) , random.randint(399 , 400)))
            else:
                screen.blit(font.render(letter , True , color , None) , ((i - 17) * random.randint(99 , 100) , random.randint(499 , 500)))

        screen.blit(font.render(name , True , (255 , 255 , 255) , None) , (random.randint(427 , 430) , random.randint(157 , 160)))
        screen.blit(font.render("Choose your name" , True , (255 , 255 , 255) , None) , (random.randint(317 , 320) , random.randint(47 , 50)))

        if selected_index >= 26:
            if selected_index == 26:
                upper_color = (255 , 255 , 0)
                finish_color = (255 , 255 , 255)
            elif selected_index == 27:
                finish_color = (255 , 255 , 0)
                upper_color = (255 , 255 , 255)
        else:
            finish_color = (255 , 255 , 255)
            upper_color = (255 , 255 , 255)

        screen.blit(font.render("upper" , True , upper_color , None) , (random.randint(217 , 220) , random.randint(597 , 600)))
        screen.blit(font.render("finish" , True , finish_color , None) , (random.randint(597 , 600) , random.randint(597 , 600)))

        pygame.display.flip()
        clock.tick(30)
          
def loadConfig():
    global config
    try:
        with open("config.json" , "r") as file:
            config = json.load(file)
    except (FileNotFoundError , json.JSONDecodeError):
        nameSelection()
        loadConfig()

loadConfig()

if isinstance(config["name"] , int) or len(config["name"]) > 6:
    playedSecret = False
    temSong = pygame.mixer.Sound("assets/menu/tem/hOI!.mp3")
    tem = pygame.image.load("assets/menu/tem/tem.png").convert_alpha()
    tem = pygame.transform.scale(tem , (300 , 300))
    tem.set_colorkey((0 , 0 , 0))
    temstand = pygame.image.load("assets/menu/tem/temStand.png").convert_alpha()
    temstand = pygame.transform.scale(temstand , (450 , 300))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        if not playedSecret:
            temSong.play(-1)
            screen.blit(tem , (360 , 300))
            screen.blit(temstand , (310 , 430))
            playedSecret = True
        
        screen.blit(font.render("hOI! tem no can read da config...\nnow u stuck wif tem forever!! :3" , True , (255 , 255 , 255) , None) , (100 , 100))

        pygame.display.flip()

attacks = {
    0: {
    },
    1: {
    }
}

amplitude = 75
frequency = 0.2

for i in range(1, 90):
    if i < 45:
        x = -4000 + i * 70
        y = 250 + int(amplitude * math.sin(frequency * i))
    else:
        x = -7075 + i * 70
        y = 490 + int(amplitude * math.sin(frequency * (i - 45)))
    attacks[0][f"{i}"] = {
        "type": "bone",
        "pos": (x, y),
        "speed_x": 750,
        "speed_y": 0,
        "hitbox_size": (50, 155),
        "sprite_size": (50, 600)
    }

platform_count = 15
bones_per_platform = 15
platform_spacing = 250
start_y = 4500
x_offset = 20
gap_size_in_bones = 3

for platform in range(platform_count):
    y = start_y - platform * platform_spacing
    gap_start = random.randint(0, bones_per_platform - gap_size_in_bones)
    for i in range(bones_per_platform):
        if gap_start <= i < gap_start + gap_size_in_bones:
            continue
        x = 390 + i * x_offset
        attacks[1][f"{platform * bones_per_platform + i}"] = {
            "type": "bone",
            "pos": (x, y),
            "speed_x": 0,
            "speed_y": -300,
            "hitbox_size": (20, 30),
            "sprite_size": (20, 100)
        }

currentAttack = 1

slashFrames = []
for i in range(6):
    sprite = pygame.image.load(f"assets/gui/attackEffect/slash-{i}.png").convert_alpha()
    slashFrames.append(sprite)

slashFrame = 0

attackMenu = pygame.image.load("assets/gui/attackMenu.png").convert_alpha()
attackMenu = pygame.transform.scale(attackMenu , (1000 , 300))

missedAttack = pygame.image.load("assets/gui/missedAttack.png").convert_alpha()
missedAttack = pygame.transform.scale(missedAttack , (150 , 50))

missedY = 100

attackBarSprites = []
for color in ["B" , "W"]:
    sprite = pygame.image.load(f"assets/gui/attackPole_{color}.png").convert_alpha()
    sprite = pygame.transform.scale(sprite , (50 , 300))
    attackBarSprites.append(sprite)
attackBar_x = 1050

soulBrokenSprite = pygame.image.load("assets/gameover/soulBroken.png").convert_alpha()

nameText = font.render(config["name"] , True , (255 , 255 , 255) , None).convert_alpha()
levelText = font.render(f"{config["lvl"]} LV" , True , (255 , 255 , 255) , None).convert_alpha()

lastChangedAttackBarFrameTick = None

mode = "menu"
attacked = False
selected_button = 0
sans_x = 480
sans_target_x = sans_x
sansDodgeTick = None
currentAttackBarFrame = 0

attemptedToHit = False
attackBar_speed = 900

hitTick = None
slashAnimationTick = None

missDelay = False

allowedToChooseButton = True
allowedToMove = False

defenseCooldown = None

isAttacking = False
torso_offset_fix = 0

def setMenu():
    global lastChangedAttackBarFrameTick , missDelay , mode , selected_button , attackBar_x , attackBar_speed , allowedToChooseButton , defenseCooldown , allowedToMove , attacked , attemptedToHit , hitTick , slashAnimationTick , sansDodgeTick
    mode = "menu"
    selected_button = 0
    attackBar_speed = 900
    attackBar_x = 1050
    allowedToChooseButton = True
    defenseCooldown = None
    allowedToMove = False
    attacked = False
    attemptedToHit = False
    hitTick = None
    slashAnimationTick = None
    sansDodgeTick = None
    missDelay = None
    lastChangedAttackBarFrameTick = None

sansPose = "normal"
headTick = None
torsoTick = None 
legsTick = None

headX , headY = sans_x , 0
headAnimIndex = 0
headAnim = [(100 , "x") , (250 , "y") , (100 , "x") , (-300 , "x") , (-250 , "y") , (100 , "x")]
headOffsetY = 0
headOffsetX = 0

torsoX , torsoY = sans_x - 46 , 100
torsoAnimIndex = 0
torsoAnim = [(100 , "x") , (50 , "y") , (100 , "x") , (-300 , "x") , (-50 , "y") , (100 , "x")]
torsoOffsetY = 0
torsoOffsetX = 0

legsX , legsY = sans_x - 15 , 200
legsAnimIndex = 0
legsAnim = [(15 , "x") , (-15 , "x")]
legsOffsetY = 0
legsOffsetX = 0

attackPosSet = None 
textTick = None

text = "This is pissing me off."
textAnim = 0

active_attacks = []
spawned_attacks = {}

pygame.mixer.set_num_channels(16)
channels = [pygame.mixer.Channel(i) for i in range(16)]

def healSoul(amount):
    global soul , hpText , bar
    channels[15].play(pygame.mixer.Sound("assets/gui/heal.mp3"))
    soul.hp = min(92 , soul.hp + amount)
    hpText = font.render(f"{soul.hp}/92" , True , (255 , 255 , 255) , None)
    bar = pygame.Rect(450 , 655 , soul.hp * 2, 50)

def setDefense():
    global attacked , mode , hitTick
    attacked = False
    mode = "defense"
    hitTick = None


while running:
    deltatime = clock.tick(60) / 1000
    keyClicked = pygame.key.get_pressed()
    current_time = time.time()
    tick_time = pygame.time.get_ticks()
    headX , headY = sans_x + headOffsetX, 0 + headOffsetY
    torsoX , torsoY = sans_x - 46 + torsoOffsetX , 100 + torsoOffsetY
    legsX , legsY = sans_x - 15 + legsOffsetX, 200 + legsOffsetY
    if battle:
        if not played_theme:
            pygame.mixer.music.play(-1)
            played_theme = True

    if sansPose == "shrug":
        torso_offset_fix = -30
    else:
        torso_offset_fix = 0
    
    if not headTick:
        headTick = pygame.time.get_ticks()
    if tick_time - headTick >= 100:
        if headAnim[headAnimIndex][1] == "y":
            headOffsetY += headAnim[headAnimIndex][0] * deltatime
        else:
            headOffsetX += headAnim[headAnimIndex][0] * deltatime

        if len(headAnim) - 1 == headAnimIndex:
            headAnimIndex = 0
        else:
            headAnimIndex += 1  

        headTick = tick_time

    if not torsoTick:
        torsoTick = pygame.time.get_ticks()
    if tick_time - torsoTick >= 100:
        if torsoAnim[torsoAnimIndex][1] == "y":
            torsoOffsetY += torsoAnim[torsoAnimIndex][0] * deltatime
        else:
            torsoOffsetX += torsoAnim[torsoAnimIndex][0] * deltatime

        if len(torsoAnim) - 1 == torsoAnimIndex:
            torsoAnimIndex = 0
        else:
            torsoAnimIndex += 1  

        torsoTick = tick_time

    if not legsTick:
        legsTick = pygame.time.get_ticks()
    if tick_time - legsTick >= 100:
        if legsAnim[legsAnimIndex][1] == "y":
            legsOffsetY += legsAnim[legsAnimIndex][0] * deltatime
        else:
            legsOffsetX += legsAnim[legsAnimIndex][0] * deltatime

        if len(legsAnim) - 1 == legsAnimIndex:
            legsAnimIndex = 0
        else:
            legsAnimIndex += 1  

        legsTick = tick_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                damageSoul(1)
            elif event.key == pygame.K_p:
                damageSoul(92)
            elif event.key == pygame.K_m:
                if mode == "defense":
                    setMenu()
            elif event.key == pygame.K_LEFT and mode == "menu" and allowedToChooseButton and not (attacked or attemptedToHit):
                if selected_button >= 1:
                    selected_button -= 1
                    pygame.mixer.Sound("assets/menu/select.mp3").play()
                else:
                    pass
            elif event.key == pygame.K_RIGHT and mode == "menu" and allowedToChooseButton and not (attacked or attemptedToHit):
                if selected_button <= 2:
                    selected_button += 1
                    pygame.mixer.Sound("assets/menu/select.mp3").play()
                else:
                    pass
            elif event.key == pygame.K_RETURN:
                if mode == "menu" and attacked is False:
                    if selected_button == 0 and not attacked:
                        attacked = True
                    if selected_button == 2 and not attacked:
                        healSoul(50)
                    if selected_button == 1 or 3 and not attacked:
                        setDefense()
                elif attemptedToHit is False:
                    current_sans_frame = 0
                    sansPose = "shrug"
                    attackBar_speed = 0
                    attemptedToHit = True
                    sans_target_x = 200
                    for ch in channels:
                        if not ch.get_busy():
                            ch.play(pygame.mixer.Sound("assets/slash.mp3"))
                            break
                    if not hitTick:
                        hitTick = pygame.time.get_ticks()
                    if not slashAnimationTick:
                        slashAnimationTick = pygame.time.get_ticks()

    screen.fill((0 , 0 , 0))

    if hitTick:
        allowedToChooseButton = False
        if tick_time - hitTick >= 400:
            sansPose = "normal"
        if tick_time - hitTick >= 1500:
            mode = "defense"
            attacked = False
            hitTick = None

    if slashAnimationTick:
        if tick_time - slashAnimationTick >= 100:
            if slashFrame != 6:
                slashFrame += 1
                slashAnimationTick = tick_time
            else:
                slashAnimationTick = None
                slashFrame = 0

    if sans_target_x != sans_x:
        if sans_x < sans_target_x:
            sans_x += 8
        elif sans_x > sans_target_x:
            sans_x -= 8
    else:
        if not sansDodgeTick:
            sansDodgeTick = pygame.time.get_ticks()
        if pygame.time.get_ticks() - sansDodgeTick >= 400:
            sans_target_x = 480
            sansDodgeTick = None
    
    if keyClicked[pygame.K_LEFT] and allowedToMove:
        collision = False
        for wall in walls:
            if pygame.Rect(soul.hitbox.x - 200 * deltatime, soul.hitbox.y , 25 , 25).colliderect(wall.hitbox):
                collision = True
        if collision == False:
            soul.hitbox.x -= 200 * deltatime

    if keyClicked[pygame.K_RIGHT] and allowedToMove:
        collision = False
        for wall in walls:
            if pygame.Rect(soul.hitbox.x + 200 * deltatime, soul.hitbox.y , 25 , 25).colliderect(wall.hitbox):
                collision = True
        if collision == False:
            soul.hitbox.x += 250 * deltatime

    if keyClicked[pygame.K_UP] and allowedToMove:
        collision = False
        for wall in walls:
            if pygame.Rect(soul.hitbox.x , soul.hitbox.y - 200 * deltatime, 25 , 25).colliderect(wall.hitbox):
                collision = True
        if collision == False:
            soul.hitbox.y -= 200 * deltatime

    if keyClicked[pygame.K_DOWN] and allowedToMove:
        collision = False
        for wall in walls:
            if pygame.Rect(soul.hitbox.x , soul.hitbox.y + 200 * deltatime , 25 , 25).colliderect(wall.hitbox):
                collision = True
        if collision == False:
            soul.hitbox.y += 250 * deltatime

    if soul.hp <= 0:
        break

    if mode == "defense":
        allowedToChooseButton = False
        selected_button = -1
        for i , wall in enumerate(walls):
            if i == 3:
                if wall.hitbox.width != 300:
                    wall.hitbox.width = max(300 , wall.hitbox.width - 1200 * deltatime)
                if wall.hitbox.x != 405:
                    wall.hitbox.x = min(405 , wall.hitbox.x + 650 * deltatime)
            elif i == 2:
                if wall.hitbox.width != 300:
                    wall.hitbox.width = max(300 , wall.hitbox.width - 1200 * deltatime)
                if wall.hitbox.x != 400:
                    wall.hitbox.x = min(400 , wall.hitbox.x + 650 * deltatime)
            elif i == 1:
                wall.hitbox.x = max(695, wall.hitbox.x - 650 * deltatime)
                wall.hitbox.height = max(300, wall.hitbox.height - 1200 * deltatime)
            elif i == 0:
                wall.hitbox.x = min(400, wall.hitbox.x + 650 * deltatime)
        screen.blit(soul.sprite , (soul.hitbox.x - 3 , soul.hitbox.y - 1))
        if not defenseCooldown:
            defenseCooldown = pygame.time.get_ticks()
        if tick_time - defenseCooldown >= 500:
            allowedToMove = True

        if currentAttack not in spawned_attacks:
            spawned_attacks[currentAttack] = []

            for attack_key, attack in attacks[currentAttack].items():
                hitbox_size = attack.get("hitbox_size", SansSpritesAttack[attack["type"]]["sprite"].get_size())
                hitbox = pygame.Rect(attack["pos"], hitbox_size)
                sprite_size = attack.get("sprite_size", SansSpritesAttack[attack["type"]]["sprite"].get_size())

                spawned_attacks[currentAttack].append({
                    "type": attack["type"],
                    "hitbox": hitbox,
                    "speed_x": attack["speed_x"],
                    "speed_y": attack["speed_y"],
                    "sprite_size": sprite_size
                })

        for attack in spawned_attacks.get(currentAttack, []):
            attack["hitbox"].x += attack["speed_x"] * deltatime
            attack["hitbox"].y += attack["speed_y"] * deltatime
            sprite = pygame.transform.scale(SansSpritesAttack[attack["type"]]["sprite"], attack["sprite_size"])
            pygame.draw.rect(screen , (0 , 0 , 255) , attack["hitbox"])
            screen.blit(sprite, attack["hitbox"])
            if soul.hitbox.colliderect(attack["hitbox"]):
                damageSoul(1)

        if all(a["hitbox"].x > 800 for a in spawned_attacks[currentAttack]):
            spawned_attacks.pop(currentAttack)
            currentAttack += 1
            setMenu()
        elif all(a["hitbox"].y < 0 for a in spawned_attacks[currentAttack]):
            spawned_attacks.pop(currentAttack)
            currentAttack += 1
            setMenu()

    elif mode == "menu":
        for i , wall in enumerate(walls):
           for i, wall in enumerate(walls):
                if i == 3:
                    wall.hitbox.width = min(1000, wall.hitbox.width + 550 * deltatime)
                    wall.hitbox.x = max(50, wall.hitbox.x - 300 * deltatime)
                elif i == 2:
                    wall.hitbox.width = min(1000, wall.hitbox.width + 550 * deltatime)
                    wall.hitbox.x = max(50, wall.hitbox.x - 300 * deltatime)
                elif i == 1:
                    wall.hitbox.x = min(1050, wall.hitbox.x + 350 * deltatime)
                    wall.hitbox.height = min(310, wall.hitbox.height + 350 * deltatime)
                elif i == 0:
                    wall.hitbox.x = max(50, wall.hitbox.x - 350 * deltatime)

        if not attacked:
            if not textTick:
                textTick = pygame.time.get_ticks()

            if tick_time - textTick >= 15:
                if textAnim < len(text):
                    textAnim += 1
                    channels[0].play(pygame.mixer.Sound("assets/gui/text.mp3"))
                textTick = tick_time
            screen.blit(font.render(f"* {text[:textAnim]}" , True , (255 , 255 , 255) , None) , (70 , 320))

        if attacked == True:
            screen.blit(attackMenu , (50 , 300))
            if not lastChangedAttackBarFrameTick:
                lastChangedAttackBarFrameTick = pygame.time.get_ticks()
            if tick_time - lastChangedAttackBarFrameTick >= 75:
                currentAttackBarFrame = 0 if currentAttackBarFrame == 1 else 1
                lastChangedAttackBarFrameTick = pygame.time.get_ticks()
            screen.blit(attackBarSprites[currentAttackBarFrame] , (attackBar_x , 300))
            attackBar_x -= attackBar_speed * deltatime
            if attackBar_x < 100 or attemptedToHit is True:
                screen.blit(missedAttack , (675 , missedY))
                if missedY > 50:
                    missedY -= 125 * deltatime
                else:
                    if not missDelay:
                        missDelay = pygame.time.get_ticks()
                    if tick_time - missDelay >= 600:
                        attacked = False

    for wall in walls:
        pygame.draw.rect(screen , (255 , 255 , 255) , wall.hitbox)
    
    for i in range(4):
        screen.blit(FightMenuAssets[FightMenuOrder[i]]["normal" if selected_button != i else "active"] , (i * 290 , 730))

    screen.blit(SansSprites["heads"][sansPose] , (headX , headY))
    screen.blit(SansSprites["torsos"][sansPose], (torsoX + torso_offset_fix, torsoY))
    screen.blit(SansSprites["legs"]["alive"] , (legsX, legsY))

    if slashFrame > 0 and slashFrame != 6:
        screen.blit(slashFrames[slashFrame] , (525 , 0))

    screen.blit(hpText , (640 , 645))
    screen.blit(krText , (380 , 645))
    screen.blit(levelText , (220 , 645))
    screen.blit(nameText , (40 , 645))
    pygame.draw.rect(screen , (255 , 255 , 0) , bar)

    pygame.display.flip()

played_gameover = False
played_soulShatter = False
soulBroken = False
soulBrokenInPieces = False
soulBrokenTick = None

gameOver = pygame.image.load("assets/menu/gameOver.png").convert_alpha()
gameOver = pygame.transform.scale(gameOver , (600 , 300))

delay = 1300

soulPieces = []
directions = ["left", "up", "right", "down"]
offset = 15
gravity = 175

text = random.choice(["You cannot give up just yet..." , "Dont lose hope!..." , "Our fate rests upon you..." , "You are the future of\nhumans and monsters..."])
textAnim = 0

msgDelay = None
textAnimReset = False
oneSecondDelay = None
addedSecondPart = False

textTick = 0
msgDelay = None
twoSec = None

text_phase = "main"
textAnim_main = 0
textAnim_name = 0
textAnim_determined = 0

text_sound = pygame.mixer.Sound("assets/gui/textAsg.mp3")

main_text = text
name_text = config["name"] + "!"
determined_text = " Stay determined..."




for i, direction in enumerate(directions):
    sprite = pygame.image.load(f"assets/gameover/SoulPiece_{i+1}.png")
    sprite = pygame.transform.scale(sprite, (25, 25))

    if direction == "left":
        pos = pygame.Rect(soul.hitbox.x - offset, soul.hitbox.y, sprite.get_width(), sprite.get_height())
        velocity = [-25, -25]  
    elif direction == "up":
        pos = pygame.Rect(soul.hitbox.x, soul.hitbox.y - offset, sprite.get_width(), sprite.get_height())
        velocity = [0, -75]  
    elif direction == "right":
        pos = pygame.Rect(soul.hitbox.x + offset, soul.hitbox.y, sprite.get_width(), sprite.get_height())
        velocity = [100 , -25]  
    elif direction == "down":
        pos = pygame.Rect(soul.hitbox.x, soul.hitbox.y + offset, sprite.get_width(), sprite.get_height())
        velocity = [0, -25] 

    soulPieces.append([sprite, pos, velocity , gravity])

pygame.mixer.music.stop()
screen.fill((0 , 0 , 0))
time.sleep(1)

while running:
    tickTime = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    if soulBroken:
        if not played_gameover:
            pygame.mixer.Sound("assets/gameover/determination.mp3").play(-1)
            played_gameover = True

    screen.fill((0 , 0 , 0))
    if not soulBrokenInPieces:
        screen.blit(soul.sprite , (soul.hitbox.x - 3 , soul.hitbox.y - 1))
    else:
        for piece, rect, velocity, gravity in soulPieces:
            rect.x += velocity[0] * deltatime
            rect.y += velocity[1] * deltatime

            velocity[1] += gravity * deltatime

            screen.blit(piece, rect)
            if not soulBrokenTick:
                soulBrokenTick = pygame.time.get_ticks()
            if pygame.time.get_ticks() - soulBrokenTick >= 1500:
                soulBroken = True

    if not played_soulShatter:
        soul.sprite = soulBrokenSprite
        soul.sprite = pygame.transform.scale(soul.sprite , (54 , 32))
        channels[1].play(pygame.mixer.Sound("assets/gameover/soulShatter.mp3"))
        shatter_time = pygame.time.get_ticks()
        played_soulShatter = True
    
    if soulBroken:
        screen.blit(gameOver , (250 , 30))
        if not textTick:
            textTick = pygame.time.get_ticks()
        if tickTime - textTick >= 100:
            if text_phase == "main":
                if textAnim_main < len(main_text):
                    textAnim_main += 1
                    channels[7].play(text_sound)
                else:
                    text_phase = "wait5"
                    msgDelay = tickTime

            elif text_phase == "wait5":
                if tickTime - msgDelay >= 5000:
                    text_phase = "clear"

            elif text_phase == "clear":
                screen.fill((0, 0, 0))
                pygame.display.flip()
                text_phase = "name"
                textAnim_name = 0
                continue 

            elif text_phase == "name":
                if textAnim_name < len(name_text):
                    textAnim_name += 1
                    text_sound.play()
                else:
                    text_phase = "wait1"
                    twoSec = tickTime

            elif text_phase == "wait1":
                if tickTime - twoSec >= 2000:
                    text_phase = "determined"
                    textAnim_determined = 0

            elif text_phase == "determined":
                if textAnim_determined < len(determined_text):
                    textAnim_determined += 1
                    channels[3].play(text_sound)
                else:
                    text_phase = "done"

            textTick = tickTime

        display_text = ""

        if text_phase in ["main", "wait5"]:
            display_text = f"{main_text[:textAnim_main]}"
        elif text_phase in ["name", "wait1", "determined", "done"]:
            display_text = f"{name_text[:textAnim_name]}{determined_text[:textAnim_determined]}"

        screen.blit(font.render(display_text, True, (255, 255, 255)), (250, 420))

    if played_soulShatter and not soulBrokenInPieces:
        if pygame.time.get_ticks() - shatter_time >= delay:
            soulBrokenInPieces = True

    pygame.display.flip()