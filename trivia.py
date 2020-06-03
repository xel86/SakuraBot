#Trivia Questions for $trivia game sorted by Genre
#questions are [genre, question, answer]

def generate_questions():

    question_master = []
    geography_questions = []
    game_questions = []
    twitch_questions = []
    question_master.append(["Geography", "What is the capital of Switzerland?", "Bern"])
    question_master.append(["Games", "How much is a flashbang in CS:GO?", "$200"])
    question_master.append(["Twitch", "Reckful, and the one who got away", "Natalie"])
    question_master.append(["Twitch", "Reckful spent how much on Blues car?", "30k"])
    question_master.append(["Twitch", "What year was the Reckful & Forsen Spain Trip?", "2017"])
    question_master.append(["History", "How many US Presidents have been assassinated during office?", "4"])
    question_master.append(["Guess Who", "Final Offer, thats the best I can do", "Rick Harrison"])

    questions_genre = [geography_questions, game_questions, twitch_questions]
    for question in question_master:
        if(question[0].lower() == "geography"):
            geography_questions.append(question)
        
        elif(question[0].lower() == "games"):
            game_questions.append(question)
        
        elif(question[0].lower() == "twitch"):
            twitch_questions.append(question)

        elif(question[0].lower() == "history"):
            twitch_questions.append(question)

        elif(question[0].lower() == "guess who"):
            twitch_questions.append(question)
    return question_master, questions_genre 
