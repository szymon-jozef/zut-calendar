from zut_calendar import api

def main():
    plan = api.get_plan()
    print(plan)

if __name__ == "__main__":
    main()
