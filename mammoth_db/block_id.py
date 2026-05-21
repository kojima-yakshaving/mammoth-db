from dataclasses import dataclass

@dataclass
class BlockID:
    filename: str
    number: int

    def __str__(self):
        return "[file " + self.filename + ", block " + str(self.number) + "]";
