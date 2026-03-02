from zut_calendar import api, config

def main():
    plan = api.get_plan()
    print(plan)

if __name__ == "__main__":
    main()
