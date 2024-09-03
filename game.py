import pygame

# Переменные для установки ширины и высоты окна
from pygame.sprite import Group

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Подключение фото для заднего фона
# Здесь лишь создание переменной, вывод заднего фона ниже в коде
bg = pygame.image.load('bg.jpg')


# Класс, описывающий поведение главного игрока
class Player(pygame.sprite.Sprite):
	# Изначально игрок смотрит вправо, поэтому эта переменная True
	right = True

	# Методы
	def __init__(self):
		# Стандартный конструктор класса
		# Нужно ещё вызывать конструктор родительского класса
		super().__init__()

		# Создаем изображение для игрока
		# Изображение находится в этой же папке проекта
		self.image = pygame.image.load('idle.png')

		# Установите ссылку на изображение прямоугольника
		self.rect = self.image.get_rect()

		# Задаем вектор скорости игрока
		self.change_x = 0
		self.change_y = 0

	def update(self):
		# В этой функции мы передвигаем игрока
		# Сперва устанавливаем для него гравитацию
		self.calc_grav()

		# Передвигаем его на право/лево
		# change_x будет меняться позже при нажатии на стрелочки клавиатуры
		self.rect.x += self.change_x

		# Следим ударяем ли мы какой-то другой объект, платформы, например
		block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		# Перебираем все возможные объекты, с которыми могли бы столкнуться
		for block in block_hit_list:
			# Если мы идем направо,
			# устанавливает нашу правую сторону на левой стороне предмета, которого мы ударили
			if self.change_x > 0:
				self.rect.right = block.rect.left
			elif self.change_x < 0:
				# В противном случае, если мы движемся влево, то делаем наоборот
				self.rect.left = block.rect.right

		# Передвигаемся вверх/вниз
		self.rect.y += self.change_y

		# То же самое, вот только уже для вверх/вниз
		block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		for block in block_hit_list:
			# Устанавливаем нашу позицию на основе верхней / нижней части объекта, на который мы попали
			if self.change_y > 0:
				self.rect.bottom = block.rect.top
			elif self.change_y < 0:
				self.rect.top = block.rect.bottom

			# Останавливаем вертикальное движение
			self.change_y = 0

	def calc_grav(self):
		# Здесь мы вычисляем как быстро объект будет
		# падать на землю под действием гравитации
		if self.change_y == 0:
			self.change_y = 1
		else:
			self.change_y += .95

		# Если уже на земле, то ставим позицию Y как 0
		if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
			self.change_y = 0
			self.rect.y = SCREEN_HEIGHT - self.rect.height


	def jump(self):
		# Обработка прыжка
		# Нам нужно проверять здесь, контактируем ли мы с чем-либо
		# или другими словами, не находимся ли мы в полете.
		# Для этого опускаемся на 10 единиц, проверем соприкосновение и далее поднимаемся обратно
		self.rect.y += 10
		platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		self.rect.y -= 10


		# Если все в порядке, прыгаем вверх
		if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
			self.change_y = -16
			global jumplimit
			jumplimit += 1

	# Передвижение игрока
	def go_left(self):
		# Сами функции будут вызваны позже из основного цикла
		self.change_x = -9 # Двигаем игрока по Х
		if(self.right): # Проверяем куда он смотрит и если что, то переворачиваем его
			self.flip()
			self.right = False

	def go_right(self):
		# то же самое, но вправо
		self.change_x = 9
		if (not self.right):
			self.flip()
			self.right = True


	def stop(self):
		# вызываем этот метод, когда не нажимаем на клавиши
		self.change_x = 0

	def flip(self):
		# переворот игрока (зеркальное отражение)
		self.image = pygame.transform.flip(self.image, True, False)


	def change(self):
		return  self.rect.center


# Класс для описания платформы
class Platform(pygame.sprite.Sprite):
	def __init__(self, width, height):
		# Конструктор платформ
		super().__init__()
		# Также указываем фото платформы
		self.image = pygame.image.load('platform.png')

		# Установите ссылку на изображение прямоугольника
		self.rect = self.image.get_rect()


# Класс для описания
class Lum(pygame.sprite.Sprite):
	def __init__(self):
		# Конструктор платформ
		super().__init__()
		# Также указываем фото платформы
		self.image = pygame.image.load('Star.png')

		# Установите ссылку на изображение прямоугольника
		self.rect = self.image.get_rect()


class Lumred(pygame.sprite.Sprite):
	def __init__(self):
		# Конструктор платформ
		super().__init__()
		# Также указываем фото платформы
		self.image = pygame.image.load('dieBlock.png')

		# Установите ссылку на изображение прямоугольника
		self.rect = self.image.get_rect()


