class Context:
    def __init__(self):
        self.data = {}


class State:
    def __init__(self, name):
        self.name = name
        self.context = None

    def set_context(self, context):
        self.context = context

    def on_enter(self):
        pass

    def action(self):
        pass

    def next_state(self):
        return None


class EndState(State):
    def action(self):
        print(f"{self.name} is an end state. No further transitions.")

    def next_state(self):
        return None


class ChainState:
    def __init__(self):
        self.states = {}
        self.current_state = None
        self.context = Context()

    def add_state(self, state):
        state.set_context(self.context)
        self.states[state.name] = state

    def set_initial_state(self, state_name):
        self.current_state = self.states.get(state_name)
        if self.current_state:
            self.current_state.on_enter()
        else:
            print(f"State {state_name} not found.")

    def next(self):
        if self.current_state:
            self.current_state.action()
            if isinstance(self.current_state, EndState):
                print("Reached an end state. No further transitions.")
                return False
            next_state_name = self.current_state.next_state()
            if next_state_name in self.states:
                self.current_state = self.states[next_state_name]
                self.current_state.on_enter()
                return True
            else:
                print(f"Transition to state {next_state_name} not possible.")
                return False
        else:
            print("No current state set.")
            return False

    def run(self):
        while self.next():
            pass
