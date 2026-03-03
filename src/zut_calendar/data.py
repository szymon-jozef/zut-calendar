class ClassEntry:
    def __init__(self, data):
        self.title = data.get("title")
        self.description = data.get("description")
        self.start = data.get("start")
        self.end = data.get("end")
        self.worker = data.get("worker")

    def __str__(self) -> str:
        return f"""
        Title = {self.title}
        Description = {self.description}
        Start = {self.start}
        End = {self.end}
        Worker = {self.worker}
        """

class ClassList:
    def __init__(self, json) -> None:
        self.list = []
        for item in json[1:]:
            if isinstance(item, dict):
                self.list.append(ClassEntry(item))

    def __str__(self) -> str:
        string = ""
        for element in self.list:
            string += str(element)

        return string
