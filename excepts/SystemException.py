# -*- coding: utf-8 -*-

class SystemException(Exception):
	#异常表示系统异常，不应该展示在客户端
	
	def __init__(self, value):
		super().__init__()
		self.value	= value