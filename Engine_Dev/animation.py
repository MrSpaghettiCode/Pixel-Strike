class animation:
    def __init__(self, default_set,  frame_sets, delay):
        self.frame_sets = frame_sets
        self.current_frame_set = frame_sets[default_set]
        self.current_set_index = 0
        self.current_set_length = len(self.current_frame_set)
        self.delay = delay
        self.current_delay = 0

    def play(self):
        frame = self.get_current()
        
        if self.current_delay >= self.delay:
            self.current_delay = 0
            self.current_set_index += 1
            if self.current_set_index >= self.current_set_length:
                self.current_set_index = 0

            return frame

        self.current_delay += 1
        return frame

    def get_current(self):
        return self.current_frame_set[self.current_set_index]
    
    def use_set(self, set_name):
        self.current_frame_set = self.frame_sets[set_name]
        self.current_set_length = len(self.current_frame_set)