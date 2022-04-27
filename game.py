# Roman Ramirez
# rr8rk@virginia.edu

# INSTRUCTIONS
# Hello! To use my pictures in the game, please unzip "game_files.zip",
# making sure that the following files are in the folder, game_files:
	# brunelle.jpg
	# heart.png
	# ide.png
	# pa.png
	# pettit.jpg
	# submission.png
# the game_files folder should be located in the same path as game.py
# Please ignore the other images that were submitted on April 17th.
	# I didn't know how to unsubmit those images.

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


### OBJECTIVE

flavor = [
	"\"You were working on your very first PA for CS 111X, when suddenly..."
	, "You fell asleep! When you awake, you realize that you've been shrunken"
	, "down! However, you still need to finish PA01, especially with the 2-hr"
	, "feedback window. It's 9:55 PM and you only have 4 minutes to finish!\""
	, ""
	, "\"You are the size of an ant, but you need to finish your assignment!"
	, "Navigate across your computer keyboard with the W-A-S-D keys."
	, "Walk over a key and select it by pressing the ENTER key."
	, "View your assignment by pressing the SPACE key."
	, "Also, you must walk off a key before pressing it again.\""
	, ""
	, "\"Oh, and try to avoid any help from the Professors...\""
]

# REQUIRED FEATURES

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

# OPTIONAL FEATURES

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

# IMPORTS

from random import randrange, randint
from sys import exit
from time import time
from urllib.request import urlopen
from urllib.error import URLError

import gamebox
import pygame

# GLOBAL VARIABLES

# debugging
debug = False

# file locations
fn_folder = "game_files/"
fn_brunelle = fn_folder + "brunelle.jpg"
fn_heart = fn_folder + "heart.png"
fn_ide = fn_folder + "ide.png"
fn_pa = fn_folder + "pa.png"
fn_pettit = fn_folder + "pettit.jpg"
fn_submission = fn_folder + "submission.png"

# camera constants
c_w, c_h = 800, 500
camera = gamebox.Camera(c_w, c_h)
fps = 60
camera_screen = 0

# moving objects
player = gamebox.from_circle(0, 0, 'yellow', 10)

try:
	enemies = [
		gamebox.from_image(0, 0, fn_pettit),
		gamebox.from_image(0, 0, fn_brunelle)
	]

	for e in enemies:
		e.scale_by(0.25)
except URLError:
	enemies = [
		gamebox.from_circle(0, 0, 'red', 10),
		gamebox.from_circle(0, 0, 'red', 10)
	]


# keyboard constants
buttons = {}
keyboard = ['!@#$%^&*()-+`', 'QWERTYUIOP[]\\', 'ASDFGHJKL;\'~', 'ZXCVBNM,./', '    ']
scale_x, scale_y = 200, 200
backspace = "backspace"
enter = "enter"
spacebar = "space"
left_shift = "left shift"
right_shift = "right shift"

# declarization - the HUD
answers = []

# game states

paused = False
won = False
lost = False
turn = 0
difficulty = 0

# don't know what else to call this
# if the letter was already added to typing_string, then it is changed to false
# this prevents more than a letter being added to typing_string more than once
# still allows for repeated words, you just have to step off of the key
is_not_repeated = True

# SPRITE BOX POSITIONING
keyboard_background_box_w, keyboard_background_box_h = 2800, 1100  # 2700, 1100
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

# global - randomize_answers()
is_random_answers = False

# global - update_inputs()
typing_string = ""
is_shifted = False
input_text = None
input_box, input_box_back, input_box_blinker = None, None, None

# global - update_timer()
timer = 0
start = 0
max_seconds = 0
seconds_left = 0
lives = 0
hearts_box = []
timer_box, timer_box_back = None, None
live_box = None

# global - update_prompt()
string_script_editor = {}
prompt_box = [None, None, None, None, None, None, None, None, None, None]
prompt_box_back = None

# global - update_not_correct()
not_correct_box, not_correct_box_back = None, None
display_not_correct = False

