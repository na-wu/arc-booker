import datetime
import time
import pytz

class IEB:
  def __init__(self, end):
    self.tz = pytz.timezone("Canada/Pacific")
    self.min_backoff = 2
    self.factor = 0.5
    self.end = end
    self.next_delay = 200
    self.retries = 10

  def transform_time(self, time_obj):
    return datetime.datetime.combine(datetime.datetime.today(), time_obj)

  def next(self):
    if self.retries == 0:
      print("Maximum number of retries reached, exiting.")
      exit()
    new_ieb_time = (self.transform_time(self.end) - self.transform_time(datetime.datetime.now(tz=self.tz).time())).total_seconds()
    self.next_delay = max(min(new_ieb_time * self.factor, self.next_delay), self.min_backoff)
    if self.next_delay == 2:
      self.retries -= 1
    time.sleep(self.next_delay)
    


      