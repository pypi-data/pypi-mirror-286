import sys
import time
from dekdjtools.management.base import CommandBasic
from dekdjseed.core import create_project_entities


class Command(CommandBasic):
    help = 'Generate fake data'

    def handle(self, seed: int = 0):
        time_begin = time.time()
        create_project_entities(seed or None)
        sys.stdout.write(f'Total cost: {time.time() - time_begin}s\n')