# global - update_pa_task()
pa_task_image = None
answers_box = [None, None, None, None]


# GET METHODS

def get_hover_button():
	"""
    This function finds what SpriteBox button the player is currently standing on.
    :return:
        if the player is standing on a button, the value of the dictionary, the SpriteBox, will be returned.
        if the player isn't standing on a button, None will be returned.
    """
	returned_button = None
	for btn in buttons.values():
		if is_over_object(player, btn):
			returned_button = btn
	return returned_button


def get_hover_letter():
	"""
    This function finds what string button the player is currently standing on.
    :return:
        if the player is standing on a button, the key of the dictionary, the string, will be returned.
        if the player isn't standing on a button, "" will be returned.
    """
	returned_letter = ""
	for btn in buttons.items():
		if is_over_object(player, btn[1]):
			returned_letter = btn[0]
	return returned_letter


def is_over_object(subject, object):
	"""
    This function determines if the subject is currently standing on the object
    :param subject: a movable SpriteBox, typically either the player or an enemy
    :param object: a stationary SpriteBox, typically a button SpriteBox
    :return: boolean,
        True if the subject is over the object
        False if the subject is not over the object
    """
	bool = False
	if object.x - object.width / 2 < subject.x < object.x + object.width / 2:
		if object.y - object.height / 2 < subject.y < object.y + object.height / 2:
			bool = True
	return bool


# KEYBOARD INITIALIZATION FUNCTIONS

def declare_button(x, y, w=1, h=1):
	"""
    This function specifies a button SpriteBox using the specified parameters:
    :param x: int, the x-position relative to the other button SpriteBoxes on the map
    :param y: int, the y-position relative to the other button SpriteBoxes on the map
    :param w: int, the width of the button relative to the other button SpriteBoxes
    :param h: int, the width of the button relative to the other button SpriteBoxes
    :return: SpriteBox, a dark gray rectangle with the specified coordinates and size.
    """
	return gamebox.from_color(x * scale_x, y * scale_y, "darkgray", scale_x * 0.9 * w, scale_y * 0.9 * h)


def declare_letter_box(x, y, ltr, dim=1):
	"""
    This function specifies a letter SpriteBox using the specified parameters:
    :param x: int, the x-position relative to the other button SpriteBoxes on the map
    :param y: int, the y-position relative to the other button SpriteBoxes on the map
    :param ltr: string, what the button cap will show on the map
    :param dim: int, by what factor the font size of the letter will be reduced
    :return: SpriteBox, a black text with the specified coordinates and size.
    """
	return gamebox.from_text(x * scale_x, y * scale_y, ltr, int(scale_x / dim), "black", False)


# finish initialization of keyboard
for i in range(len(keyboard)):
	for j in range(len(keyboard[i])):

		dim = 5
		width = 1
		if keyboard[i][j] is "`":
			text = backspace
		elif keyboard[i][j] is " ":
			text = spacebar
			dim = 2
			width = 5
		elif keyboard[i][j] is "~":
			text = enter
		else:
			text = keyboard[i][j]
			dim = 1

		buttons.update({text: declare_button(j + i / 2, i, w=width)})
		buttons[text].letter_box = declare_letter_box(j + i / 2, i, text, dim=dim)

# left shift
lsi, lsj = 3, -1
buttons.update({left_shift: declare_button(lsj + lsi / 2, lsi)})
buttons[left_shift].letter_box = declare_letter_box(lsj + lsi / 2, lsi, left_shift, dim=5)

# right shift
rsi, rsj = 3, len(keyboard[3])
buttons.update({right_shift: declare_button(rsj + rsi / 2, rsi)})
buttons[right_shift].letter_box = declare_letter_box(rsj + rsi / 2, rsi, right_shift, dim=5)


# INITIALIZE THE GAME

