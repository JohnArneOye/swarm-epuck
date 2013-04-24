import random
class Robot:

	def __init__(self):
		self.max_speed = 1.0
		self.weights = [[-1.0, -0.8],[-1.0, -0.8],[-0.4,  0.4],[ 0.0,  0.0],[ 0.0,  0.0],[ 0.4, -0.4],[-0.6, -0.8],[-0.6, -0.8]]
		self.offset = [0.5*self.max_speed, 0.5*self.max_speed]
		self.stagnation_threshold = 0.002
		self.retrieval_threshold = 0.3
		self.retrieval_light_threshold = 0.08

		self.recovering = False
		self.counter = 0
		self.last_data = None


	def update(self, data):
		# use stagnation, retrieval, or search behaviour
		
		if self.use_stagnation(data):
			return self.stagnation(data)
		if self.use_retrieval(data):
			return self.retrieval(data)
		
		return self.search(data)
			
		
	def use_stagnation(self, data):
		if self.recovering: return True
		if self.last_data:
			if ( abs(self.last_data[0][0] - data[0][0]) < self.stagnation_threshold 
			or abs(self.last_data[1][0] - data[1][0]) < self.stagnation_threshold
			or self.last_data == data ):
				self.counter += 1
				if self.counter > 200:
					self.counter = 0
					self.recovering = True
					return True
		self.last_data = data
		return False
		
	def use_retrieval(self, data):
		for prox in data[0]:
			light_is_near = False
			for light in data[1]:
				if light > self.retrieval_light_threshold:
					light_is_near = True
			if prox > self.retrieval_threshold and light_is_near:
				return True
		return False
		
	#Method defining the retrieval behaviour
	def retrieval(self, data):
		print "retrieving"
		if (data[0][0] > self.retrieval_threshold and data[0][7] > self.retrieval_threshold):
			return [self.max_speed, self.max_speed]
		else:
			sensors_left = sum(data[0][4:])
			sensors_right = sum(data[0][:4])
			if (sensors_left - sensors_right) < 0:
				return [self.max_speed * 0.7, self.max_speed * -0.3]
			else:
				return [self.max_speed * -0.3, self.max_speed * 0.7]
		
	#Method defining the stagnation behaviour
	def stagnation(self, data):
		print "stagnating"
		lw,rw = 0,0
		rw = -self.max_speed
		lw = -self.max_speed
		if self.counter > 50:
			lw = 0
		if self.counter > 100:
			self.counter = 0
			self.recovering = False
			
		self.counter += 1
		return (lw,rw)
		
	#Method defining the search behaviour
	def search(self, data):
		print "searching"
		# proximity sensors
		sensors_left = sum(data[1][:4])
		sensors_right = sum(data[1][4:])

		sensors_back = data[1][0] + data[1][7]

		diff = sensors_right - sensors_left
		#left_speed = self.minmax((sensors_left + (sensors_right - sensors_left) * random.random()), -self.max_speed, self.max_speed)
		#right_speed = self.minmax((sensors_right + (sensors_left - sensors_right) * random.random()), -self.max_speed, self.max_speed)
		if diff < 0:
			left_speed = self.max_speed
			right_speed = self.max_speed * (1 + diff*2)
		else:
			left_speed = self.max_speed * (1 - diff*2)
			right_speed = self.max_speed
		if sensors_back < data[1][3] + data[1][4]:
			left_speed = self.max_speed
			right_speed = -self.max_speed

		return [left_speed, right_speed]