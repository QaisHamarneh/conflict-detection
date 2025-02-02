class Framerate():
    def __init__(self, data: list):
        self.data = data
        self.framerate_position = 0
        self.framerate = self._calculate_framerate(0)

    def _calculate_framerate(self, position: int):
        start_time = self.data[position][7]
        for index in range(position, len(self.data)):
            if self.data[index][7] != start_time:
                self.framerate_position = index
                return (index + 1) - position
            
        return len(self.data)

    def current_framerate(self, data_position: int) -> list:
        if data_position <= self.framerate_position:
            print(self.framerate)
            return self.framerate
        else:
            self.framerate = self._calculate_framerate(data_position)
            print(self.framerate)
            return self.framerate