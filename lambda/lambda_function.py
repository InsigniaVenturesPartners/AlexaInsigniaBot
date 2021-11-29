import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response
from ask_sdk_model.interfaces.alexa.presentation.apl import (RenderDocumentDirective, ExecuteCommandsDirective)

from utils import *
from built_in_handlers import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CURRENT_STATE = "IDLE"
DATA = load_json_from_path("data.json")

def playlist():
    return [
        {
            "url": create_presigned_url("Media/INSIGNIA_VC_VIDEO.mp4"),
            "title": "Insignia Video",
            "subtitle": ""
        }    
    ]

def get_coinvestor(coinvestor):
    global DATA
    return DATA["COMPANIES"].get(coinvestor.upper())

def get_video_directive():
    video_directive = RenderDocumentDirective(
        token = "VideoPlayer",
        document = load_json_from_path("apl/render-videoplayer.json"),
        datasources = create_all_video_playlist(playlist())
    )
    return video_directive

class LaunchRequestHandler(AbstractRequestHandler):
    #Handler for Skill Launch
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        return (
            handler_input.response_builder
                .speak(DATA["INTRO"])
                .response
        )

class IntroductionIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("IntroductionIntent")(handler_input)

    def handle(self, handler_input):
        global CURRENT_STATE
        CURRENT_STATE = "PROMPTING_VIDEO"
        speech_output = DATA["COMPANYINTRO"] + " Would you like to watch a video from Insignia Ventures Partners?"
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(speech_output)
                .response
        )

class FounderInfoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("FounderInfoIntent")(handler_input)

    def handle(self, handler_input):
        speech_output = DATA["FOUNDER"]
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(speech_output)
                .response
        )

class InvestorCEOIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("InvestorCEOIntent")(handler_input)
    
    def handle(self, handler_input):
        coinvestor = handler_input.request_envelope.request.intent.slots["coinvestor"].value
        data = get_coinvestor(coinvestor)
        speech_output = ""
        if data:
            speech_output = "The CEO of " + coinvestor + " is " + data["CEO"] + "."
        else:
            speech_output = "Sorry, the coinvestor " + coinvestor + " could not be found."
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .response
        )

class InvestorFoundersIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("InvestorFoundersIntent")(handler_input)
    
    def handle(self, handler_input):
        coinvestor = handler_input.request_envelope.request.intent.slots["coinvestor"].value
        data = get_coinvestor(coinvestor)
        speech_output = ""
        if data:
            founders = data["FOUNDER"]
            if len(founders) > 1:
                speech_output = "The Founders of " + coinvestor + " are "
                for i in range(len(founders) - 1):
                    speech_output += founders[i]
                    speech_output += ", "
                speech_output += " and " + founders[len(founders) - 1] + "."
            else:
                speech_output = "The Founder of " + coinvestor +  " is " + founders[0] + "."
        else:
            speech_output = "Sorry, the coinvestor " + coinvestor + " could not be found."
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .response
        )

class InvestorInfoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("InvestorInfoIntent")(handler_input)
    
    def handle(self, handler_input):
        coinvestor = handler_input.request_envelope.request.intent.slots["coinvestor"].value
        data = get_coinvestor(coinvestor)
        if data:
            speech_output = data["INFO"]
        else:
            speech_output = "Sorry, the coinvestor " + coinvestor + " could not be found."
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .response
        )

class VideoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("VideoIntent")(handler_input)
    
    def handle(self, handler_input):
        video_directive = get_video_directive()
        return (
            handler_input.response_builder
                .speak("Here is a video for more information on Insignia Ventures Partners")
                .add_directive(video_directive)
                .response
        )

class NewsIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("NewsIntent")(handler_input)
    
    def handle(self, handler_input):

class YesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        global CURRENT_STATE
        if CURRENT_STATE == "PROMPTING_VIDEO":
            video_directive = get_video_directive()
            CURRENT_STATE = "IDLE"
            return (
                handler_input.response_builder
                    .speak("Here is a video for more information on Insignia Ventures Partners")
                    .add_directive(video_directive)
                    .response
            )
        else:
            CURRENT_STATE = "IDLE"
            return (
                handler_input.response_builder
                    .speak("")
                    .response
            )
        
class NoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        global CURRENT_STATE
        speak_output = ""
        if CURRENT_STATE == "PROMPTING_VIDEO":
            speak_output = "Okay, that's alright"
        CURRENT_STATE = "IDLE"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class PlayIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.ResumeIntent")(handler_input)
    
    def handle(self, handler_input):
        video_directive = ExecuteCommandsDirective(
                            token = "VideoPlayer",
                            commands = [
                                {
                                    "type": "ControlMedia",
                                    "componentId": "VideoPlayer",
                                    "command": "play"
                                },
                                {
                                    "type": "showOverlayShortly"
                                }
                            ]
                            )
        return (
            handler_input.response_builder
                .speak("")
                .add_directive(video_directive)
                .response
            )

class PauseIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.PauseIntent")(handler_input)
    
    def handle(self, handler_input):
        video_directive = ExecuteCommandsDirective(
                            token = "VideoPlayer",
                            commands = [
                                {
                                    "type": "ControlMedia",
                                    "componentId": "VideoPlayer",
                                    "command": "pause"
                                }
                            ]
                            )
        return (
            handler_input.response_builder
                .speak("")
                .add_directive(video_directive)
                .response
            )



# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.

sb = SkillBuilder()


sb.add_request_handler(LaunchRequestHandler())

sb.add_request_handler(IntroductionIntentHandler())
sb.add_request_handler(FounderInfoIntentHandler())
sb.add_request_handler(InvestorInfoIntentHandler())
sb.add_request_handler(InvestorCEOIntentHandler())
sb.add_request_handler(InvestorFoundersIntentHandler())
sb.add_request_handler(VideoIntentHandler())

sb.add_request_handler(PlayIntentHandler())
sb.add_request_handler(PauseIntentHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NoIntentHandler())

#Built In Intents
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler())


sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()