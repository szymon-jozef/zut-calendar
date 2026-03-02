import requests
import json

student_id = 60035
begining_week = "2026-03-02T00%3A00%3A00%2B01%3A00"
end_week = "2026-03-09T00%3A00%3A00%2B01%3A00"
url = f"https://plan.zut.edu.pl/schedule_student.php?number={student_id}&start={begining_week}&end={end_week}"

result = requests.get(url)

class ClassEntry:
    def __new__(self) -> Self:
        self.title
        self.start
        self.end
        self.worker
        self.group_name
        self.room
        self.hours
        pass

def test():
    try:
        result.raise_for_status

        for q in json.loads(result.text)[1]:
            print(q)
        
    except Exception as e:
        print(f"Error: {e}")
