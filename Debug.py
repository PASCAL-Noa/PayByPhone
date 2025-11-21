import datetime

class Debug:

    COLORS = {
        "RESET":    "\033[0m",
        "INFO":     "\033[36m",
        "DEBUG":    "\033[35m",
        "WARNING":  "\033[33m",
        "ERROR":    "\033[31m",
        "SUCCESS":  "\033[32m",
    }

    def __init__(self, debug=False, use_colors=True, prefix="", silent=False):
        self.debug_enabled = debug
        self.use_colors = use_colors
        self.prefix = prefix
        self.silent = silent

    def _log(self, level, message):
        if self.silent:
            return

        if level == "DEBUG" and not self.debug_enabled:
            return

        is_error_level = (level == "ERROR" or level == "CRITICAL")
        if not self.debug_enabled and not is_error_level:
            return

        tag = f"[{level}]"
        if self.use_colors and level in self.COLORS:
            tag = f"{self.COLORS[level]}{tag}{self.COLORS['RESET']}"

        prefix = f"{self.prefix} " if self.prefix else ""
        print(f"{tag} {prefix}{message}")


    def info(self, msg):       self._log("INFO", msg)
    def debug(self, msg):      self._log("DEBUG", msg)
    def warning(self, msg):    self._log("WARNING", msg)
    def error(self, msg):      self._log("ERROR", msg)
    def success(self, msg):    self._log("SUCCESS", msg)
    def critical(self, msg):   self._log("ERROR", f"[CRITICAL] {msg}")