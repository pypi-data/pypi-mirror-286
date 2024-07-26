#!/usr/bin/python3

from emmi_escpi.application import Application
import sys, os

import logging
logger = logging.getLogger("escpi")

def main():

    app = Application(env=os.environ, args=sys.argv)
    app.setupIoc(env_prefix_map={ "ESCPI": None })
    app.runIoc()

if __name__ == "__main__":
    main()
