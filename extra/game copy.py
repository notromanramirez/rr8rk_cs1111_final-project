# Roman Ramirez
# rr8rk@virginia.edu

# CITATIONS
# The pictures of Professor Nathan and Professor Brunelle were taken from the UVA CS website:
# https://engineering.virginia.edu/faculty/nathan-brunelle
# https://engineering.virginia.edu/faculty/ray-pettit
# The information from PA01 was taken from the CS Homepage:
# https://cs1110.cs.virginia.edu/pa01-greeting.html
# The heart picture was taken from this site:
# https://en.wikipedia.org/wiki/Heart_symbol
# The data for all the random words was used from this site:
# http://cs1110.cs.virginia.edu/files/words.txt

# TO DO
# make timer based on datetime, not gametime


### OBJECTIVE

flavor = [
	"You were working on your very first PA for CS 111X, when suddenly..."
	,"You passed out! When you awake, you realize that you've been shrunken"
	,"down! But you still need to finish PA01, especially with the 2-hr"
	,"feedback window. It's 9:55 PM and you only have 4 minutes to finish!"
	,""
	,"You are the size of an ant but you need to finish your assignment!"
	,"Navigate across your computer keyboard with the W-A-S-D keys."
	,"Walk over a key and select it by pressing ENTER."
	,"Also, you must walk off a key before pressing it again!"
	,""
	,"Oh, and try to avoid any help from the Professors..."
]

### REQUIRED FEATURES

# User Input
# W-A-S-D, movement keys
# ENTER, enter
# SPACE, look at assignment

# Graphics/Images
# screenshot of Lab01
# each individual key

# Start Screen
# in the main method
# displayed in black and white for now
# press enter to continue
# starts the gamebox.timer

# Small Enough Window
# final ints, 800 width, 600 height

### OPTIONAL FEATURES

# Enemies
# they move towards you
# Professor Brunelle and Pettit
# if they touch you, you lose a life

# Scrolling Level
# Left half will be for the map and the hud
# Right half will be for the PyCharm IDE

# Timer
# countdown from 4 minutes
# displayed on the screen

# Health Bar
# you have a red bar at the top of the screen
# begins to diminish after two minutes
# represents your grade

import pygame
import gamebox
import sys
import random
import urllib.request as urllib

# GETTERS

def get_key(dict, key):
	returned_key = ""
	for item in dict.items():
		if key == item[0]:
			returned_key = item[0]
	return returned_key

def get_hover_button():
	returned_button = None
	for btn in buttons.values():
		if is_over_object(player, btn):
			returned_button = btn
	return returned_button

def get_hover_letter():
	returned_letter = ""
	for btn in buttons.items():
		if is_over_object(player, btn[1]):
			returned_letter = btn[0]
	return returned_letter

# DECLARIZATION - FRAME
c_w, c_h = 800, 500
camera = gamebox.Camera(c_w, c_h)
fps = 60

debug = False

camera_screen = 0

# DECLARIZATION - PLAYER
player = gamebox.from_circle(0, 0, 'yellow', 10)

# gamebox.from_circle(0, 0, 'red', 20)
enemies = [
	gamebox.from_image(0, 0, 'ray.jpg'),
	gamebox.from_image(0, 0, 'nathan.jpg')
]

for e in enemies:
	e.scale_by(0.25)


# DECLARIZATION - THE KEYBOARD
buttons = {}
keyboard = ['!@#$%^&*()-+`', 'QWERTYUIOP[]\\', 'ASDFGHJKL;\'~', 'ZXCVBNM,./', '    ']
scale_x, scale_y = 200, 200

def declare_button(x, y, w=1, h=1, color='darkgray'):
	return gamebox.from_color(x * scale_x, y * scale_y, color, scale_x * 0.9 * w, scale_y * 0.9 * h)

def declare_letter_box(x, y, ltr, col="black", dim=1):
	return gamebox.from_text(x * scale_x, y * scale_y, ltr, int(scale_x / dim), col, False)

# not used atm
def update_button(btn_dict, name, x, y, col="black", dim=1):
	btn_dict[name].letter_box = declare_letter_box(x, y, get_key(btn_dict, name), col, dim)
	#btn_dict[name].box_color = col

for i in range(len(keyboard)):
	for j in range(len(keyboard[i])):

		dim = 5
		width = 1
		if keyboard[i][j] is "`":
			text = "backspace"
		elif keyboard[i][j] is " ":
			text = "spacebar"
			dim = 2
			width = 5
		elif keyboard[i][j] is "~":
			text = "enter"
		else:
			text = keyboard[i][j]
			dim = 1

		buttons.update({text: declare_button(j + i / 2, i, w=width)})
		buttons[text].letter_box = declare_letter_box(j + i / 2, i, text, dim=dim)

