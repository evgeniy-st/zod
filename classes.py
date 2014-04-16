#!/usr/bin/python3
from datetime import datetime, time, timedelta, date
import segment
"""
Module for my class
"""
class Day:
	"""
	Describes the day of unit
	"""
	def __init__(self, date, timestart, timefinish):	
		"""
		date - datetime, but without time :-) (%d.%m.%Y)
		timestart - datetime (%d.%m.%Y %H:%M)
		timefinish - datetime (%d.%m.%Y %H:%M)
		"""
		if type(date) == datetime:
			self.day = date.date()
		else:
			self.day = date
		self.timestart = timestart
		self.timefinish = timefinish
	def __str__(self):
		return(self.day.strftime('%d.%m.%y') + ': ' + self.timestart.strftime('%d.%m.%Y %H:%M')+\
			' - ' + self.timefinish.strftime('%d.%m.%Y %H:%M'))
	def gettimetuple(self):
		"""
		Return: tuple of start time and finish time
		"""
		return (self.timestart, self.timefinish)
class Pause:
	"""
	Describes the pause in work of unit
	"""
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
	"""
	Describes the incident in work of unit
	"""
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
		result = 'Code: ' + str(self.code) + '\n'
		result += 'Delete: ' + str(self.delete) + '\n'
		result += 'Norm: ' + str(self.norm) + ' min\n'
		for day in self.days:
			result += '\tDay ' + str(self.days[day]) + '\n'
		for pause in self.pauses:
			result += '\tPause ' + str(self.pauses[pause]) + '\n'
		for day in self.incidents:
			for incident in self.incidents[day]:
				result += '\tIncident ' + str(incident) + '\n'
		return result
	def checkday(self, day):
		"""
		Check the day of unit
		Input: day - datetime/date, tested day
		Return: value of work unit or None
		"""
		if type(day) == datetime:
			day = day.date()
		if day in self.days:
			lgood = self.days[day].gettimetuple()
			lbad = []
			if day.weekday() in self.pauses:
				thStart = datetime.combine(day, self.pauses[day.weekday()].time)
				thEnd = thStart + timedelta(seconds = (self.pauses[day.weekday()].duration*60))
				lbad.append((thStart, thEnd))
			if day in self.incidents:
			        for inc in self.incidents[day]:
			                dtStart = inc.datetime
			                dtEnd = dtStart + timedelta(minutes = inc.duration)
			                lbad.append((dtStart, dtEnd))
			lbad = segment.union(lbad)
			result = (lgood[1] - lgood[0]).total_seconds()/60
			for l in lbad:
			        z = segment.getintersection(lgood, l)
			        if z:
			                result -= (z[1] - z[0]).total_seconds()/60
			return result
	def checkdays(self, days=None):
		"""
		Check the days of unit
		Input: day - tested day:
			- if None then check all days
			- if date/datetime then check one day
			- if list of date/datetime then check list of days
		Return: list of tuple (day, value) of work unit or None
		"""
		if not days :
			return [(day, self.checkday(day)) for day in self.days]
		elif type(days) == type([]):
			return [(day, self.checkday(day)) for day in days]
		elif type(days) == datetime or type(days) == date:
			return [(days, self.checkday(days))]
	def addday(self, addday):
		"""
		Add day to unit
		addday - Day object
		"""
		self.days[addday.day] = addday
	def addincident(self, incident):
		"""
		Add incidetn to unit
		incident - Incident object
		"""
		incidentdate = incident.datetime.date()
		if incidentdate not in self.incidents:
			self.incidents[incidentdate] = [incident]
		else:
			self.incidents[incidentdate].append(incident)
	def addpause(self, pause):
		"""
		Add pause to unit
		pause - Pause object
		"""
		self.pauses[pause.weekday] = pause
	def setnorm(self, norm):
		"""
		Set norm of unit
		norm - digital, min
		"""
		self.norm = norm
	def getrating(self, days):
		"""
		Calculate rating of unit for days
		Input: days - list of Day objects
		Return tupe: code_of_unit, norm_of_unit, list_days_w_value_rating, num_all_day,
			     num_good_day, percent, message	
		"""
		daysvalue = self.checkdays(days)
		numdays = len([y for y in daysvalue if y[1]])
		numgooddays = len([x for x in [y[1] for y in daysvalue if y[1]] if x <= self.norm])
		percent = round(numgooddays/numdays*100, 2)
		message = '1' if percent>=90 else '0'
		return self.code, self.norm, daysvalue, numdays, numgooddays, percent, message
		
