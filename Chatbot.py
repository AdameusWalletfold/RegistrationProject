import spacy
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


def main(message):
    nlp = spacy.load('en_core_web_sm')

    chatbot = ChatBot(name='Talon',
                      logic_adapters=['chatterbot.logic.BestMatch'])

    trainer = ChatterBotCorpusTrainer(chatbot)
    # Replace path with your own
    trainer.train('C:/Users/adkno/PycharmProjects/GroupProject/Lib/site-packages/chatterbot_corpus/data/custom/myown'
                  '.yml')

    response = chatbot.get_response(message)
    return response.text


