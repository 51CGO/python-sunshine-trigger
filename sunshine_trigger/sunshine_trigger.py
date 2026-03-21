import logging
import datetime
import time
import threading

import suntimes


class SunshineTrigger(threading.Thread):

    def __init__(self, lattitude, longitude, test_duration=0):

        threading.Thread.__init__(self)

        self.logger = logging.getLogger("SunshineTrigger")

        self.do_run = True
        self.test_duration = test_duration

    def run(self):

        self.logger.debug("run")

        if self.test_duration:

            dt_now = datetime.datetime.now(datetime.timezone.utc)
            dt_next = dt_now + datetime.timedelta(seconds=self.test_duration)
            sun_is_shining = True

            while self.do_run:

                dt_now = datetime.datetime.now(datetime.timezone.utc)

                if dt_now > dt_next:

                    if sun_is_shining:
                        self.on_sunset()
                    else:
                        self.on_sunrise()

                    sun_is_shining = not sun_is_shining

                    dt_next = dt_now + datetime.timedelta(seconds=self.test_duration)

                else:
                    time.sleep(1)

            return

        self.calendar = suntimes.SunTimes(longitude, lattitude)

        dt_now = datetime.datetime.now(datetime.timezone.utc)
        self.logger.debug("Now : %s" % dt_now)


        next_sunrise = self.calendar.riseutc(dt_now.date()).replace(
            tzinfo=datetime.timezone.utc)
        self.logger.debug("Sunrise : %s" % next_sunrise)

        next_sunset = self.calendar.setutc(dt_now.date()).replace(
            tzinfo=datetime.timezone.utc)
        self.logger.debug("Sunset : %s" % next_sunset)

        if dt_now > next_sunrise and dt_now < next_sunset:
            sun_is_shining = True
            self.logger.debug("Day")
        else:
            sun_is_shining = False
            self.logger.debug("Night")

        while self.do_run:

            dt_now = datetime.datetime.now(datetime.timezone.utc)

            if sun_is_shining:

                if dt_now > next_sunset:
                    self.logger.debug("Night has fallen")
                    sun_is_shining = False
                    next_sunrise = self.calendar.riseutc(
                        dt_now.date() + datetime.timedelta(days=1)
                    ).replace(tzinfo=datetime.timezone.utc)
                    self.logger.debug("Next sunrise : %s" % next_sunrise)
                    self.on_sunset()

            else:

                if dt_now > next_sunrise:
                    self.logger.debug("Day has raised")
                    sun_is_shining = True
                    next_sunset = self.calendar.setutc(
                        dt_now.date()
                    ).replace(tzinfo=datetime.timezone.utc)
                    self.logger.debug("Next sunset : %s" % next_sunset)
                    self.on_sunrise()

            time.sleep(1)

    def on_sunrise(self):
        self.logger.debug("on_sunrise")

    def on_sunset(self):
        self.logger.debug("on_sunset")

    def join(self):
        self.logger.debug("join")
        self.do_run = False
        threading.Thread.join(self)
