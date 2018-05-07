#### Final Project for CHEME5500 aio23 ####

import pygame
from pygame.locals import *
import requests
import random
import string


class Hangman():

    def __init__(self):
        '''
        __init__ function. Initiates main game variables and
        pygame screen.
        '''
        ##Start game main variables
        self.word_input = False
        self.start_screen = True

        ## Set icon and widow caption
        icon=pygame.Surface((32,32))
        icon=pygame.transform.scale(pygame.image.load('Images\\ballons.png'), (32, 32))
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Hangman")

        pygame.init()
        self.screen = pygame.display.set_mode((600, 400))

        #call main function to play game
        self.gameplay()


    def gameplay(self):
        '''
        Main pygame code logic. Checks what screen needs to be diplayed.
        '''
        in_game = True
        self.streak = 0
        self.long_streak = 0
        self.start_screen_disp()
        self.win_lose = False

        #main game loop
        while in_game:
            for event in pygame.event.get():
                #checks if the user wants to quit the game
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
                    in_game = False

                #displays the start screen and waits for input
                elif self.start_screen == True:
                    self.start_screen_disp()
                    if event.type == pygame.KEYDOWN and event.key == K_SPACE:
                        self.new_word = ''
                        self.word_input_disp('')
                        self.word_input = True
                        self.start_screen = False
                    elif event.type == pygame.KEYDOWN and event.key == K_RETURN and not self.word_input:
                        self.game_vars_init()
                        self.gameplay_disp()
                        self.start_screen = False

                #diplays a screen asking the user to type a word to play
                elif self.word_input and event.type == pygame.KEYDOWN:
                    input_word = self.get_input_word(event)
                    if not input_word[0]:
                        self.word_input_disp(input_word[1])
                    else:
                        self.set_input = False
                        self.start_screen = True

                #displays the main game or a winning/losing screen if the game was won/lost.
                elif not (self.word_input or self.start_screen) and event.type == pygame.KEYDOWN:
                    if self.win_lose[0]:
                        self.win_lose_disp(self.win_lose[1], event)
                    else:
                        self.playgame(event)
                        self.gameplay_disp()
                        if self.win_lose[0]:
                            self.win_lose_disp(self.win_lose[1], event)

    def playgame(self, event):
        '''
        The main logic of the Hangman game. Checks if the input is valid,
        checks if the letters are in the word, and checks if the user
        guessed the word right. Also updates the current and longest streak.
        '''

        key_pressed = str(pygame.key.name(event.key))

        #checks if valid letter
        if key_pressed in string.ascii_lowercase:
            letter_pressed = key_pressed.upper()

            #checks if letter on the word and if the letter has not been used already.
            if letter_pressed in self.word and letter_pressed not in self.letters_used:
                self.comment = "You guessed right!"
                indexes = [i for i,val in enumerate(self.word) if val==letter_pressed]
                for i in indexes:
                    self.guessed_word[i] = letter_pressed
                self.letters_used.append(letter_pressed)

            #if letter was used already it tells the user.
            elif letter_pressed in self.letters_used:
                self.comment = "You already used that letter, try another one!"

            #if the user guessed wrong it updates the picture used and the attempts left
            else:
                self.comment = "Bad Guess"
                self.bad_guess_num -= 1
                self.letters_used.append(letter_pressed)
                self.img_name = "man_%s2.jpg" % str(7 - int(self.bad_guess_num))

        #tells the user if a pressed key is not valid
        else:
            self.comment = "You didn't press a valid key"

        #checks if the user has won
        if self.word == "".join(x for x in self.guessed_word):
            if not self.win_lose[0]:
                self.win_lose = [True, True]
                self.streak += 1
                if self.streak > self.long_streak:
                    self.long_streak = self.streak

        #checks if the user has lost
        elif self.bad_guess_num == 0:
            self.win_lose = [True, False]
            self.streak = 0

    def game_vars_init(self):
        '''
        Function that initiates all the variables for a new game
        '''
        #checks if there is a word set by the user
        try:
            if self.new_word != '':
                self.word = self.new_word
                self.new_word = ''
            else:
                self.word = self.get_dict_word()
        except:
            self.word = self.get_dict_word()

        #initiates main game variables
        self.letters_used = []
        self.guessed_word = ['__' for i in range(len(self.word))]
        self.bad_guess_num = 7
        self.comment = "Start Guessing!"
        self.img_name = "man_02.jpg"
        self.win_lose = [False, None]


    def get_dict_word(self):
        '''
        Get word from online dictionary, if the dictionary was already
        loaded it doens't load it again.
        '''

        #checks if the dictionary was loaded already. If not it loads it from online.
        try:
            word = random.choice(list_words)
            while len(word) < 4:
                word = random.choice(list_words)
            return word.upper()
        except UnboundLocalError:
            word_site = "http://www-01.sil.org/linguistics/wordlists/english/wordlist/wordsEn.txt"
            response = requests.get(word_site)
            list_words = response.content.splitlines()
            word = random.choice(list_words)
            while len(word) < 4:
                word = random.choice(list_words)
            return word.upper()

    def start_screen_disp(self):
        '''
        Display start screen that asks for input from the User.
        The user can either press Enter to continue with a random
        word or input their own word.
        '''

        self.screen.fill((255, 255, 255))
        start_instructions = self.rendering("Press Enter to continue...")
        start_instructions2 = self.rendering("or Space to set your own word.")
        start_Img = pygame.transform.scale(pygame.image.load('Images\\start.jpg'),(400, 200))

        self.screen.blit(start_Img, (100, 50))
        self.screen.blit(start_instructions,
                    (300 - start_instructions.get_width() // 2, 260))
        self.screen.blit(start_instructions2,
                    (300 - start_instructions2.get_width() // 2, 280))

        pygame.display.flip()

    def word_input_disp(self, text):
        '''
        Display the word the user is typying.
        '''

        self.screen.fill((255, 255, 255))
        word_prompt = self.rendering("Write the word you want to use:")
        disp_word = self.rendering(self.new_word)
        word_instruct = self.rendering(text)

        self.screen.blit(word_prompt, (300 - word_prompt.get_width() // 2, 50))
        self.screen.blit(disp_word, (300 - disp_word.get_width() // 2, 80))
        self.screen.blit(word_instruct, (300 - word_instruct.get_width() // 2, 110))

        pygame.display.flip()

    def gameplay_disp(self):
        '''
        Displays Main Game. Includes the man image, the streak,
        the word, the letters already used, and the tries left.
        '''
        self.screen.fill((255, 255, 255))
        guessed_word = self.rendering(" ".join(x for x in self.guessed_word))
        comment = self.rendering(self.comment)
        letters_used = self.rendering(" ".join(x for x in self.letters_used), size=18)
        Img = pygame.transform.scale(pygame.image.load('Images\\' + self.img_name),(290, 290))
        streak = self.rendering("Current Streak: " + str(self.streak))
        long_streak = self.rendering("Longest Streak: " + str(self.long_streak))

        self.screen.blit(long_streak, (5,0))
        self.screen.blit(streak, (5,20))
        self.screen.blit(Img, (5, 55))
        self.screen.blit(comment, (450 - comment.get_width() // 2, 0))
        self.screen.blit(self.rendering("Letters Used:"), (300, 240))
        self.screen.blit(letters_used, (300, 265))
        self.screen.blit(guessed_word, (450 - guessed_word.get_width() // 2, 180))
        self.screen.blit(self.rendering("Ballons Remaining:"),(300, 330))
        self.screen.blit(self.rendering(str(self.bad_guess_num)),(450, 360))
        pygame.display.flip()

    def win_lose_disp(self, win_lose, event):
        '''
        Displays the winning or losing screen. Asks the user to Press
        Enter to continue playing.
        '''

        #checks if user has pressed Enter to restart the game.
        if event.key == K_RETURN:
            self.start_screen = True
            return

        if win_lose:
            img = pygame.transform.scale(pygame.image.load('Images\\winning.jpg'),
                                             (290, 290))
            text = self.rendering("The word was: " + self.word, width=600)
            man_img = pygame.transform.scale(pygame.image.load('Images\\' + self.img_name),(290, 290))

        elif not win_lose:
            img = pygame.transform.scale(pygame.image.load('Images\\losing.jpg'),
                                             (290, 290))
            text = self.rendering("The correct word was: " + self.word, width=600)

            #if the user keeps pressing letters after losing,
            #the picture at the end doesn't change. This happens
            #when the user presses keys too fast before the display
            #can be updated
            try:
                man_img = pygame.transform.scale(pygame.image.load('Images\\' + self.img_name),(290, 290))
            except:
                man_img = pygame.transform.scale(pygame.image.load('Images\\man_72.jpg'),(290, 290))

        self.screen.fill((255, 255, 255))
        self.screen.blit(img,(305, 55))
        self.screen.blit(text, (300 - text.get_width() // 2, 5))
        self.screen.blit(man_img, (5, 55))
        self.play_again = self.rendering("Press Enter to Play Again")
        self.screen.blit(self.play_again,
                         (300 - self.play_again.get_width() // 2, 370))
        pygame.display.flip()

    def get_input_word(self, event):
        '''
        Gets the input from the user and makes a new word out of it.
        The user can use backspace erase a letter and press Enter
        to use the word typed. Returns a list.
        '''

        key_pressed = str(pygame.key.name(event.key))
        word_instruct = "Press Enter to Continue"

        #checks if key pressed is a letter
        if key_pressed in string.ascii_lowercase:
            letter_pressed = key_pressed.upper()
            self.new_word += letter_pressed

        #cheks if the user finished typying a word
        elif event.key == K_RETURN:
            if len(self.new_word) > 0:
                self.word_input = False
                self.start_screen = False
                return [True, word_instruct]
            elif not self.new_word:
                word_instruct = "You didn't type a word"

        #checks if the user wants to erase a letter from the word
        elif event.key == K_BACKSPACE and len(self.new_word) > 0:
            self.new_word = self.new_word[:-1]

        #if key pressed not valid then it tells the user
        else:
            word_instruct = "You didn't press a valid key"

        return [False, word_instruct]

    def rendering(self, string_to_convert, color=(0, 0, 0), size=20, width=300):
        '''
        Pygame code to diplay text on the screen. Was using this too many times,
        so I made it it's own function.
        '''

        font = pygame.font.SysFont("comicsansms", size)

        #checks that the size of the text displayed is less that the space it will be on
        #default size half of the screen.
        if font.size(string_to_convert)[0] > width:
            size -= 1
            return self.rendering(string_to_convert, size=size, width=width)

        return font.render(string_to_convert, True, color)

game = Hangman()
