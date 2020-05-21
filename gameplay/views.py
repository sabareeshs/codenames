# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import redirect
from codenames.settings import STATIC_DIR
from gameplay.forms import BoardForm, CluesForm
from django.contrib import messages

from gameplay.models import Board, Card, CardStatus, CardType, Turn, BoardStatus

import random

def get_words():
	list = '/wordlist_1.txt' if random.getrandbits(1) else '/wordlist_2.txt'
	file = open(STATIC_DIR + list, 'r')
	return random.sample(file.readlines(), 25)

def new_board(name):
	board = Board.objects.get_or_create(name=name)
	board[0].save()
	words = get_words()
	words_per_color = int(words/2)
	type = []
	for i in range(words_per_color):
		type.append(CardType.RED)
		type.append(CardType.BLUE)
	type.append(CardType.WHITE)
	random.shuffle(type)
	for i in range(words_per_color):
		card = Card.objects.get_or_create(word=words[i].strip(), status=CardStatus.OPEN, type=type[i], board=board[0])
		card[0].type = type[i]
		card[0].status = CardStatus.OPEN
		card[0].save()
	return board[0]

def is_turn(player, board):
	return board.status == "BoardStatus.INPROGRESS" and ((board.turn == "Turn.BLUEMASTER" and player == 'blue_master') or (board.turn == "Turn.REDMASTER" and player == 'red_master') or (board.turn == "Turn.BLUEAGENT" and player == 'blue_agent') or (board.turn == "Turn.REDAGENT" and player == 'red_agent'))

# actual views
def num_clues(request, board_id):
	board = Board.objects.get(id=board_id)
	if request.method == 'POST':
		form = CluesForm(request.POST)
		if form.is_valid():
			board.num_clues = form.cleaned_data['num_clues']
			board.clue = form.cleaned_data['clue']
			board.num_clicks = 0
			board.save()
			if board.turn == "Turn.BLUEMASTER":
				return redirect('/gameplay/' + str(board.id) + '/blue_master')
			else:
				return redirect('/gameplay/' + str(board.id) + '/red_master')
	form = CluesForm()
	return render(request, 'gameplay/num_clues.html', {'form': form, 'board': board})
	
def create_board(request):
	if request.method == 'POST':
		form = BoardForm(request.POST)
		if form.is_valid():
			board = new_board(name=form.cleaned_data['name'])
			if board.turn == "Turn.BLUEMASTER":
				return redirect('/gameplay/' + str(board.id) + '/blue_master')
			else:
				return redirect('/gameplay/' + str(board.id) + '/red_master')
	form = BoardForm()
	return render(request, 'gameplay/create_board.html', {'form': form})


def index(request):
	boards = Board.objects.all()[:10]
	context_dict = {'boards': boards}
	return render(request, 'index.html', context=context_dict)

def delete(request, board_id):
	Board.objects.filter(id=board_id).delete()
	boards = Board.objects.all()[:10]
	context_dict = {'boards': boards}
	return render(request, 'index.html', context=context_dict)
	
def board(request, board_id, player):
	board = Board.objects.get(id=board_id)
	cards = Card.objects.filter(board=board)
	context_dict = {'board': board, 'cards': cards, 'is_turn': is_turn(player, board)}
	if player[-6:] == "master":
		return render(request, 'gameplay/master.html', context=context_dict)
	elif player[-5:] == "agent":
		return render(request, 'gameplay/agent.html', context=context_dict)

def change_turn(board, force=False):
	if force or (board.num_clicks >= board.num_clues):
		if board.turn == "Turn.BLUEMASTER":
			board.turn = Turn.BLUEAGENT
		elif board.turn == "Turn.BLUEAGENT":
			board.num_clues = -1
			board.clue = ""
			board.turn = Turn.REDMASTER
		elif board.turn == "Turn.REDMASTER":
			board.turn = Turn.REDAGENT
		else:
			board.clue = ""
			board.num_clues = -1
			board.turn = Turn.BLUEMASTER
		board.num_clicks = 0
		board.save()

def end_turn(request, board_id, player):
	board = Board.objects.get(id=board_id)
	if is_turn(player, board):
		change_turn(board, force=True)
	return redirect('board', board_id=board_id, player=player)

def card_click(request, board_id, word, player):
	board = Board.objects.get(id=board_id)
	cards = Card.objects.filter(board=board)
	card = cards.get(word__exact=word)
	end_turn = False
	end_game = False
	if (is_turn(player, board)):
		card.status = CardStatus.CLOSED
		card.save()
		if card.type == "CardType.BLUE" and player == "blue_agent":
			board.bluescore = board.bluescore + 1
		elif card.type == "CardType.RED" and player == "red_agent":
			board.redscore = board.redscore + 1
		elif card.type == "CardType.WHITE":
			board.status = BoardStatus.BLUEWIN if player == "red_agent" else BoardStatus.REDWIN 
			messages.info(request, 'You lost by revealing the Taboo card!!.')
		else:
			end_turn = True
		if len(Card.objects.filter(board=board).filter(status="CardStatus.CLOSED")) == 24:
			if board.bluescore > board.redscore:
				board.status = BoardStatus.BLUEWIN
			elif board.redscore > board.bluescore:
				board.status = BoardStatus.REDWIN
			else:
				board.status = BoardStatus.DRAW

		board.num_clicks = board.num_clicks + 1
		board.save()
		# increase score if the correct card is clicked 
		change_turn(board, end_turn)
	return redirect('board', board_id=board_id, player=player)
