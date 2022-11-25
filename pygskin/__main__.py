import sys
from pygskin import sleeper

# weather.process_csv(sys.stdin, sys.stdout)
sleeper.process_stream(sys.stdin, sys.stdout)