def spawn_to_letter(subject, ltr):
	"""
    This function places the subject on the specified letter
    :param subject: SpriteBox, typically the player or an enemy
    :param ltr: string, the text of the button that the SpriteBox will be placed on
    :return: None
    """
	for btn in buttons.items():
		if btn[0] is ltr:
			subject.x = btn[1].letter_box.x
			subject.y = btn[1].letter_box.y


def init_game():
	"""
    This function initializes the game by resetting every global variable in the function to its game default.
    These global variables have been globally declared before this function with values that are unimportant.
    :return: None
    """
	global camera_screen
	global paused, won, lost  # game states
	global enemies  # entities
	global turn, answers, string_script_editor  # prompt variables
	global typing_string, is_not_repeated  # input states
	global timer, start, max_seconds, seconds_left  # timer values
	global lives, hearts_box  # lives values

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
		'',  # unprofessional
		'',  # original
		'',  # submission system
		'',  # stacks
		'# I am the size of an ant, help!'
	]

	hearts_box = []

	lives = 5
	try:
		for i in range(0, 12):
			hearts_box.append(gamebox.from_image(0, 0, fn_heart))
			hearts_box[i].scale_by(0.10)
	except URLError:
		for i in range(0, 12):
			hearts_box.append(gamebox.from_circle(0, 0, 'red', 10))

	timer = 0
	start = 0
	max_seconds = 4 * 60
	seconds_left = max_seconds

	typing_string = ""

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

	# spawn enemies
	for e in enemies:
		e.x = randrange(left_col_box.right, right_col_box.left)
		e.y = randrange(top_col_box.top, bot_col_box.bottom)

	if debug:
		spawn_to_letter(player, "'")
	else:
		spawn_to_letter(player, spacebar)
	spawn_to_letter(enemies[0], 'I')


def draw_background():
	"""
    This function draws the background SpriteBoxes in order:
        the collision boxes,
        the keyboard's background box,
        the buttons,
        the letters
    :return: None
    """
	for box in collision_boxes:
		camera.draw(box)

	camera.draw(keyboard_background_box)

	for button in buttons.values():
		camera.draw(button)
		camera.draw(button.letter_box)


def randomize_answers():
	"""
    This function edits the default answers, the answers to PA01, and replaces them with four random words, taken
    from the UVA CS department's list of words. These four words depend on the difficulty of the game.
    :return: None.
    """
	global answers

	try:
		url = "http://cs1110.cs.virginia.edu/files/words.txt"
		with urlopen(url) as website:
			s = website.read().decode('utf-8').split('\n')

		list_of_words = []
		for line in s:
			stripped_line = line.strip()
			list_of_words.append(stripped_line)

		word_lengths = (4, 8, 13)

		for i in range(len(answers)):
			possible_word = list_of_words[randint(0, len(list_of_words))]
			while len(possible_word) > word_lengths[difficulty]:
				possible_word = list_of_words[randint(0, len(list_of_words))]
			answers[i] = possible_word
	except URLError:
		print("\nInvalid URL, using the default assignment words.")

# UPDATES

def update_inputs():
	"""
    This function updates the input SpriteBoxes as the run_game() screen is being displayed:
        the current line of text that the player is typing,
        the blinker cursor,
        and the white background.
    :return: None
    """
	global input_text
	global input_box, input_box_back, input_box_blinker
	input_text = 'print("' + typing_string + '")'

	input_box = gamebox.from_text(0, 0, input_text[:-2], 50, 'black')
	input_box.left, input_box.bottom = camera.left, camera.bottom

	input_box_back = gamebox.from_color(camera.x, camera.bottom, 'white', camera.width, input_box.height)
	input_box_back.bottom = camera.bottom
	camera.draw(input_box_back)

	input_box_blinker = gamebox.from_text(0, 0, "_", 50, 'black')
	input_box_blinker.left, input_box_blinker.bottom = input_box.right, camera.bottom
	if int(timer * 3) % 2 is 0:
		camera.draw(input_box_blinker)

	input_box_end = gamebox.from_text(0, 0, input_text[-2:], 50, 'black')
	input_box_end.left, input_box_end.bottom = input_box_blinker.right, camera.bottom
	camera.draw(input_box_end)

	camera.draw(input_box)


