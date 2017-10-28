# -*- coding: utf-8 -*-
import sys
import os
import json
import pprint
import time
from datetime import datetime, timedelta

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)


class APICallCounter:
    def __init__(self, client_tier=2):
        self.client_tier = client_tier
        self.api_calls_count = 0
        self.tier_decrease_count_rate = {
            2: 3,
            3: 2,
            4: 1
        }
        self.tier_max_counts = {
            2: 15,
            3: 20,
            4: 20
        }
        self.last_count_decreased = datetime.now()
        # self.start_counter()

    # def start_counter(self, time_limit=1000):
    #     count = 0
    #     while count < time_limit:
    #         time.sleep(self.tier_decrease_count_rate[self.client_tier])
    #         self.update_api_calls()

    def update_api_calls(self):
        dt = datetime.now() - self.last_count_decreased
        decrease = int(dt.total_seconds()) // self.tier_decrease_count_rate[self.client_tier]
        if decrease > 0:
            self.api_calls_count = max(0, self.api_calls_count - decrease)
            self.last_count_decreased = datetime.now()

    def add_call(self, count_increase=1):
        self.update_api_calls()
        if count_increase > 0:
            while self.api_calls_count >= self.tier_max_counts[self.client_tier]:
                print('Waiting for API call count to decrease...')
                time.sleep(1)
                self.update_api_calls()
            self.api_calls_count += count_increase
        return True

    def test_counter(self):
        count = 0
        while count < 50:
            if counter.add_call():
                count += 1
                print('%s \t Call %s placed - Current call count is: %s' % (datetime.now(), count, self.api_calls_count))


if __name__ == '__main__':
    counter = APICallCounter(client_tier=4)
    counter.test_counter()
