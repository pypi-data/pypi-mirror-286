class Dataset:
    def __init__(self, dataset_name, data, description=None):
        self.name = dataset_name
        self.data = data
        self.description = description
    
    def to_json(self):
        return {
            "name": self.name,
            "data": self.data,
            "description": self.description
        }