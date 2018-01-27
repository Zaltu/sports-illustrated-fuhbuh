from libs.namespace import Namespace
from src.play import play


STANCES = ['Offense', 'Defense', 'Kick', 'Return']
GAME = Namespace()
GAME.clock = ['1st', 720]
GAME.simplePriorityLow = ['+', '-']

GAME.playmap = {
	'+': play.soft
 	'-': play.soft,
	':+': play.hard,
	':-': play.hard,
	'OP': lambda t='OP':play.penalty(towards=t),
	'DF': lambda t='DF':play.penalty(towards=t),
	'PI': lambda t='PI':play.penalty(towards=t),
	'0': play.incomplete,
	':+TD': play.hard,
	'QT': play.qtrouble,
	'INT': play.intercept,
	'F+': play.fumble,
	'F-': play.fumble,
	'BK-': play.fumble
}

GAME.priority = {
	
}