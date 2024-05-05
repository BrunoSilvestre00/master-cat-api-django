import json
from learning.models import Question, Alternative, QuestionPool

def upload_questions_json(obj_file) -> int:
    data: dict = json.load(obj_file)
    key = next(iter(data.keys()))
    question_keys = ('statement', 'discrimination', 'difficulty', 'guess')
    
    questions_created = []
    for question in data[key]:
        obj = Question.objects.create(
            **{k: question[k] for k in question_keys}
        )
        Alternative.objects.bulk_create([Alternative(
            question=obj,
            text=question.get(a_key), 
            is_correct=question.get(f'{a_key}_is_correct', 0)
        ) for a_key in filter(
            lambda x: 'alternative_' in x and '_is_correct' not in x, 
            question.keys()
        )])
        questions_created.append(obj)
    
    pool = QuestionPool.create_pool(questions_created)
    return len(pool)