def update_prompt():
	"""
    This function updates the prompt SpriteBoxes as the run_game() screen is being displayed:
        the image of the IDE on the right side of the screen,
        all the text that the player typed that will be submitted in the game.
    :return: None
    """
	global prompt_box, prompt_box_back

	ide_font_size = 20

	try:
		prompt_box_back = gamebox.from_image(0, 0, fn_ide)
		prompt_box_back.scale_by(0.5)
	except URLError:
		prompt_box_back	= gamebox.from_color(0, 0, 'lightblue', camera.width/2, camera.height)

	prompt_box_back.right, prompt_box_back.top = camera.right, camera.top
	camera.draw(prompt_box_back)

	for i in range(len(string_script_editor)):
		prompt_box[i] = gamebox.from_text(0, 0, string_script_editor[i], ide_font_size, 'white')
		prompt_box[i].left, prompt_box[i].top = prompt_box_back.left + 70, camera.top + i * 24 + 87

	for line in prompt_box:
		camera.draw(line)

	for i in range(len(string_script_editor)):
		if (turn + 5) == i:
			string_script_editor[i] = input_text


def update_timer():
	"""
    This function updates the timer SpriteBoxes as the run_game() screen is being displayed:
        the time remaining for the player to finish the assignment,
        the background for the time,
        the amount of lives the player currently has
    This function also updates the timer and start variables as integers
    that are not based on the game clock (tick speed), but of the computer clock with the time.py.
    This function also checks to see if the player is out of time.
    :return: None
    """
	global live_box
	global seconds_left
	global timer, timer_box, timer_box_back, start

	if start is 0:
		start = time()
	current = time()
	timer = current - start

	seconds_left = max_seconds - int(timer)
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


def update_instructions():
	"""
    This function updates the instructions SpriteBoxes as the run_game() screen is being displayed:
        text that tells the player either to press space to see the assignment,
        or text that tells the player that the last line submission was incorrect,
        a light gray background above the input box for the text.
    :return: None
    """
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


def update_pa_task(keys):
	"""
    This function updates the pa_task SpriteBoxes as the run_game() screen is being displayed:
        if the player is playing with random words, the four words will be shown when SPACE is pressed.
        if the player isn't, the task for PA01 will be shown when SPACE is pressed.
    :param keys: list of pygame constants, used to check if a computer key is pressed.
    :return: None
    """
	global pa_task_image, answers_box, is_random_answers
	if not is_random_answers:
		try:
			pa_task_image = gamebox.from_image(0, 0, fn_pa)
			pa_task_image.scale_by(0.8)

			pa_task_image.x = camera.x
			pa_task_image.y = camera.y
			if pygame.K_SPACE in keys:
				camera.draw(pa_task_image)
		except URLError:
			is_random_answers = True

	else:
		for i in range(len(answers_box)):
			answers_box[i] = gamebox.from_text(0, 0, answers[i], 40, 'black')
			answers_box[i].left, answers_box[i].top = camera.left, camera.top + i * 28 + 30

			answers_box_back = gamebox.from_color(
				answers_box[i].x, answers_box[i].y, "white", answers_box[i].width, answers_box[i].height)

			if pygame.K_SPACE in keys:
				camera.draw(answers_box_back)
				camera.draw(answers_box[i])


def update_lost():
	"""
    This function updates the lost SpriteBoxes when the player has lost:
        text displaying that the player lost,
        a white background for the above text,
        instructions for the player to play again or quit.
    :return: None
    """
	global lost, paused
	lost = True
	lost_box = gamebox.from_text(camera.x, camera.y, "You failed to submit...", 40, "darkred")
	lost_box_back = gamebox.from_color(camera.x, camera.y, "white", lost_box.width, lost_box.height)
	camera.draw(lost_box_back)
	camera.draw(lost_box)

	replay_box = gamebox.from_text(0, 0, "Press N to play again or press X to quit.", 30, "brown")
	replay_box.right, replay_box.bottom = camera.right, camera.bottom
	camera.draw(replay_box)

	paused = True