lsi, lsj = 3, -1
buttons.update({"left shift": declare_button(lsj + lsi / 2, lsi)})
buttons["left shift"].letter_box = declare_letter_box(lsj + lsi / 2, lsi, "left shift", dim=5)

rsi, rsj = 3, len(keyboard[3])
buttons.update({"right shift": declare_button(rsj + rsi / 2, rsi)})
buttons["right shift"].letter_box = declare_letter_box(rsj + rsi / 2, rsi, "right shift", dim=5)

is_shifted = False

# DECLARATION - THE PROMPT
turn = 0
answers = []
string_script_editor = {}


# INITIALIZING THE GAME

def spawn_to_letter(player, spawn):
	for btn in buttons.items():
		if btn[0] is spawn:
			player.x = btn[1].letter_box.x
			player.y = btn[1].letter_box.y

lives = 0
hearts_box = []
timer = 0
max_seconds = 0
seconds_left = 0
string_of_words = ""

# GAME STATES

paused = False
won = False
lost = False
difficulty = 0

# don't know what else to call this
# if the letter was already added to string_of_words, then it is changed to false
# this prevents more than a letter being added to string_of_words more than once
# still allows for repeated words, you just have to step off of the key
is_not_repeated = True

# OBJECT POSITIONING
keyboard_background_box_w, keyboard_background_box_h = 2800, 1100 # 2700, 1100
keyboard_background_box = gamebox.from_color(0, 0, 'lightgray', keyboard_background_box_w, keyboard_background_box_h)
keyboard_background_box.top = -150
keyboard_background_box.left = -150

border_w = 1000
border_col = 'black'

top_col_box = gamebox.from_color(0, 0, border_col, keyboard_background_box_w + border_w * 2, border_w)
left_col_box = gamebox.from_color(0, 0, border_col, border_w, keyboard_background_box_h + border_w * 2)
right_col_box = gamebox.from_color(0, 0, border_col, border_w, keyboard_background_box_h + border_w * 2)
bot_col_box = gamebox.from_color(0, 0, border_col, keyboard_background_box_w + border_w * 2, border_w)
collision_boxes = [top_col_box, left_col_box, right_col_box, bot_col_box]

# INITIALIZE THE GAME

def init_game():
	global camera_screen
	global turn, answers, string_script_editor
	global lives, timer, string_of_words
	global max_seconds, seconds_left
	global paused, won, lost
	global is_not_repeated
	global enemies
	global hearts_box

	camera_screen = 0

	turn = 0
	answers = [
		"unprofessional",
		"original",
		"submission system",
		"Stacks"
	]
	if debug: answers = ['\'', '\'', '\'', '\'']
	string_script_editor = [
		'# Cavalier Man',
		'# cav1mn@virginia.edu',
		'',
		'print("My name is CavMan!")',
		'print("Fun Fact: I finished this code last second.")',
		'', # unprofessional
		'', # original
		'', # submission system
		'', # stacks
		'# I am the size of an ant, help!'
	]

	hearts_box = []

	lives = 5
	for i in range(0, 12):
		hearts_box.append(gamebox.from_image(0, 0, 'heart.png'))
		hearts_box[i].scale_by(0.10)

	timer = 0
	max_seconds = 4 * 60
	seconds_left = max_seconds

	string_of_words = ""

	# GAME STATES

	paused = False
	won = False
	lost = False

	is_not_repeated = True

	top_col_box.bottom = keyboard_background_box.top
	top_col_box.left = keyboard_background_box.left - border_w

	left_col_box.right = keyboard_background_box.left
	left_col_box.top = keyboard_background_box.top - border_w

	right_col_box.left = keyboard_background_box.right
	right_col_box.top = keyboard_background_box.top - border_w

	bot_col_box.top = keyboard_background_box.bottom
	bot_col_box.left = keyboard_background_box.left - border_w

	#spawn enemies
	for e in enemies:
		e.x = random.randrange(left_col_box.right, right_col_box.left)
		e.y = random.randrange(top_col_box.top, bot_col_box.bottom)

	spawn_to_letter(player, "'")
	spawn_to_letter(enemies[0], 'I')

# DECLARIZATION - THE HUD

def draw_background():
	for box in collision_boxes:
		camera.draw(box)

	camera.draw(keyboard_background_box)

	for button in buttons.values():
		camera.draw(button)
		camera.draw(button.letter_box)

