class Context:
    def __init__(self):
        self.data = {}


class State:
    def __init__(self):
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
        print(f"{self.__class__.__name__} is an end state. No further transitions.")


class Chain:
    def __init__(self):
        self.states = {}
        self.current_state = None
        self.context = Context()
        print("This is the context data:", self.context.data)

    def add_state(self, state_class):
        state_instance = state_class()
        state_instance.set_context(self.context)
        self.states[state_class] = state_instance

    def set_initial_state(self, state_class):
        self.current_state = self.states.get(state_class)
        if self.current_state:
            self.current_state.on_enter()
        else:
            print(f"State {state_class} not found.")

    def next(self):
        if self.current_state:
            self.current_state.action()
            if isinstance(self.current_state, EndState):
                print("Reached an end state. No further transitions.")
                return False
            next_state_class = self.current_state.next_state()
            if next_state_class in self.states:
                self.current_state = self.states[next_state_class]
                self.current_state.on_enter()
                return True
            else:
                print(f"Transition to state {next_state_class} not possible.")
                return False
        else:
            print("No current state set.")
            return False

    def run(self):
        while self.next():
            pass
