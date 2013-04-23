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
		elif self.use_retrieval(data):
			return self.retrieval(data)
		else:
			return self.search(data)
			
		
	def use_stagnation(self, data):
		return False
		
	def use_retrieval(self, data):
		return False
		
	#Method defining the retrieval behaviour
	def retrieval(self, data):
		pass
		
	#Method defining the stagnation behaviour
	def stagnation(self, data):
		pass
		
	#Method defining the seach behaviour
	def search(self, data):
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