# MOVEMENTS

def move_camera():
	"""
    This function moves the camera such that the player is always in the same position relative to the camera.
    :return: None
    """
	camera.x = player.x + c_w / 4
	camera.y = player.y


def move_hud():
	"""
    This function updates all of the HUD elements as run_game() screen is being displayed:
    :return: None
    """
	update_prompt()
	update_inputs()
	update_timer()
	update_instructions()


def action_move(keys, obj):
	"""
    This function moves the player at a certain speed depending on what keys are pressed and lets
    the player select a key by pressing SPACE. The player may only select the key once; if the player
    wants to press a key successively, the player must move off of the key before selecting it again.
    This function prevents the player from going out of bounds.
    :param keys: list of pygame constants, used to check if a computer key is pressed.
    :param obj: SpriteBox, used to determine if a player is over a SpriteBox
    :return: None
    """
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
		action_select()

	for box in collision_boxes:
		player.move_to_stop_overlapping(box)


def action_select():
	"""
    This function defines what happens when the player selects a button:
        if "shift" is pressed, the next alphabetical letter will be uppercase.
        if spacebar is pressed, a space will be added to the typing string
        if enter is pressed, the typing string will be submitted if it's correct with the assignment.
        else, the letter will be added to the typing string
    :return: None
    """
	global lives
	global is_not_repeated, turn
	global typing_string, string_script_editor
	global buttons, answers, won, lost
	global display_not_correct
	global is_shifted

	if display_not_correct:
		display_not_correct = False

	if "shift" in get_hover_letter():
		is_shifted = True
	elif get_hover_letter() == backspace:
		if typing_string:
			typing_string = typing_string[:-1]
	elif get_hover_letter() == spacebar:
		typing_string += " "
	elif get_hover_letter() == enter:
		# win condition
		if typing_string == answers[-1] and (turn == 3):
			won = True
		# advance turn
		elif typing_string == answers[turn]:
			turn += 1
			lives += 1
		else:
			display_not_correct = True
			lives -= 1
			if lives <= 0:
				lost = True
		typing_string = ""
	else:
		if is_shifted:
			typing_string += get_hover_letter().upper()
			is_shifted = False
		else:
			typing_string += get_hover_letter().lower()

	is_not_repeated = False


def move_enemies():
	"""
    This function moves each enemy towards the player with a simple algorithm.
    This function does not prevent the enemies from overlapping each other.
    :return: None
    """
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


def collision():
	"""
    This function causes the player to lose a life if the player touches an enemy.
    :return: None
    """
	global lost, paused, lives
	for e in enemies:
		if player.touches(e):
			lives -= 1

			if lives <= 0:
				lost = True
			else:
				for e in enemies:
					e.x = randrange(left_col_box.right, right_col_box.left)
					e.y = randrange(top_col_box.bottom, bot_col_box.top)


def out_of_time(time):
	"""
    This function cause the player to lose if the player runs out of time.
    :param time: int, the current game countdown.
    :return: None
    """
	global lost
	if time <= 0:
		lost = True


# FUNCTIONS - SCREENS

def advance_screen(next_screen_number):
	"""
    This function allows the different screen functions to be toggled:
        each screen is given a camera screen number by comments
    This function also prevents the screens to be toggled successively, which is
    inherent in the way gamebox handles key presses.
    :param next_screen_number: int, a number of the next screen that prevents the function from
        "overshooting" to the following camera screen.
    :return: None
    """
	global camera_screen
	if camera_screen < next_screen_number:
		camera_screen += 1
	else:
		camera_screen = 0


