from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter

def train_nlu(data, config, model_dir):
	# loading data
	training_data = load_data(data)
	# configuring trainer
	trainer = Trainer(RasaNLUConfig(config))
	#loading data in trainer
	trainer.train(training_data)
	#Intialisinf model, training it
	model_directory = trainer.persist(model_dir, fixed_model_name='weather_nlu')

def run_nlu():
	interpreter = Interpreter.load("./models/nlu/default/weather_nlu", RasaNLUConfig("config_spacy.json"))
	#print(interpreter.parse(u"I am planning my holiday to Barcelona. I wonder what is the weather out there"))
	print(interpreter.parse(u"I am planning my holiday to Barcelona from 15-03-2020. I wonder what is the weather out there"))


if __name__ == '__main__':
	#train_nlu("./data/data.json","config_spacy.json", "./models/nlu")
	run_nlu()

