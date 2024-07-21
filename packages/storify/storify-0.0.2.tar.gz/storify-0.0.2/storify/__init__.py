import os
import time
import copy

from .dummylogger import DummyLogger
from .database import Database

class Storify:
    def __init__(self, root="data", save_interval=60, log=DummyLogger(), models=[]):
        """
        Initialize the Storify instance.

        Parameters:
        - root (str): The root directory where databases will be stored. Default is "data".
        - save_interval (int): The interval in seconds for automatic saving of databases. Default is 60 seconds.
        - log (DummyLogger): Logger instance for logging messages. Default is an instance of DummyLogger.
        - models (list): A list of model classes to be used with the Storify instance. Default is an empty list.
        """
        self.root = root
        self.save_interval = save_interval
        self.log = log
        self.models = models

        self.databases = []

        if not os.path.exists(self.root):
            os.mkdir(self.root)

        if not os.path.exists(os.path.join(self.root, ".backups")):
            os.mkdir(os.path.join(self.root, ".backups"))
            
    def get_db(self,
               name,
               root={}):

        _root = copy.deepcopy(root)

        db = Database(name, self.root, self.log, rootdata=_root, models=self.models)
        self.databases.append(db)

        return db

    def db_exists(self, name):
        return os.path.exists(
            os.path.join(self.root, name + ".mpack")
        )

    def rename_db(self, old_name, new_name):
        """ WARNING: Dangerous to use if a DB is open! """
        # TODO: Make this safer

        old_path = os.path.join(self.root, old_name + ".mpack")
        new_path = os.path.join(self.root, new_name + ".mpack")

        os.rename(old_path, new_path)

    def remove_db(self, name):
        """ WARNING: Likely ineffective if a DB is open! """
        # TODO: Make this safer
        # TODO: Remove backups
        path = os.path.join(self.root, name + ".mpack")

        os.remove(path)

    def tick(self, force=False):
        # Filter out defunct databases
        active_dbs = [db for db in self.databases if not db.defunct]

        for db in active_dbs:
            if force:
                db.flush()
            else:
                # Saves on a regular interval based off of self.save_interval
                if time.time() - db.last_flush > self.save_interval:
                    db.flush()

    def flush(self):
        self.tick(force=True)

    def __getitem__(self, name):
        """Access a database by name using get_db."""
        return self.get_db(name)

    def __delitem__(self, name):
        """Remove a database by name using remove_db."""
        self.remove_db(name)