#!/usr/bin/python3
from datetime import datetime, time
"""
Module for my class
"""
class Day:
	def __init__(self, date, timestart, timefinish):	
		"""
		date - datetime, but without time :-) (%d.%m.%Y)
		timestart - datetime (%d.%m.%Y %H:%M)
		timefinish - datetime (%d.%m.%Y %H:%M)
		"""
		self.date = date
		self.timestart = timestart
		self.timefinish = timefinish
	def __str__(self):
		return(self.date.strftime('%d.%m.%y') + ': ' + self.timestart.strftime('%d.%m.%Y %H:%M')+\
			' - ' + self.timefinish.strftime('%d.%m.%Y %H:%M'))
	def gettimetuple(self):
		"""
		return tuple of start time and finish time
		"""
		return (self.timestart, self.timefinish)
class Pause:
	def __init__(self, weekday, time, duration):
		"""
		weekday - number
		time - datetime.time (datetime.time(hour, minute))
		duration - number, min
		"""
		self.weekday = weekday
		self.time = time
		self.duration = duration
	def __str__(self):
		return (str(self.weekday) + ': с '+ str(self.time) + ' в течении ' + str(self.duration) + ' мин.')
class Incident:
	def __init__(self, datetime, duration):
		"""
		datetime - datetime
		duration - number, min
		"""
		self.datetime = datetime
		self.duration = duration
	def __str__(self):
		return ('с ' + self.datetime.strftime('%d.%m.%Y %H:%M') + ' в течении ' + str(self.duration) + ' мин.')
class Unit:
	"""
	Unit class
	"""
	def __init__(self, code, delete = False, norm = 0):
		"""	
		code - code of unit
		delete - allow/deny, bool
		norm - norm, min.
		"""
		self.code = code
		self.delete = delete
		self.norm = norm
		self.days = {}
		self.incidents = {}
		self.pauses = {}
	def __str__(self):
		result = ''
		result += 'Code: ' + str(self.code) + '\n'
		result += 'Delete: ' + str(self.delete) + '\n'
		result += 'Norm: ' + str(self.norm) + ' min\n'
		for day in self.days:
			result += '\tDay ' + str(self.days[day]) + '\n'
		for pause in self.pauses:
			result += '\tPause ' + str(self.pauses[pause]) + '\n'
		for incident in self.incidents:
			result += '\tIncident ' + str(self.incidents[incident]) + '\n'
		return result
	def checkday(self, day):
		if day in self.days:
			lgood = self.days[day].gettimetuple()
			lbad = []
			return 'sss'
	def addday(self, day):
		self.days[day.date] = day
	def addincident(self, incident):
		self.incidents[incident.datetime] = incident
	def addpause(self, pause):
		self.pauses[pause.weekday] = pause

if __name__ == '__main__':
	unit = Unit('735')
	unit.addday(Day(datetime(2014, 4, 1), datetime(2014, 4, 1, 15, 0), datetime(2014, 4, 1, 17, 0)))
	unit.addday(Day(datetime(2014, 4, 2), datetime(2014, 4, 2, 15, 15), datetime(2014, 4, 2, 17, 0)))
	unit.addpause(Pause(1, time(hour = 15, minute = 0), 30))
	unit.addincident(Incident(datetime(2014,4,1,15,25), 30))
	print(unit)

	