class SuperUnit():
	"""
	SuperUnit class
	"""
	def __init__(self, code):
		"""
		Input code of SuperUnit
		"""
		self.code = code
		self.units = {}
	def __str__(self):
		result = 'SuperUnit: ' + str(self.code) + '\n'
		for unit in self.units:
			result += str(self.units[unit]) + '\n'
		return result 
	def addunit(self, unitcode):
		"""
		Create Unit object in SuperUnit
		Input: unitcode - code of new unit
		"""
		if unitcode not in self.units:
			self.units[unitcode] = Unit(unitcode)
	def adddaytounit(self, unitcode, day):
		"""
		Add Day object to unit
		If unit does`n present then create new unit
		Input:  unitcode - code of unit
			day - Day object
		"""
		self.addunit(unitcode)
		self.units[unitcode].addday(day)
	def addincidenttounit(self, unitcode, incident):
		"""
		Add Inciden object to unit
		If unit does`n present then create new unit
		Input:  unitcode - code of unit
			incident - Incident object
		"""
		self.addunit(unitcode)
		self.units[unitcode].addincident(incident)
	def addpausetounit(self, unitcode, pause):
		"""
		Add Inciden object to unit
		If unit does`n present then create new unit
		Input:  unitcode - code of unit
			incident - Incident object
		"""
		self.addunit(unitcode)
		self.units[unitcode].addpause(pause)
	def checkdaysunit(self, unitcode, days=None):
		"""
		Check day of unit
		Input:  unitcode - code of unit
			days - list of check day
		Return: list of tuple (day, value) of work unit or None
		"""
		if unitcode in self.units:
			return self.units[unitcode].checkdays(days)
	def setnormunit(self, unitcode, norm):
		"""
		Set norm of unit
		Input:  unitcode - code of unit
			norm - norm of unit
		"""
		self.addunit(unitcode)
		self.units[unitcode].setnorm(norm)
	def getratingunits(self, days):
		"""
		Return rating all units of SuperUnit
		"""
		return [(self.code,) + self.units[unit].getrating(days) for unit in self.units\
		if not self.units[unit].delete]
	def getratingsuperunit(self, days):
		"""
		Return rating of superunit
		"""
		unitsvalue = self.getratingunits(days)
		numdays = len(unitsvalue)
		numgooddays = len([x for x in unitsvalue if x[7]=='1'])
		percent = round(numgooddays/numdays*100, 2)
		message = 'КПЭ выполнен' if percent>=90 else 'КПЭ не выполнен'
		return self.code, numdays, numgooddays, percent, message
class MegaUnit():
	def __init__(self):
		self.superunits = {}
	def __str__(self):
		result = ''
		for superunit in self.superunits:
			result += str(self.superunits[superunit]) + '\n'
	def addsuperunit(self, sunitcode):
		if sunitcode not in self.superunits:
			self.superunits[sunitcode] = SuperUnit(sunitcode)
	def adddaytounit(self, sunitcode, unitcode, day):
		self.addsuperunit(sunitcode)
		self.superunits[sunitcode].adddaytounit(unitcode, day)
	def addincidenttounit(self, sunitcode, unitcode, incident):
		self.addsuperunit(sunitcode)
		self.superunits[sunitcode].addincidenttounit(unitcode, incident)
	def addpausetounit(self, sunitcode, unitcode, pause):
		self.addsuperunit(sunitcode)
		self.superunits[sunitcode].addpausetounit(unitcode, pause)
	def setnormunit(self, sunitcode, unitcode, norm):
		self.addsuperunit(sunitcode)
		self.superunits[sunitcode].setnormunit(unitcode, norm)
	def getrating(self, days):
		result = []
		for sunit in self.superunits:
			result.append(self.superunits[sunit].getratingsuperunit(days))
		return result

