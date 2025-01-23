from pydantic import BaseModel


class Statistics(BaseModel):
    title: str
    count: int

    def to_dict(self):
        return {
            "title": self.title,
            "count": self.count,
        }