# UPDATES AND MOVEMENTS

live_box = None
input_text = None
input_box, input_box_back, input_box_blinker = None, None, None
timer_box, timer_box_back = None, None
prompt_box_back = None

prompt_box = [None, None, None, None, None, None, None, None, None, None]

is_random_answers = False

def randomize_answers():
	global answers

	f = urllib.urlopen("http://cs1110.cs.virginia.edu/files/words.txt").read().decode('utf-8')
	s = f.split('\n')

	list_of_words = []
	for line in s:
		stripped_line = line.strip()
		list_of_words.append(stripped_line)

	word_lengths = (4, 8, 13)

	for i in range(len(answers)):
		possible_word = list_of_words[random.randint(0, len(list_of_words))]
		while len(possible_word) > word_lengths[difficulty]:
			possible_word = list_of_words[random.randint(0, len(list_of_words))]
		answers[i] = possible_word

def update_inputs():
	global input_text
	global input_box, input_box_back, input_box_blinker
	input_text = 'print("'+string_of_words+'")'

	input_box = gamebox.from_text(0, 0, input_text[:-2], 50, 'black')
	input_box.left, input_box.bottom = camera.left, camera.bottom

	input_box_back = gamebox.from_color(camera.x, camera.bottom, 'white', camera.width, input_box.height)
	input_box_back.bottom = camera.bottom
	camera.draw(input_box_back)

	input_box_blinker = gamebox.from_text(0, 0, "_", 50, 'black')
	input_box_blinker.left, input_box_blinker.bottom = input_box.right, camera.bottom
	if int(timer/fps*3) % 2 is 0:
		camera.draw(input_box_blinker)

	input_box_end = gamebox.from_text(0, 0, input_text[-2:], 50, 'black')
	input_box_end.left, input_box_end.bottom = input_box_blinker.right, camera.bottom
	camera.draw(input_box_end)

	camera.draw(input_box)

