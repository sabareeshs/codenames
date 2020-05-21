# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import uuid

from enum import Enum
from django.db import models

class Turn(Enum):
	BLUEMASTER = 'BM'
	REDMASTER = 'RM'
	BLUEAGENT = 'BA'
	REDAGENT = 'RA'
	
	@classmethod
	def choices(cls):
		return tuple((i.name, i.value) for i in cls)

class BoardStatus(Enum):
	BLUEWIN = 'BW'
	REDWIN = 'RW'
	INPROGRESS = 'IP'
	DRAW = 'DRAW'
	
	@classmethod
	def choices(cls):
		return tuple((i.name, i.value) for i in cls)

# Create your models here.
class Board(models.Model):
	turn = models.CharField(max_length=255, choices=Turn.choices(), default=(Turn.BLUEMASTER if random.getrandbits(1) else Turn.REDMASTER))
	status = models.CharField(max_length=255, choices=BoardStatus.choices(), default=BoardStatus.INPROGRESS)
	bluescore = models.IntegerField(default=0)
	redscore = models.IntegerField(default=0)
	num_clues = models.IntegerField(default=-1)
	num_clicks = models.IntegerField(default=-1)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=255, default=id)
	clue = models.CharField(max_length=255, default="")
	
	def __str__(self):
		return str(self.name)

	def __unicode__(self):
		return unicode(self.name)

class CardStatus(Enum):
	OPEN = 'O'
	CLOSED = 'C'
	
	@classmethod
	def choices(cls):
		return tuple((i.name, i.value) for i in cls)

class CardType(Enum):
	BLUE = 'B'
	RED = 'R'
	WHITE = 'W'
	
	@classmethod
	def choices(cls):
		return tuple((i.name, i.value) for i in cls)

class Card(models.Model):
	word = models.CharField(max_length=255)
	status = models.CharField(max_length=255, choices=CardStatus.choices())
	type = models.CharField(max_length=255, choices=CardType.choices())
	board = models.ForeignKey(Board, on_delete=models.CASCADE)

	def __str__(self):
		return self.word

	def __unicode__(self):
		return unicode(self.word)
