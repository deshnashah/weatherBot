from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function

import logging
import warnings

from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.interpreter import RegexInterpreter
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter

logger = logging.getLogger(__name__)

warnings.filterwarnings("ignore")


def run_weather_online(input_channel, interpreter, domain_file='domain_weather.yml', training_data_file = 'data/stories.md') :
	#Create Agent
	agent = Agent(domain_file, policies = [KerasPolicy(), MemoizationPolicy()], interpreter=interpreter)
	
	#Train agent
	agent.train_online(
						training_data_file,
						max_history=2,
						batch_size=50,
						epochs=200,
						max_training_samples=300)
			
	return agent
	
if __name__ == '__main__' :
	logging.basicConfig(level='INFO')
	nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/weather_nlu')
	run_weather_online(ConsoleInputChannel(), nlu_interpreter)