class Minred(pygame.sprite.Sprite):
	def __init__(self):
		# Конструктор платформ
		super().__init__()
		# Также указываем фото платформы
		self.image = pygame.image.load('Star.png')

		# Установите ссылку на изображение прямоугольника
		self.rect = self.image.get_rect()


class Finish(pygame.sprite.Sprite):
	def __init__(self):
		# Конструктор платформ
		super().__init__()
		# Также указываем фото платформы
		self.image = pygame.image.load('portal1.png')

		# Установите ссылку на изображение прямоугольника
		self.rect = self.image.get_rect()

# Класс для расстановки платформ на сцене
class Level(object):
	def __init__(self, player):
		# Создаем группу спрайтов (поместим платформы различные сюда)
		self.platform_list = pygame.sprite.Group()

		self.lums_list = pygame.sprite.Group()
		self.lumsred_list = pygame.sprite.Group()
		self.minred_list = pygame.sprite.Group()
		self.finish_list = pygame.sprite.Group()
		# Ссылка на основного игрока
		self.player = player
		global classlist
		classlist = self
	# Чтобы все рисовалось, то нужно обновлять экран
	# При вызове этого метода обновление будет происходить
	def update(self):
		self.platform_list.update()
		self.lums_list.update()
		self.lumsred_list.update()
		self.finish_list.update()
		self.minred_list.update()

	# Метод для рисования объектов на сцене
	def draw(self, screen):
		# Рисуем задний фон
		screen.blit(bg, (0, 0))

		# Рисуем все платформы из группы спрайтов
		self.platform_list.draw(screen)
		self.lums_list.draw(screen)
		self.lumsred_list.draw(screen)
		self.minred_list.draw(screen)
		self.finish_list.draw(screen)