def update_timer():
	global live_box
	global seconds_left
	global timer, timer_box, timer_box_back
	timer += 1

	seconds_left = max_seconds-int(timer/fps)
	if seconds_left % 60 < 10:
		second = "0" + str(seconds_left % 60)
	else:
		second = str(seconds_left % 60)
	minute = str(seconds_left // 60)
	clock_left = minute + ":" + second

	out_of_time(seconds_left)

	for i in range(len(hearts_box)):
		hearts_box[i].top, hearts_box[i].left = camera.top, camera.left + 30 * i
		if i < lives:
			camera.draw(hearts_box[i])


	timer_box = gamebox.from_text(0, 0, clock_left, 30, 'black')
	timer_box.right, timer_box.top = prompt_box_back.left, camera.top

	timer_box_back = gamebox.from_color(timer_box.x, timer_box.y, "white", timer_box.width, timer_box.height)
	camera.draw(timer_box_back)

	camera.draw(timer_box)

def update_prompt():
	global prompt_box, prompt_box_back

	ide_font_size = 20

	prompt_box_back = gamebox.from_image(0, 0, "ide.png")
	prompt_box_back.scale_by(0.5)
	prompt_box_back.right, prompt_box_back.top = camera.right, camera.top
	camera.draw(prompt_box_back)

	for i in range(len(string_script_editor)):
		prompt_box[i] = gamebox.from_text(0, 0, string_script_editor[i], ide_font_size, 'white')
		prompt_box[i].left, prompt_box[i].top = prompt_box_back.left + 70, camera.top + i * 24 + 87

	for i in range(len(string_script_editor)):
		if (turn + 5) == i:
			string_script_editor[i] = input_text

	for line in prompt_box:
		camera.draw(line)

not_correct_box, not_correct_box_back = None, None
display_not_correct = False

def update_not_correct():
	global not_correct_box, not_correct_box_back
	global display_not_correct

	text = ""
	if display_not_correct:
		text = "Your entry is not correct..."
	else:
		text = "Press SPACE to view your assignment!"

	not_correct_box = gamebox.from_text(0, 0, text, 30, "black")

	not_correct_box.left, not_correct_box.bottom = camera.left, input_box.top

	not_correct_box_back = gamebox.from_color(0, 0, "lightgray", not_correct_box.width, not_correct_box.height)
	not_correct_box_back.left, not_correct_box_back.bottom = camera.left, input_box.top


	camera.draw(not_correct_box_back)
	camera.draw(not_correct_box)

pa_task_image = None
answers_box = [None, None, None, None]

def update_pa_task(keys):
	global pa_task_image, answers_box
	if not is_random_answers:
		pa_task_image = gamebox.from_image(0, 0, "pa.png")

		pa_task_image.scale_by(0.8)
		pa_task_image.x = camera.x
		pa_task_image.y = camera.y
		if pygame.K_SPACE in keys:
			camera.draw(pa_task_image)
	else:
		for i in range(len(answers_box)):
			answers_box[i] = gamebox.from_text(0, 0, answers[i], 40, 'black')
			answers_box[i].left, answers_box[i].top = camera.left, camera.top + i * 28 + 30

			answers_box_back = gamebox.from_color(
				answers_box[i].x, answers_box[i].y, "white", answers_box[i].width, answers_box[i].height)

			if pygame.K_SPACE in keys:
				camera.draw(answers_box_back)
				camera.draw(answers_box[i])



def move_camera():
	camera.x = player.x + c_w / 4
	camera.y = player.y

def move_hud():
	update_prompt()
	update_inputs()
	update_timer()
	update_not_correct()

def move_player(keys, obj):
	global is_not_repeated

	camera.draw(player)

	speed = 0.8
	is_not_over_any_button = True
	for n in obj:
		if is_over_object(player, n):
			is_not_over_any_button = False

	if is_not_over_any_button:
		is_not_repeated = True

	if pygame.K_w in keys:
		player.y -= 10 * speed
	if pygame.K_a in keys:
		player.x -= 10 * speed
	if pygame.K_s in keys:
		player.y += 10 * speed
	if pygame.K_d in keys:
		player.x += 10 * speed
	if pygame.K_RETURN in keys and is_not_repeated:
		jump_player()

	for box in collision_boxes:
		player.move_to_stop_overlapping(box)


def jump_player():
	global lives
	global is_not_repeated, turn
	global string_of_words, string_script_editor
	global buttons, answers, won
	global display_not_correct
	global is_shifted

	# the backspace action
	if display_not_correct:
		display_not_correct = False

	if "shift" in get_hover_letter():
		is_shifted = True
	elif get_hover_letter() == "backspace":
		if string_of_words:
			string_of_words = string_of_words[:-1]
	elif get_hover_letter() == "spacebar":
		string_of_words += " "
	elif get_hover_letter() == "enter":
		# win condition
		if string_of_words == answers[-1] and (turn == 3):
			won = True
		# advance turn
		elif string_of_words == answers[turn]:
			turn += 1
			lives += 1
		else:
			display_not_correct = True
		string_of_words = ""
	else:
		if is_shifted:
			string_of_words += get_hover_letter().upper()
			is_shifted = False
		else:
			string_of_words += get_hover_letter().lower()


	# WIP: CHANGE COLOR OF THE BUTTON WHEN PRESSED
	# if get_hover_button() != None:
	#     x = get_hover_button().x
	#     y = get_hover_button().y
	#     width = get_hover_button().width
	#     height = get_hover_button().height
	#     for btn in buttons.values():
	#         if btn == get_hover_button():
	#             print(btn.letter_box)
	#             buttons.update(update_button(buttons, "A", x, y, "green"))

	is_not_repeated = False

def move_enemies():
	enemy_speed = 3.0
	for e in enemies:
		collision()
		e.move_speed()
		if e.right < player.left:
			e.speedx = enemy_speed
		elif e.left > player.right:
			e.speedx = -enemy_speed

		if e.bottom < player.top:
			e.speedy = enemy_speed
		elif e.top > player.bottom:
			e.speedy = -enemy_speed

		camera.draw(e)

#####################

def is_over_object(subject, object):
	bool = False
	if object.x - object.width/2 < subject.x < object.x + object.width/2:
		if object.y - object.height/2 < subject.y < object.y + object.height/2:
			bool = True
	return bool

# FUNCTIONS - SCREENS

def advance_screen(next_screen_number):
	global camera_screen
	if camera_screen < next_screen_number:
		camera_screen += 1
	else:
		camera_screen = 0

def run_title(keys):
	global camera_screen, debug, is_random_answers
	global difficulty

	camera.clear("black")

	# displaying the flavor
	font_size, y = 30, camera.top + 50
	for line in flavor:
		box_line = gamebox.from_text(0, y, line, font_size, "white")
		box_line.left = camera.left + font_size
		camera.draw(box_line)
		y += font_size

	continue_box = gamebox.from_text(0, 0, "or Press SPACE to do your assignment.", font_size, "yellow")
	continue_box.right, continue_box.bottom = camera.right, camera.bottom
	camera.draw(continue_box)

	hard_box = gamebox.from_text(0, 0, "Press 3 to play with hard, random words!", font_size - 5, "yellow")
	hard_box.left, hard_box.bottom = camera.left, camera.bottom
	camera.draw(hard_box)

	med_box = gamebox.from_text(0, 0, "Press 2 to play with medium, random words!", font_size - 5, "yellow")
	med_box.left, med_box.bottom = camera.left, hard_box.top
	camera.draw(med_box)

	easy_box = gamebox.from_text(0, 0, "Press 1 to play with easy, random words!", font_size - 5, "yellow")
	easy_box.left, easy_box.bottom = camera.left, med_box.top
	camera.draw(easy_box)

	if pygame.K_9 in keys:
		debug = True
	if pygame.K_0 in keys:
		debug = False

	# advance to the game screen
	if pygame.K_SPACE in keys:
		is_random_answers = False
		advance_screen(1)
	elif pygame.K_1 in keys:
		difficulty = 0
		is_random_answers = True
		randomize_answers()
		advance_screen(1)
	elif pygame.K_2 in keys:
		difficulty = 1
		is_random_answers = True
		randomize_answers()
		advance_screen(1)
	elif pygame.K_3 in keys:
		difficulty = 2
		is_random_answers = True
		randomize_answers()
		advance_screen(1)

	camera.display()

def collision():
	global lost, paused, lives
	for e in enemies:
		if player.touches(e):
			lives -= 1

			if lives == 0:
				lost = True
			else:
				for e in enemies:
					e.x = random.randrange(left_col_box.right, right_col_box.left)
					e.y = random.randrange(top_col_box.bottom, bot_col_box.top)

def update_lost():
	global lost, paused
	lost = True
	lost_box = gamebox.from_text(camera.x, camera.y, "You lost!", 40, "darkred")
	lost_box_back = gamebox.from_color(camera.x, camera.y, "white", lost_box.width, lost_box.height)
	camera.draw(lost_box_back)
	camera.draw(lost_box)

	replay_box = gamebox.from_text(0, 0, "Press N to play again or press X to quit.", 30, "brown")
	replay_box.right, replay_box.bottom = camera.right, camera.bottom
	camera.draw(replay_box)

	paused = True


def out_of_time(time):
	global lost
	if time <= 0:
		lost = True

def run_game(keys):
	# global camera_screen
	# global won, string_of_words

	if not paused:
		# clear the camera
		camera.clear("black")

		# draw the background
		draw_background()

		# update the screen based on moving
		move_camera()
		move_enemies()
		move_hud()
		move_player(keys, buttons.values())
		update_pa_task(keys)

		if lost:
			update_lost()

		if won:
			advance_screen(2)

		camera.display()
	else:
		# how to unpause
		if pygame.K_n in keys:
			advance_screen(-1)
		if pygame.K_x in keys:
			sys.exit(0)

def run_win(keys):
	camera.clear("black")

	submission_image = gamebox.from_image(0, 0, submision)
	submission_image.width = camera.width
	submission_image.left = camera.left
	submission_image.top = camera.top
	camera.draw(submission_image)

	sub_font_size = 17

	for i in range(len(string_script_editor)):
		prompt_box[i] = gamebox.from_text(0, 0, string_script_editor[i], sub_font_size, 'black')
		prompt_box[i].left, prompt_box[i].top = camera.left + 70, camera.top + i * 11 + 90
		camera.draw(prompt_box[i])

	duration = max_seconds - seconds_left
	minutes = str(55 + duration // 60)

	if duration % 60 < 10:
		seconds = "0" + str(duration % 60)
	else:
		seconds = str(duration % 60)

	win_box = gamebox.from_text(
		camera.x, camera.y, "You submitted on time at 9:" + minutes + ":" + seconds + " PM!", 40, 'white')
	win_box.top = submission_image.bottom + sub_font_size
	camera.draw(win_box)

	replay_box = gamebox.from_text(0, 0, "Press N to play again!", 30, 'yellow')
	replay_box.left, replay_box.bottom = camera.left, camera.bottom
	camera.draw(replay_box)

	quit_box = gamebox.from_text(0, 0, "Press X to quit.", 30, 'yellow')
	quit_box.right, quit_box.bottom = camera.right, camera.bottom
	camera.draw(quit_box)


	if pygame.K_n in keys:
		advance_screen(-1)
	if pygame.K_x in keys:
		sys.exit(0)

	camera.display()

# REFRESHING THE SCREEN
def tick(keys):
	if camera_screen == 0:
		init_game()
		run_title(keys)
	elif camera_screen == 1:
		run_game(keys)
	elif camera_screen == 2:
		run_win(keys)

gamebox.timer_loop(fps, tick)