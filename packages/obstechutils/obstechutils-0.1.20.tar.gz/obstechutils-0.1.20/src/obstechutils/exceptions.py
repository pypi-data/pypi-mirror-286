import sys
import logging

def logged_exit_excepthook(args, /):
    logger = logging.getLogger()
    logger.error(f"Error of type {args.exc_type} occurred")
    sys.exit(1)

def silent_exit_excepthook(args, /):
    sys.exit(1)