if __name__ == '__main__':
#	unit = Unit('735')
#	unit.addday(Day(date(2014, 4, 1), datetime(2014, 4, 1, 15, 0), datetime(2014, 4, 1, 17, 0)))
#	#dayy = Day(datetime(2014, 4, 1).date(), datetime(2014, 4, 1, 15, 0), datetime(2014, 4, 1, 17, 0))
#	unit.addday(Day(datetime(2014, 4, 2), datetime(2014, 4, 2, 15, 15), datetime(2014, 4, 2, 17, 0)))
#	unit.addpause(Pause(1, time(hour = 15, minute = 0), 30))
#	unit.addincident(Incident(datetime(2014,4,1,15,25), 30))
#	unit.addincident(Incident(datetime(2014,4,1,16,25), 5))
#	unit.setnorm(65)
#	print(unit)
#	print(unit.checkday(datetime(2014, 4, 1)))
#	print(unit.checkday(datetime(2014, 4, 2)))
#	print(unit.checkdays([date(2014, 4, 1), date(2014, 4, 2)]))
#	print(unit.getrating([date(2014, 4, 1), date(2014, 4, 2), date(2014, 4, 3)]))
#		
#	sunit = SuperUnit('5230')
#	
#	sunit.adddaytounit('736', Day(date(2014, 4, 1), datetime(2014, 4, 1, 15, 0), datetime(2014, 4, 1, 17, 0)))
#	sunit.adddaytounit('736', Day(datetime(2014, 4, 2), datetime(2014, 4, 2, 15, 15), datetime(2014, 4, 2, 17, 0)))
#	sunit.addpausetounit('736', Pause(1, time(hour = 15, minute = 0), 30))
#	sunit.addincidenttounit('736', Incident(datetime(2014,4,1,15,25), 30))
#	sunit.addincidenttounit('736', Incident(datetime(2014,4,1,16,25), 5))
#	sunit.setnormunit('736', 180)
#
#	sunit.adddaytounit('737', Day(date(2014, 4, 1), datetime(2014, 4, 1, 15, 0), datetime(2014, 4, 1, 17, 10)))
#	sunit.adddaytounit('737', Day(datetime(2014, 4, 2), datetime(2014, 4, 2, 15, 15), datetime(2014, 4, 2, 17, 0)))
#	sunit.addpausetounit('737', Pause(1, time(hour = 15, minute = 0), 30))
#	sunit.addincidenttounit('737', Incident(datetime(2014,4,1,15,25), 30))
#	sunit.addincidenttounit('737', Incident(datetime(2014,4,1,16,25), 5))
#	sunit.setnormunit('737', 80)
#	print(sunit)
#	print(sunit.checkdaysunit('736'))
#	print(sunit.getratingunits([date(2014, 4, 1), date(2014, 4, 2), date(2014, 4, 3)]))
#	print(sunit.getratingsuperunit([date(2014, 4, 1), date(2014, 4, 2), date(2014, 4, 3)]))
	mega = MegaUnit() 
	mega.adddaytounit('5230', '736', Day(date(2014, 4, 1), datetime(2014, 4, 1, 15, 0), datetime(2014, 4, 1, 17, 0)))
	mega.adddaytounit('5230', '736', Day(datetime(2014, 4, 2), datetime(2014, 4, 2, 15, 15), datetime(2014, 4, 2, 17, 0)))
	mega.addpausetounit('5230', '736', Pause(1, time(hour = 15, minute = 0), 30))
	mega.addincidenttounit('5230', '736', Incident(datetime(2014,4,1,15,25), 30))
	mega.addincidenttounit('5230', '736', Incident(datetime(2014,4,1,16,25), 5))
	mega.setnormunit('5230', '736', 180)

	mega.adddaytounit('5230', '737', Day(date(2014, 4, 1), datetime(2014, 4, 1, 15, 0), datetime(2014, 4, 1, 17, 10)))
	mega.adddaytounit('5230', '737', Day(datetime(2014, 4, 2), datetime(2014, 4, 2, 15, 15), datetime(2014, 4, 2, 17, 0)))
	mega.addpausetounit('5230', '737', Pause(1, time(hour = 15, minute = 0), 30))
	mega.addincidenttounit('5230', '737', Incident(datetime(2014,4,1,15,25), 30))
	mega.addincidenttounit('5230', '737', Incident(datetime(2014,4,1,16,25), 5))
	mega.setnormunit('5230', '737', 80)

	mega.adddaytounit('8643', '04', Day(date(2014, 4, 1), datetime(2014, 4, 1, 15, 0), datetime(2014, 4, 1, 17, 0)))
	mega.adddaytounit('8643', '04', Day(datetime(2014, 4, 2), datetime(2014, 4, 2, 15, 15), datetime(2014, 4, 2, 17, 0)))
	mega.addpausetounit('8643', '04', Pause(1, time(hour = 15, minute = 0), 30))
	mega.addincidenttounit('8643', '04', Incident(datetime(2014,4,1,15,25), 30))
	mega.addincidenttounit('8643', '04', Incident(datetime(2014,4,1,16,25), 5))
	mega.setnormunit('8643', '04', 180)

	mega.adddaytounit('8643', '05', Day(date(2014, 4, 1), datetime(2014, 4, 1, 15, 0), datetime(2014, 4, 1, 17, 10)))
	mega.adddaytounit('8643', '05', Day(datetime(2014, 4, 2), datetime(2014, 4, 2, 15, 15), datetime(2014, 4, 2, 17, 0)))
	mega.addpausetounit('8643', '05', Pause(1, time(hour = 15, minute = 0), 30))
	mega.addincidenttounit('8643', '05', Incident(datetime(2014,4,1,15,25), 30))
	mega.addincidenttounit('8643', '05', Incident(datetime(2014,4,1,16,25), 5))
	mega.setnormunit('8643', '05', 80)

	print(mega.getrating([date(2014, 4,1), date(2014, 4, 2), date(2014, 4, 3)]))
