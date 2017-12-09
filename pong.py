#!/usr/bin/python3.6 -tt
# http://trevorappleton.blogspot.com.es/2014/04/writing-pong-using-python-and-pygame.html

# import the pygame libraries into our program so we have access to them
import pygame, sys, random
from pygame.locals import *

# Number of frames per second
# Change this value to speed up or slow down your game
FPS = 200

#Global Variables to be used through our program
# playgame (window) size
WINDOWWIDTH = 400
WINDOWHEIGHT = 300

# other global variables defining the height and the width we will add a few more variables.
LINETHICKNESS = 10
PADDLESIZE = 50
PADDLEOFFSET = 20

# Set up the colours
BLACK     = (0  ,0  ,0  )
WHITE     = (255,255,255)
ARENA      = (0, 127, 66)

#Draws the arena the game will be played in.
def drawArena():
    # fill Surface with a solid color
    # fill(color, rect=None, special_flags=0) -> Rect
    DISPLAYSURF.fill(ARENA)

    #Draw outline of arena
    # rect(Surface, color, Rect, width)
    #The width argument is the thickness to draw the outer edge. If width is zero then the rectangle will be filled.
    pygame.draw.rect(DISPLAYSURF, WHITE,  pygame.Rect(0, 0, WINDOWWIDTH, WINDOWHEIGHT), LINETHICKNESS*2)

    # Draw center line
    # draw a straight line segment
    # line(Surface, color, start_pos, end_pos, width=1) -> Rect
    # width requires an integer, so the divide is // --> In Python 3.0, 10 / 4 will return 2.5 and 10 // 4 will return 2.
    # The former is floating point division, and the latter is floor division, sometimes also called integer division.
    pygame.draw.line(DISPLAYSURF, WHITE, (WINDOWWIDTH/2, 0), (WINDOWWIDTH/2, WINDOWHEIGHT), LINETHICKNESS//4)
    return

#Draws the paddle
def drawPaddle(paddle):
    #Stops paddle moving too low
    # note must be > as the bottom can't be greater than
    if paddle.bottom > (WINDOWHEIGHT - LINETHICKNESS):
        paddle.bottom = (WINDOWHEIGHT - LINETHICKNESS)
    # Stops moving too high
    # Note must be < as the number can be lower than zero
    if paddle.top < (0 + LINETHICKNESS):
        paddle.top = (0 + LINETHICKNESS)

    # Draws recranglerect
    # rect(Surface, color, Rect, width=0)
    #The width argument is the thickness to draw the outer edge. If width is zero then the rectangle will be filled.
    pygame.draw.rect(DISPLAYSURF, WHITE, paddle, 0)
    return

#draws the ball
def drawBall(ball):
    # rect(Surface, color, Rect, width=0)
    #The width argument is the thickness to draw the outer edge. If width is zero then the rectangle will be filled.
    pygame.draw.rect(DISPLAYSURF, WHITE, ball, 0)
    return

#moves the ball returns new position
def moveBall(ball, ballDirX, ballDirY):
    # ball.x = ball.x + ballDirX
    ball.x += ballDirX
    ball.y += ballDirY
    return ball

# check colision to edges
def checkEdgeCollision(ball, ballDirX, ballDirY):
    # check top and bottom
    if ball.top < (0 + LINETHICKNESS):
        ballDirY = random.uniform(+0.5, +1.5) # +1
    if ball.bottom > (WINDOWHEIGHT - LINETHICKNESS):
        ballDirY = random.uniform(-1.5, -0.5) # -1
    # check left and right
    if ball.left < (0 + LINETHICKNESS):
        ballDirX = +1
    if ball.right > (WINDOWWIDTH - LINETHICKNESS):
        ballDirX = -1
    return(ballDirX, ballDirY)

#Checks if the ball has hit a paddle, and 'bounces' ball off it.
def checkHitBall(ball, paddle1, paddle2, ballDirX):
    # This line checks four things to see if the ball has been hit.
    # The first things it checks the direction of the ball. We only want to ball to be classed as being hit if it is hits the paddle from the front.
    # If it is hit from the rear it means you have missed the ball, so we will make the ball pass through the paddle until it is back in play.
    # The next three things it checks are to see the position of the ball relative to the paddle.
    # It checks if the right hand side of the paddle hits the left hand side of the ball AND that the top of the ball is lower than the top of the paddle AND the bottom of the ball is higher than the bottom of the paddle.
    # If these three AND statements are true, then the paddle has hit the ball so we return a -1 to flip the direction.

    # check hit of computer paddle
    if ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        return(-1) # change direction
    # check hit of player paddle
    elif ballDirX == 1 and paddle2.left == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
        return(-1) # change direction
    else: return(1) # keep direction

#Checks to see if a point has been scored returns new score
def checkPointScored(ball, paddle1, paddle2, ballDirX, score1, score2):
    # check player 1 (computer)
    if ballDirX == -1:
        if ball.left == LINETHICKNESS:
            score2 += 1  #1 point for player2 for hitting the ball
    if ballDirX == +1:
        if ball.right == (WINDOWWIDTH - LINETHICKNESS):
            score1 += 1  #1 point for player1 (COMPUTER) for hitting the ball
    return (score1, score2)

# Calling the render method on this object will return a Surface with the given text, which you can blit on the screen or any other Surface.
def displayScore(score1, score2):
    # creates a new surface called resultSurf.
    # takes the information from BASICFONT and renders it with the following information defined within the brackets
    # True refers to the fact we want anti-aliasing turned on
    resultSurf = BASICFONT.render('%s     %s' % (score1, score2), True, WHITE)
    # This creates a new rectangle called resultRect which is the same size as the surface we created on the previous line.
    # It uses a built in function of pygame called get_rect().
    resultRect = resultSurf.get_rect()
    resultRect.center = (WINDOWWIDTH/2, 25)     # position topleft, topcenter, centerx, ....
    DISPLAYSURF.blit(resultSurf, resultRect)    # blit to draw one image onto another: dest_surface.blit(source_surface, position)
    return

# Artificial Intelligence of computer player
# play similar to:
#        Once I have hit the ball I move to the centre of the court.
#        When my opponent has hit the ball I start to follow the ball so I can hit it back.
# The position of the ball so it can follow it.
# The direction of the ball so it knows if it is moving away or towards the computers paddle.
# The position of the paddle so it can adjust its position depending on what the ball is doing.
# The output will be the position of the paddle.
def artificialIntelligence(ball, ballDirX, paddle):
    #If ball is moving away from paddle, center paddle
    if ballDirX == +1:
        if paddle.centery < (WINDOWHEIGHT/2):
            paddle.y += 1
        elif paddle.centery > (WINDOWHEIGHT/2):
            paddle.y -= 1
    #If ball is moving to the paddle, follow the ball
    if ballDirX == -1:
        if paddle.centery < ball.y:
            paddle.y += 1
        elif paddle.centery > ball.y:
            paddle.y -= 1
    return(paddle)

#Main function
def main():
    # initialise pygame.
    pygame.init()
    # adding global allows us to modify the value later on.
    # We will be changing our surface, so it's important we can modify it when we need to.
    global DISPLAYSURF
    # Initialize a window or screen for display
    # assign some information to our surface, which sets the display width and height.
    # set_mode(resolution=(0,0), flags=0, depth=0) -> Surface
    # must be defined here otherwise will give error as DISPLAYSURF not available ????
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    # set the title of our window. Set the current window caption
    pygame.display.set_caption('Pong')

    # to set the frame rate ourselves
    FPSCLOCK = pygame.time.Clock()

    # To write the score, we have to create a Font (or SysFont) object.
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 20
    # create a Font object from the system fonts. SysFont(name, size, bold=False, italic=False) -> Font
    BASICFONT = pygame.font.SysFont('Arial.ttf', BASICFONTSIZE)
    # set initial score
    score1 = 0
    score2 = 0

    #Initiate variable and set starting positions
    #any future changes made within rectangles
    ballX = WINDOWWIDTH/2 - LINETHICKNESS/2
    ballY = WINDOWHEIGHT/2 - LINETHICKNESS/2
    playerOnePosition = (WINDOWHEIGHT - PADDLESIZE)/2
    playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE)/2


    # create initial position for ball
    # Rect (x,y,deltax, deltay)
    ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)
    # set initial ball dirction randomly
    # -1 left or up. +1 right or bottom
    ballDirX = random.choice([+1, -1])
    ballDirY = random.choice([+1, -1])

    # create initial position for paddles
    paddle1 = pygame.Rect(PADDLEOFFSET,playerOnePosition,LINETHICKNESS,PADDLESIZE)
    paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS, PADDLESIZE)

    #Draws the starting position of the Arena
    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    drawBall(ball)
    displayScore(score1, score2)


    while True: #main game loop
        # get() retrieves all events currently in the queue, and is usually used in a loop --> for event in pygame.event.get():
        # the loop simply won't run if there are no events. Generally, it is more common to use the get() version.
        # poll() retrieves only a single event:
        event = pygame.event.poll()
        # All events have a type identifier. http://www.pygame.org/docs/ref/event.html

        # check for quit. Window close?
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # User movement
        # move paddle through mouse movement commands
        # Moving the mouse will generate a new pygame.MOUSEMOTION event.
        if event.type == pygame.MOUSEMOTION:  # return (pos, rel, buttons)
            mousex, mousey = event.pos
            paddle2.y = mousey

        # Computer movement for paddle1
        paddle1 = artificialIntelligence (ball, ballDirX, paddle1)

        # Check if the ball has hit a paddle, and 'bounces' ball off it.
        # basically changes direction (+1, -1)
        ballDirX = ballDirX * checkHitBall(ball, paddle1, paddle2, ballDirX)

        # check colision to edges
        ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)

        # Check if the ball has scored
        score1, score2 = checkPointScored(ball, paddle1, paddle2, ballDirX, score1, score2)

        # Moves the ball
        ball = moveBall(ball, ballDirX, ballDirY)


        # makes the cursor invisible
        pygame.mouse.set_visible(0)
        # Udates the graphic display
        drawArena() # needed to clean the surface before ball and paddle moves
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        drawBall(ball)
        displayScore(score1, score2)


        #  we can just ask the screen to update.
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()
