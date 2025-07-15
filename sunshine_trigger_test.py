
import argparse
import logging
import signal
import time

import sunshine_trigger


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("lattitude", type=float)
    parser.add_argument("longitude", type=float)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    sunshine_trigger = sunshine_trigger.SunshineTrigger(args.lattitude, args.longitude)

    signal.signal(signal.SIGTERM, sunshine_trigger.join)

    sunshine_trigger.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sunshine_trigger.join()
