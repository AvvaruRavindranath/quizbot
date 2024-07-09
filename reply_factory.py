
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    """MY Tought : i assume that if any text is there the answer is True, and saved it to session else return False """
    if answer!=None:
        session[answer][current_question_id]=answer
        return True, ""

    return False, "Not a Valed answer"


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    dummyQuestion = PYTHON_QUESTION_LIST[current_question_id+1]
    QuestionId = current_question_id+1

    return dummyQuestion, QuestionId


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    totalQuestions = len(PYTHON_QUESTION_LIST)
    correctAnswers = len(session)

    return "You got {correctAnswers} Correct answers out of {totalQuestions}".format(totalQuestions,correctAnswers)



