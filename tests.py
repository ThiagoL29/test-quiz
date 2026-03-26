import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_correct_choice():
    question = Question(title='q1')
    question.add_choice('a', True)

    choice = question.choices[0]

    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert choice.is_correct

def test_create_multiple_choices():
    question = Question(title='q1')

    question.add_choice('a', False)
    question.add_choice('b', True)

    assert len(question.choices) == 2
    assert question.choices[0].text == 'a'
    assert not question.choices[0].is_correct
    assert question.choices[1].text == 'b'
    assert question.choices[1].is_correct

def test_create_choice_with_invalid_text():
    with pytest.raises(Exception, match='Text cannot be empty'):
        Question(title='q1').add_choice('', False)
    with pytest.raises(Exception, match='Text cannot be longer than 100 characters'):
        Question(title='q1').add_choice('a'*101, False)

def test_remove_choice_with_valid_id():
    question = Question(title='q1')

    choice = question.add_choice('a', False)
    question.remove_choice_by_id(choice.id)

    assert len(question.choices) == 0

def test_remove_choice_with_invalid_id():
    with pytest.raises(Exception, match='Invalid choice id 1'):
        Question(title='q1').remove_choice_by_id(1)

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)
    question.remove_all_choices()

    assert len(question.choices) == 0

def test_set_correct_choices_with_valid_ids():
    question = Question(title='q1')
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', False)

    question.set_correct_choices([choice1.id, choice2.id])

    assert choice1.is_correct
    assert choice2.is_correct

def test_set_correct_choices_with_invalid_ids():
    with pytest.raises(Exception, match='Invalid choice id 1'):
        Question(title='q1').set_correct_choices([1, 2])

def test_correct_selected_choices_with_correct_choices():
    question = Question(title='q1')
    choice1 = question.add_choice('a', True)

    correct_choices = question.correct_selected_choices([choice1.id])

    assert len(correct_choices) == 1
    assert correct_choices[0] == choice1.id

def test_correct_selected_choices_with_incorrect_choices():
    question = Question(title='q1')
    choice1 = question.add_choice('a', False)

    correct_choices = question.correct_selected_choices([choice1.id])

    assert len(correct_choices) == 0

def test_correct_selected_choices_with_more_choices_than_selections():
    question = Question(title='q1', max_selections=1)
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', False)

    with pytest.raises(Exception, match='Cannot select more than 1 choices'):
        question.correct_selected_choices([choice1.id, choice2.id])

@pytest.fixture
def question_with_multiple_choices():
    question = Question(title='q1', max_selections=2)
    question.add_choice('a', True)
    question.add_choice('b', True)
    question.add_choice('c', False)
    return question

def test_correct_selected_choices_with_multiple_correct_choices(question_with_multiple_choices):
    correct_choices = question_with_multiple_choices.correct_selected_choices([1, 2])

    assert len(correct_choices) == 2
    assert 1 in correct_choices
    assert 2 in correct_choices

def test_add_incorrect_choice(question_with_multiple_choices):
    question_with_multiple_choices.add_choice('d', False)

    assert len(question_with_multiple_choices.choices) == 4
    assert question_with_multiple_choices.choices[3].text == 'd'
    assert not question_with_multiple_choices.choices[3].is_correct