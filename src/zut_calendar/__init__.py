from zut_calendar import tui
import argparse

def main():
    parser = argparse.ArgumentParser(
            prog="Zut Calendar",
            description="Simple program for getting ZUT university class schedule",
            )

    parser.add_argument('-f', '--force-refresh', action='store_true', help="Force refreshing of the schedule")

    app = tui.ZutCalendarApp()
    app.run()

if __name__ == "__main__":
    main()
