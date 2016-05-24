
class GeoPoint:
	def __init__(self, latitude, longtitude):
		self.latitude = latitude #широта
		self.longtitude = longtitude #долгота

class SubFileHeader:
	__slots__ = "anameg", "apgrid", "alimit", "agscount", "astart", "childs", "parent"
	
	def __init__(self):
		self.childs = []

	def grid_contains_point(subFileHeader, geoPoint):
		return (geoPoint.latitude >= subFileHeader.alimit[0] and \
				geoPoint.latitude < subFileHeader.alimit[1] and \
				geoPoint.longtitude >= subFileHeader.alimit[2] and \
				geoPoint.longtitude < subFileHeader.alimit[3])

	#проверяем попадание точки в матрицу и определяем самую плотную дочернюю матрицу
	def find_grid(self, point):
		
		current_grid=self
		if grid_contains_point(self, point):
			return next((child.find_grid(current_grid, point) for child in current_grid.childs if child.find_grid(current_grid, point) != None), current_grid)
		else:
			return None

	def description(self):
		return(u'Название матрицы: {0}\n' +\
				u'Название базовой матрицы: {1}\n'+\
				u'Широта правого нижнего угла: {2}\n'+\
				u'Широта левого верхнего угла: {3}\n'+\
				u'Долгота правого нижнего угла: {4}\n'+\
				u'Долгота левого верхнего угла: {5}\n'+\
				u'Интервал матричной решетки по высоте: {6}\n'+\
				u'Интервал матричной решетки по долготе: {7}\n'+\
				u'Количество записей в матрице: {8}\n'+\
				u'Количество дочерних матриц: {9}').format(self.anameg, self.apgrid, self.alimit[0], self.alimit[1], self.alimit[2], self.alimit[3], self.alimit[4], self.alimit[5], self.agscount, len(self.childs))
