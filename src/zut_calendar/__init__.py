from zut_calendar import api, data
import argparse

def main():
    parser = argparse.ArgumentParser(
            prog="Zut Calendar",
            description="Simple program for getting ZUT university class schedule",
            )

    parser.add_argument('-f', '--force-refresh', action='store_true', help="Force refreshing of the schedule")
    args = parser.parse_args()

    plan = api.get_plan(args.force_refresh)
    ce = data.ClassList(plan)
    print(ce)

if __name__ == "__main__":
    main()
