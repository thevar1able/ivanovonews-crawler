#!/usr/bin/env python3

import logging

logging.basicConfig(
    format='%(levelname)s:%(asctime)s:%(name)s:%(message)s',
    level=logging.INFO,
)

import schedule
import time
import pipeline


def main():
    pipeline.run()
    schedule.every(15).minutes.do(pipeline.run)
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
    main()
