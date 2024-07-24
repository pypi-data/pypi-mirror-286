def main() -> int:
    from tradingtoolbox.utils import time_manip

    print(time_manip.days_ago(3, to_timestamp=True))
    # print(time_manip.months_ago(3))

    # from tradingtoolbox.clickhouse import Clickhouse
    # print("Hello")
    # ch = Clickhouse()
    return 0
