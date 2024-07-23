from typing import Optional
from flask import Flask
from gunicorn.app.base import BaseApplication


class GunicornApplication(BaseApplication):
    """
    This class is a small helper to wrap flask apps and launch
    a gunicorn server application
    """

    def __init__(self, app: Flask, options: Optional[dict] = None):
        """
        Arguments:
            app: Flask
                Your flask app.
            options: dict or None
                Options for your gunicorn app
                https://docs.gunicorn.org/en/stable/configure.html#framework-settings

        """
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        if self.cfg is not None:
            config = {key: value for key, value in self.options.items()
                      if key in self.cfg.settings and value is not None}

            for key, value in config.items():
                self.cfg.set(key.lower(), value)

    def load(self):
        return self.application
