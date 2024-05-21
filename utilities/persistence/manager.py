import os

class PersistenceManager:
    def __init__(self, file_path: str):
        self.file_path = file_path

        if os.path.isdir(self.file_path):
            raise ValueError("Valor do caminho deve ser um arquivo!")

        if not os.path.exists(self.file_path):
            open(self.file_path, 'w').close()

        with open(file_path, 'r', encoding="utf-8") as f:
            self._content: list[str] = list(filter(bool, map(lambda x: x.strip(), f.readlines())))

    @property
    def content(self) -> list[str]:
        return self._content
        
    @content.setter
    def content(self, value: list[str]):
        self._content = value

    def append(self, new_value: str):
        self._content.append(new_value)

        return len(self._content) - 1
    
    def remove(self, index: int):
        self._content.pop(index)

    def commit(self):
        with open(self.file_path, 'w') as f:
            f.write('\n'.join(self.content))

    def __contains__(self, item: str):
        return item in self._content
    
    def __bool__(self):
        return bool(self._content)
    

