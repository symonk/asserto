class StringMixin:
    def endswith(self, suffix: str) -> None:
        if not self.value.endswith(suffix):
            self._failed(f"String: {self.value} did not end with: {suffix}")

    def startswith(self, prefix: str) -> None:
        if not self.value.startswith(prefix):
            self._failed(f"String: {self.value} did not start with: {prefix}")
