class State:
    def __init__(self, appRunner):
        self._state = {}
        self.appRunner = appRunner

    def __onStateUpdate(self):
        self.appRunner.scheduler.create_task(self.appRunner.on_state_update())

    def __getitem__(self, key):
        return self._state[key]

    def __setitem__(self, key, value):
        self._state[key] = value
        self.__onStateUpdate()

    def overwrite(self, new_state):
        self._state = new_state
        self.__onStateUpdate()

    def merge(self, new_state):
        self._state.update(new_state)
        self.__onStateUpdate()

    def __repr__(self):
        return repr(self._state)
