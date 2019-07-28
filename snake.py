from segment import Segment


class Snake:
	def __init__(self, x, y, seg_size, color, speed):
		self.seg_size = seg_size
		self.color = color
		self.head = Segment(x, y, self.seg_size, self.color)
		self.tail = []
		self.speed = speed
		self.maximum_tail_size = 70

		starting_tail_size = 4

		for i in range(starting_tail_size):
			seg = Segment(x, y, self.seg_size, self.color)
			self.tail.append(seg)

	def render(self):
		for i in range(len(self.tail)):
			self.tail[len(self.tail)-1-i].render()

		self.head.render()

	def update(self):
		if len(self.tail) > self.maximum_tail_size:
			self.tail.pop()

		for i in range(len(self.tail)):
			self.tail[i].color = (255 - i * (255 / len(self.tail)), 0, 0)

		self.head.update()

		for seg in self.tail:
			seg.update()
