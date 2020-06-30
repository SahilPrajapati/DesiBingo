from network import Network
import pygame
import numpy as np
import os
from tkinter import *
from tkinter import messagebox
import time

# activate the pygame library .
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

rect = (50, 50, 250, 250)

# define the RGB value
# for white colour
white = (255, 255, 255)

# assigning values to X and Y variable
X = 250
Y = 320

# create the display surface object
# of specific dimension..e(X, Y).
win = pygame.display.set_mode((X, Y))

# It will store the indexes of numbers 0-24 which are randomly distribute on the 5X5 board.
# The indices of the number is stored as a tuple (i,j).
index = {}

# Playing board in which the numbers 0 - 24 are stored.
board = np.random.permutation(25).reshape((5, 5))

# flag board whose index(i,j) will tell whether the number stored at (i,j) has been marked on the board or not.
# initialized with false(zeros), because initially no number has been marked.
boolArray = np.zeros((5, 5))

# storing the indices of the board
for i in range(5):
    for j in range(5):
        index[board[i][j]] = (i, j)

# set the pygame window name
pygame.display.set_caption('Player 2')

# List to store all the objects of images, which are to be presented at the board.
# index 0 - 24 : images of numbers 0-24
# index 25     : image of cross which will be blitted on that no. which is marked
# index 26 - 30 : image of letters B,I,N,G,O
# index 31 - 35 : images of crossed letters B,I,N,G,O
image = []
for i in range(25):
    pic = str(i) + '.jpg'
    image.append(pygame.image.load(os.path.join("images", pic)))

image.append(pygame.image.load(os.path.join("images", "cross.jpg")))

image.append(pygame.image.load(os.path.join("images", "B.jpg")))
image.append(pygame.image.load(os.path.join("images", "I.jpg")))
image.append(pygame.image.load(os.path.join("images", "N.jpg")))
image.append(pygame.image.load(os.path.join("images", "G.jpg")))
image.append(pygame.image.load(os.path.join("images", "O.jpg")))

image.append(pygame.image.load(os.path.join("images", "Bcross.jpg")))
image.append(pygame.image.load(os.path.join("images", "Icross.jpg")))
image.append(pygame.image.load(os.path.join("images", "Ncross.jpg")))
image.append(pygame.image.load(os.path.join("images", "Gcross.jpg")))
image.append(pygame.image.load(os.path.join("images", "Ocross.jpg")))


def click(pos):
    """
    :return: pos (x, y) in range 0-7 0-7
    """
    x = int(pos[0] / 50)
    y = int(pos[1] / 50)

    return x, y


# To count no. of lines(row, column, diagonal) which are completely marked
def countScore():
    count = 0

    for i in range(5):
        flag = True
        for j in range(5):
            if not boolArray[i, j]:
                flag = False
                break
        if flag:
            count += 1

    for j in range(5):
        flag = True
        for i in range(5):
            if not boolArray[i, j]:
                flag = False
                break;
        if flag:
            count += 1

    for i in range(5):
        if not boolArray[i, i]:
            break
        if i == 4:
            count += 1

    for i in range(5):
        if not boolArray[i, 4 - i]:
            break
        if i == 4:
            count += 1

    return count


def read_pos(str):
    return int(str)


def make_pos(tup):
    return str(tup)


# completely fill the surface object
# with white colour
win.fill(white)

# copying the image surface object
# to the display surface object at
# (0, 0) coordinate.

for i in range(5):
    for j in range(5):
        win.blit(image[board[i, j]], (i * 50, j * 50))

# Blitting letters B,I,N,G,O
win.blit(image[26], (0, 260))
win.blit(image[27], (50, 260))
win.blit(image[28], (100, 260))
win.blit(image[29], (150, 260))
win.blit(image[30], (200, 260))

# separator of cyan color
pygame.draw.rect(win, (0, 255, 255), (0, 250, 250, 10))
pygame.draw.rect(win, (0, 255, 255), (0, 310, 250, 10))

# infinite loop
number = -1
n = Network()
player = int(n.getP())
went = False
print("You are player", player)

while True:

    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
    for event in pygame.event.get():

        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        pygame.display.update()
        if event.type == pygame.QUIT:
            # deactivates the pygame library
            pygame.quit()

            # quit the program.
            quit()

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            i, j = click(pos)
            print(i, " ", j)
            if i < 5 and j < 5 and went is False:
                # blitting green marked image for a while
                win.blit(pygame.image.load(os.path.join("images", "crossR.jpg")), (i * 50, j * 50))
                pygame.display.update()

                # Now blitting permanent red marked image over that number at pos (i,j)
                win.blit(image[25], (i * 50, j * 50))

                # Sending the information to the server
                print("sending to server")
                game = n.send(make_pos(board[i, j]))
                print("number : ", game.move)
                print("sent to server")

        game = n.send(make_pos(number))
        number = game.move
        went = game.went[player]

        if number != -1:
            previousScore = countScore()
            print(number)

            clickedIndex = index[number]

            if not boolArray[clickedIndex[0], clickedIndex[1]]:
                win.blit(pygame.image.load(os.path.join("images", "crossR.jpg")),
                         (clickedIndex[0] * 50, clickedIndex[1] * 50))
                pygame.display.update()
                time.sleep(0.4)

            win.blit(image[25], (clickedIndex[0] * 50, clickedIndex[1] * 50))
            boolArray[clickedIndex[0], clickedIndex[1]] = True

            score = countScore()
            print("score : ", score)

            if score > 0:
                if score > 5:
                    score = 5

                # blitting crossed BINGO letters upto score
                for i in range(score - previousScore):
                    win.blit(image[30 + previousScore + i + 1], ((previousScore + i) * 50, 260))

                # If other player won the match
                if score < 5 and game.wins[1 - player]:
                    window = Tk()
                    window.withdraw()
                    messagebox.showinfo("Result", "Loser is : Player 2")
                    pygame.quit()
                    quit()
                    window.destroy()

            pygame.display.update()

            # If the current player marked atleast 5 lines, then it is expected to win.
            if score >= 5:

                game.wins[player] = True
                n.send("25")
                print("Winner : ", game.wins[player], " ", game.wins[1 - player])
                time.sleep(1)

                # signal to the server that the current player is going to win
                game = n.send("25")

                # If other player also going to win, then the match is DRAWN
                if game.wins[1 - player]:
                    window = Tk()
                    window.withdraw()
                    messagebox.showinfo("Result", "Game Draw")
                    pygame.quit()
                    quit()
                    window.destroy()


                # Otherwise current player wins the match
                else:
                    window = Tk()
                    window.withdraw()
                    messagebox.showinfo("Result", "Winner is : Player 2")
                    pygame.quit()
                    quit()
                    window.destroy()

            number = -1
            game.move = -1
            pygame.display.update()

        # Draws the surface object to the screen.
        pygame.display.update()
