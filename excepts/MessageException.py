# -*- coding: utf-8 -*-

class MessageException(Exception):
	#一般表示用户输入异常，应该给予用户提示的异常类型
	
	def __init__(self, value):
		super().__init__()
		self.value	= value