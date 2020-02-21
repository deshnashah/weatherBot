from rasa_core.channels import HttpInputChannel
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_slack_connector import SlackInput


nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/weather_nlu')

agent = Agent.load('./models/dialogue', interpreter = nlu_interpreter)

inputChannel = SlackInput('xoxp-935750121813-937940392534-935832465845-c6882214c09ba4a5df94d22b62d3f0e2','xoxb-935750121813-925590510417-62Et1blmVnQMghPas6fAwv4V','oi0tvy686jcj44BRxYeYbjb8', True)

agent.handle_channel(HttpInputChannel(5004, '/', inputChannel))
