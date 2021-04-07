class AppState:
    def __init__(self, max_state):
        self.current_state = -1
        self.state_list = []
        self.max_state = max_state

    def state_append(self, state):
        self.state_list.append(state)
        self.current_state += 1

    def save_state(self, state):
        if len(self.state_list) >= self.max_state:
            self.state_list.pop(0)
            self.current_state -= 1
        self.state_append(state)

    def undo(self):
        if self.current_state in [0, -1]:
            return None
        self.current_state -= 1
        return self.state_list[self.current_state]

    def redo(self):
        if self.current_state >= self.max_state - 1:
            return None
        self.current_state += 1
        return self.state_list[self.current_state]