# camera screen 0
def run_title(keys):
	"""
    This function runs the title screen when called in the tick function by drawing:
        a black background,
        the flavor text which acts as the pregame instructions,
        the instructions for selecting a game mode.
    :param keys: list of pygame constants, used to check if a computer key is pressed.
    :return: None
    """
	global camera_screen, debug, is_random_answers
	global difficulty

	camera.clear("black")

	# displaying the flavor
	font_size, y = 30, camera.top + 70

	credits_box = gamebox.from_text(
		0, 0, "A CS1111 Python Project by Roman Ramirez", font_size - 5, "orange")
	credits_box.right, credits_box.top = camera.right, camera.top
	camera.draw(credits_box)

	credits_box_2 = gamebox.from_text(
		0, 0, "rr8rk@virginia.edu", font_size - 5, "orange")
	credits_box_2.right, credits_box_2.top = camera.right, credits_box.bottom
	camera.draw(credits_box_2)

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
		advance_screen(1)
	elif pygame.K_2 in keys:
		difficulty = 1
		is_random_answers = True
		advance_screen(1)
	elif pygame.K_3 in keys:
		difficulty = 2
		is_random_answers = True
		advance_screen(1)

	if is_random_answers:
		randomize_answers()

	camera.display()


# camera screen 1
def run_game(keys):
	"""
    This function runs the game screen when called in the tick function by drawing:
        a black background, the keyboard, and the movements,
    while also checking if the player has either lost or won,
    and displays instructions if the player has lost.
    :param keys: list of pygame constants, used to check if a computer key is pressed.
    :return: None
    """
	# global camera_screen
	# global won, typing_string

	if not paused:
		# clear the camera
		camera.clear("black")

		# draw the background
		draw_background()

		# update the screen based on moving and check if lost
		move_camera()
		move_enemies()
		move_hud()

		if lost:
			update_lost()

		action_move(keys, buttons.values())
		update_pa_task(keys)

		if won:
			advance_screen(2)

		camera.display()

	else:
		# the selections in the lost screen
		if pygame.K_n in keys:
			advance_screen(-1)
		if pygame.K_x in keys:
			exit(0)


# camera screen 2
def run_win(keys):
	"""
    This function runs the win screen when called in the tick function by drawing:
        a black background,
        the "kytos" background of a submitted assignment,
        the total, current, submitted text,
        the time of submission,
        the instructions to either play again or quit.
    :param keys: list of pygame constants, used to check if a computer key is pressed.
    :return: None
    """
	camera.clear("black")

	try:
		submission_image = gamebox.from_image(0, 0, fn_submission)
	except URLError:
		submission_image = gamebox.from_color(0, 0, 'white', camera.width, camera.height*3/4)

	submission_image.width = camera.width
	submission_image.left = camera.left
	submission_image.top = camera.top
	camera.draw(submission_image)

	sub_font_size = 22

	for i in range(len(string_script_editor)):
		prompt_box[i] = gamebox.from_text(0, 0, string_script_editor[i], sub_font_size, 'black')
		prompt_box[i].left, prompt_box[i].top = camera.left + 95, camera.top + i * 18.75 + 159
		camera.draw(prompt_box[i])

	duration = max_seconds - seconds_left
	minutes = str(55 + duration // 60)

	if duration % 60 < 10:
		seconds = "0" + str(duration % 60)
	else:
		seconds = str(duration % 60)

	win_box = gamebox.from_text(
		camera.x, camera.y, "You submitted on time at 9:" + minutes + ":" + seconds + " PM!", 30, 'white')
	win_box.top = submission_image.bottom
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
		exit(0)

	camera.display()


# REFRESHING THE SCREEN
def tick(keys):
	"""
    This function runs the pygame, showing a screen depending on the camera_screen integer.
    :param keys: list of pygame constants, used to check if a computer key is pressed.
    :return: None
    """
	if camera_screen == 0:
		init_game()
		run_title(keys)
	elif camera_screen == 1:
		run_game(keys)
	elif camera_screen == 2:
		run_win(keys)


if __name__ == '__main__':
	gamebox.timer_loop(fps, tick)