# Класс,, что описывает где будут находится все платформы
# на определенном уровне игры
class Level_01(Level):
	def __init__(self, player, active_sprite_list):
		# Вызываем родительский конструктор
		Level.__init__(self, player)

		# Массив с данными про платформы. Данные в таком формате:
		# ширина, высота, x и y позиция
		level = [
			[210, 32, 500, 500],
			[210, 32, 200, 400],
			[210, 32, 600, 300],
			[210, 32, 0, 300],
			[210, 32, 210, 180],
			[210, 32, 420, 200],
			[210, 32, 630, 300],
			[210, 32, 840, 300],
			[210, 32, 1050, 300],
			[210, 32, 1260, 300],
			[210, 32, 1470, 300],
			[210, 32, 1470, 250],

		]
		coin = [[1000,200],
				[1000,250] ]

		coinred = [[300, 300]]

		minred = [[1470, 250]]

		finish = [0, 280]

		global lencoin, score
		lencoin = len(coin)
		for i in range(250):
			level.append([210, 32, (i - 250 // 2) *210, 600])

		# Перебираем массив и добавляем каждую платформу в группу спрайтов - platform_list
		for platform in level:
			block = Platform(platform[0], platform[1])
			block.rect.x = platform[2]
			block.rect.y = platform[3]
			block.player = self.player
			self.platform_list.add(block)
			active_sprite_list.add(block)


		for lums in coin:
			lum = Lum()
			lum.rect.x = lums[0]
			lum.rect.y = lums[1]
			lum.player = self.player
			self.lums_list.add(lum)
			active_sprite_list.add(lum)


		for lums in coinred:
			lumred = Lumred()
			lumred.rect.x = lums[0]
			lumred.rect.y = lums[1]
			lumred.player = self.player
			self.lumsred_list.add(lumred)
			active_sprite_list.add(lumred)


		for lums in minred:
			min = Minred()
			min.rect.x = lums[0]
			min.rect.y = lums[1]
			min.player = self.player
			self.minred_list.add(min)
			active_sprite_list.add(min)


		fin = Finish()
		fin.rect.x = finish[0]
		fin.rect.y = finish[1]
		fin.player = self.player
		self.finish_list.add(fin)
		active_sprite_list.add(fin)


def removesprite(self):
	modul = 55
	for coin in self.lums_list:
		if abs(coin.rect.center[0] - self.player.rect.center[0]) < modul and abs(coin.rect.center[1] - self.player.rect.center[1]) < modul:
			self.lums_list.remove(coin)
			coin.rect.center = (1000, 1000)
			global score
			score += 1


def removespritered(self):
	modul = 55
	for coin in self.lumsred_list:
		if abs(coin.rect.center[0] - self.player.rect.center[0]) < modul and abs(coin.rect.center[1] - self.player.rect.center[1]) < modul:
			self.lumsred_list.remove(coin)
			coin.rect.center = (1000, 1000)
			global scorered
			scorered += 1


def mindel(self):
	modul = 55
	for coin in self.minred_list:
		if abs(coin.rect.center[0] - self.player.rect.center[0]) < modul and abs(coin.rect.center[1] - self.player.rect.center[1]) < modul:
			global scorered
			scorered -= 10



def finishgame(self):
	modul = 55
	for coin in self.finish_list:
		if abs(coin.rect.center[0] - self.player.rect.center[0]) < modul and abs(coin.rect.center[1] - self.player.rect.center[1]) < modul:
			self.lumsred_list.remove(coin)
			return False
		else:
			return True


font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, (0, 255, 0), fill_rect)
    pygame.draw.rect(surf, (255, 255, 255), outline_rect, 2)


def show_go_screen(screen, WIDTH, HEIGHT, result):
    #screen.blit()
    draw_text(screen, "RAYMAN", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, result, 22,
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        pygame.time.Clock().tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); waiting = False


# Основная функция прогарммы
def main():
	global jumplimit, classlist, score, scorered

	levels = [Level_01]
	levelind = 0


	indexf = 0
	finishimage = ['portal2.png', 'portal1.png']
	FPSF = 0

	jumplimit = 0
	maxred = 100

	score = 0
	scorered = maxred
	# Инициализация
	pygame.init()

	# Установка высоты и ширины
	size = [SCREEN_WIDTH, SCREEN_HEIGHT]
	screen = pygame.display.set_mode(size)

	# Название игры
	pygame.display.set_caption("Платформер")

	player = Player()
	active_sprite_list: Group = pygame.sprite.Group()
	# Создаем игрока

	# Создаем все уровни
	level_list = []
	level_list.append(levels[levelind](player, active_sprite_list))

	# Устанавливаем текущий уровень
	current_level_no = 0
	current_level = level_list[current_level_no]


	player.level = current_level

	player.rect.x = 340
	player.rect.y = SCREEN_HEIGHT - player.rect.height
	active_sprite_list.add(player)


	# Цикл будет до тех пор, пока пользователь не нажмет кнопку закрытия
	done =  True

	# Используется для управления скоростью обновления экрана
	clock = pygame.time.Clock()

	soundfon = pygame.mixer.music.load('fon1.mp3')
	pygame.mixer.music.set_volume(-1)
	pygame.mixer.music.play()
	# Основной цикл программы
	while done:
		# Отслеживание действий
		for event in pygame.event.get():
			if event.type == pygame.QUIT: # Если закрыл программу, то останавливаем цикл
				done = False
				quit()
			# Если нажали на стрелки клавиатуры, то двигаем объект
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					player.go_left()
				if event.key == pygame.K_RIGHT:
					player.go_right()
				if event.key == pygame.K_UP:
					player.jump()

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT and player.change_x < 0:
					player.stop()
				if event.key == pygame.K_RIGHT and player.change_x > 0:
					player.stop()

		# Обновляем игрока
		active_sprite_list.update()

		# Обновляем объекты на сцене
		current_level.update()

		# Если игрок приблизится к правой стороне, то дальше его не двигаем
		if player.rect.right > SCREEN_WIDTH:
			player.rect.right = SCREEN_WIDTH

		# Если игрок приблизится к левой стороне, то дальше его не двигаем
		if player.rect.left < 0:
			player.rect.left = 0

		if jumplimit > 5:
			delta = -20
			jumplimit -= 1
		else:
			delta = 0
		if player.change_y != 0:
			coy = player.change_y + delta
		else:
			coy = 0
		for aline in active_sprite_list:
			aline.rect.x -=  player.change_x  # small move
			aline.rect.y -= coy


		if scorered <= 0:
			done = False
		if scorered >= maxred:
			scorered = maxred

		removesprite(classlist)
		removespritered(classlist)
		mindel(classlist)
		for i in classlist.finish_list:
			i.image = pygame.image.load(finishimage[1 - indexf])
			if FPSF >= 270:
				indexf = 1 - indexf
				FPSF =  0
			FPSF += 30

		# Рисуем объекты на окне
		current_level.draw(screen)
		active_sprite_list.draw(screen)

		draw_text(screen, 'ЛЮМОВ ' + str(score) + ':' + str(lencoin), 20, SCREEN_WIDTH  - 80, 10)
		draw_shield_bar(screen, 5, 5, scorered)

		done = finishgame(classlist)
		# Устанавливаем количество фреймов
		clock.tick(30)
		# Обновляем экран после рисования объектов
		pygame.display.flip()
		if not done:
			show_go_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT,'Уровень ' + str(levelind + 1) + ' ЛЮМОВ ' + str(score) + ':' + str(lencoin))

	# Корректное закртытие программы
	pygame.quit()
main()