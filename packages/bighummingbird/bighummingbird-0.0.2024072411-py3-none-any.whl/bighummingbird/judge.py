class Judge:
    def __init__(self, name, description, scoring_rubric, passing_criteria=None):
        self.name = name
        self.description = description
        self.scoring_rubric = scoring_rubric
        self.passing_criteria = passing_criteria

    def to_json(self):
        return {
            'name': self.name,
            'description': self.description,
        }