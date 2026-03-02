import requests

student_id = 60035
begining_week = "2026-03-02T00%3A00%3A00%2B01%3A00"
end_week = "2026-03-09T00%3A00%3A00%2B01%3A00"
url = f"https://plan.zut.edu.pl/schedule_student.php?number={student_id}&start={begining_week}&end={end_week}"

result = requests.get(url)

if __name__ == "__main__":
    try:
        result.raise_for_status
        print(result.text)
        
    except Exception as e:
        print(f"Error: {e}")
