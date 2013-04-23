#A controller for swarm behaviour in webots
import epuck_basic as epb
from robot import Robot
import math

class SwarmBot(epb.EpuckBasic):

	def __init__(self):
		
		epb.EpuckBasic.__init__(self)
		self.basic_setup()
		self.robot = Robot()


	def long_run(self):
		while True:
			proximities = [(x/4096) for x in self.get_proximities()] #There is NaN-bread
			lights = [(x/4096) for x in self.get_lights()]
			proximities = [0 if math.isnan(x) else x for x in proximities]
			lights = [0 if math.isnan(x) else x for x in lights]
			print proximities
			print lights
			#lights are out of order, (YOU'RE OUT OF ORDER!)
			lights_order = [4,5,6,7,0,1,2,3]
			lights = [lights[x] for x in lights_order]
			data = (proximities,lights)
			speed = self.robot.update(data)
			
			self.set_wheel_speeds(speed[0], speed[1])
			self.run_timestep()


controller = SwarmBot()
controller.long_run()