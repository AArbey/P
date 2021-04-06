# Created by OwlFight 
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#												#
#	File that does most of the connect 4 game	#
#												#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
# 				Thing to note:					#
# 1) For the whole file, the BOARD is an array	#
# with this form:								#
# [[ 0 , 0,  0 , 0 , 0 , 0 , 0 ],< this is a ROW#
#  [ 0 , 0,  0 , 0 , 0 , 0 , 0 ],				#
#  [ 0 , 0,  0 , 0 , 0 , 0 , 0 ],				#
#  [ 0 , 0,  0 , 0 , 0 , 0 , 0 ],				#
#  [ 0 , 0,  0 , 0 , 0 , 0 , 0 ],				#
#  [ 0 , 0,  0 , 0 , 0 , 0 , 0 ]]				#
#	 ^											#
# This colomn of 0 is refered as a LIGNE 		#
#												#
# 2) I give player 1 or 2 (player 1 or 2)		#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

def winDiagonol(board, row, ligne, player):
	
	diff = min(5-row, ligne)
	iniRow = row + diff
	iniLigne = ligne - diff
	counter = 0

	while iniLigne <= 6 and iniRow >= 0:
		
		if board[iniRow][iniLigne] == player:
			if counter == 3:
				return True
			else:
				counter = counter + 1
		else:
			counter = 0

		iniLigne = iniLigne + 1
		iniRow = iniRow - 1

	diff = min(5-row, 6-ligne)
	iniRow = row + diff
	iniLigne = ligne + diff
	counter = 0

	while iniLigne >= 0 and iniRow >= 0:

		if board[iniRow][iniLigne] == player:
			if counter == 3:
				return True
			else:
				counter = counter + 1
		else:
			counter = 0

		print(iniLigne,iniRow,counter,player,board[iniRow][iniLigne])
		iniLigne = iniLigne - 1
		iniRow = iniRow - 1

	return False


def winByLigne(board, ligne, player):

	counter = 0

	for i in range(6):

		if board[i][ligne] == player:
			if counter == 3:
				return True
			else:
				counter = counter + 1
		else:
			counter = 0

	return False


def winByRow(board, row, player):

	counter = 0

	for i in range(7):

		if board[row][i] == player:
			if counter == 3:
				return True
			else:
				counter = counter + 1
		else:
			counter = 0

	return False


def draw_board(board):
	text_board = ""
	for ligne in board:
		temp_ligne = ""
		for c in ligne:
			if c == 0:
				temp_ligne = temp_ligne + ":black_large_square:" 
			if c == 1:
				temp_ligne = temp_ligne + ":yellow_circle:" 
			if c == 2:
				temp_ligne = temp_ligne + ":red_circle:"
		temp_ligne = temp_ligne + "\n"
		text_board = text_board + temp_ligne
	return text_board


#I KNOW THIS IS A SHITTY WAY OF DOING THIS
def initial_board():
	return [[0,0,0,1,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]


class ConnectBoard(object):
	def __init__(self, messageID, placeHolder, board):
		self.messageID = messageID
		self.placeHolder = placeHolder
		self.board = board
		self.player = 1

	def left(self):

		place = self.placeHolder
		inital_place = place
		board = self.board
		IsNotPlaced = True

		while place > 0 and IsNotPlaced:

			if board[0][place-1] == 0:
				place = place - 1
				board[0][place] = self.player
				board[0][inital_place] = 0
				IsNotPlaced = False

			else:
				place = place - 1

		self.placeHolder = place
		self.board = board

		return draw_board(board)


	def right(self):

		place = self.placeHolder
		inital_place = place
		board = self.board
		IsNotPlaced = True

		while place < 6 and IsNotPlaced:

			if board[0][place+1] == 0:
				place = place + 1
				board[0][place] = self.player
				board[0][inital_place] = 0
				IsNotPlaced = False

			else:
				place = place + 1

		self.placeHolder = place
		self.board = board

		return draw_board(board)

	def place(self):

		place = self.placeHolder
		board = self.board
		row = 5
		IsNotPlaced = True
		color = board[0][place]

		while row - 1 >= 0 and IsNotPlaced:

			if board[row][place] == 0:
				board[row][place] = self.player
				board[0][place] = 0
				IsNotPlaced = False

			else:
				row = row - 1

		#check if player win
		if winByRow(board, row, self.player) or winByLigne(board, place, self.player) or winDiagonol(board, row, place, self.player):
			return True, "**Player "+str(self.player)+" has won**\n"+draw_board(board)

		if color == 1:
			self.player = 2
			board[0][3] = 2
		else:
			self.player = 1
			board[0][3] = 1

		self.placeHolder = 3
		self.board = board

		return False, draw_board(board)






