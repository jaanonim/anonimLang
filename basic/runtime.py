class RuntimeResult:
    def __init__(self):
        self.reset()

    def reset(self):
        self.error = None
        self.value = None
        self.return_value = None
        self._continue = False
        self._break = False

    def register(self, res):
        self.error = res.error
        self.return_value = res.return_value
        self._break = res._break
        self._continue = res._continue
        return res.value

    def success(self, value):
        self.reset()
        self.value = value
        return self

    def success_return(self, value):
        self.reset()
        self.return_value = value
        return self

    def success_continue(self):
        self.reset()
        self._continue = True
        return self

    def success_break(self):
        self.reset()
        self._break = True
        return self

    def failure(self, error):
        self.reset()
        self.error = error
        return self

    def should_return(self):
        return self._continue or self._break or self.error or self.return_value
