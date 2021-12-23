import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response
from ask_sdk_model.interfaces.alexa.presentation.apl import (RenderDocumentDirective, ExecuteCommandsDirective)
from ask_sdk_core.utils import get_supported_interfaces

from utils import *
from news import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#test

PROMPTING_VIDEO_COMPANY = ""
CURRENT_STATE = "IDLE"
READ_NEWS = 0
DATA = load_json_from_path("data.json")

def get_company(company):
    global DATA
    return DATA["COMPANIES"].get(company.upper())

def get_person(name):
    global DATA
    return DATA["PEOPLE"].get(name)

def get_video_directive(company_name):
    video_directive = RenderDocumentDirective(
        token = "VideoPlayer",
        document = load_json_from_path("apl/videoplayer.json"),
        datasources = {
            "videoPlayerData": {
                "properties" : {
                    "url" : create_presigned_url("Media/" + company_name.upper() + ".mov")
                }
            }
        }
    )

    return video_directive

class LaunchRequestHandler(AbstractRequestHandler):
    #Handler for Skill Launch
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        return (
            handler_input.response_builder
                .speak(DATA["INTRO"] + "i am cool")
                .ask(DATA["INTRO"])
                .response
        )

class InsigniaNewsIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("InsigniaNewsIntent")(handler_input)

    def handle(self, handler_input):
        global READ_NEWS
        global CURRENT_STATE
        READ_NEWS = 0
        response_builder = handler_input.response_builder
        speak_output = get_insignia_news()[READ_NEWS]["title"]
        READ_NEWS += 1
        speak_output += ". Would you like more news?"
        CURRENT_STATE = "PROMPTING_NEWS"
        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )

class NewsIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("NewsIntent")(handler_input)

    def handle(self, handler_input):
        response_builder = handler_input.response_builder
        speak_output = get_other_news()[0]["title"]
        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )

class CompanyCEOIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("CompanyCEOIntent")(handler_input)

    def handle(self, handler_input):
        company = handler_input.request_envelope.request.intent.slots["company"].value
        data = None
        if company:
            data = get_company(company.split()[0])
        speak_output = ""
        if data:
            speak_output = "The CEO of " + company + " is " + data["CEO"] + "."
        else:
            speak_output = "Sorry, the company could not be found."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class CompanyFounderIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("CompanyFounderIntent")(handler_input)

    def handle(self, handler_input):
        company = handler_input.request_envelope.request.intent.slots["company"].value
        data = None
        if company:
            data = get_company(company.split()[0])
        speak_output = ""
        if data:
            founders = data["FOUNDER"]
            if len(founders) > 1:
                speak_output = "The Founders of " + company + " are "
                for i in range(len(founders) - 1):
                    speak_output += founders[i]
                    speak_output += ", "
                speak_output += " and " + founders[len(founders) - 1] + "."
            else:
                speak_output = "The Founder of " + company +  " is " + founders[0] + "."
        else:
            speak_output = "Sorry, the company could not be found."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class CompanyInfoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("CompanyInfoIntent")(handler_input)

    def handle(self, handler_input):
        company = handler_input.request_envelope.request.intent.slots["company"].value
        data = None
        if company:
            data = get_company(company.split()[0])
        if data:
            speak_output = data["INFO"]
            if data["VIDEO"] == True:
                global CURRENT_STATE
                global PROMPTING_VIDEO_COMPANY
                CURRENT_STATE = "PROMPTING_VIDEO"
                PROMPTING_VIDEO_COMPANY = company
                speak_output += " Would you like to watch a video on " + company + "?"
                return (
                    handler_input.response_builder
                        .speak(speak_output)
                        .ask(speak_output)
                        .response
                )

        else:
            speak_output = "Sorry, the company could not be found."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class VideoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("VideoIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = ""
        response_builder = handler_input.response_builder
        company = handler_input.request_envelope.request.intent.slots["company"].value
        data = None
        if company:
            data = get_company(company.split()[0])
        if data:
            if data["VIDEO"] == True:
                if get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
                    response_builder.add_directive(
                        get_video_directive(company)
                    )
                else:
                    speak_output = "Sorry, this device does not support video playing."
            else:
                speak_output = "Sorry, we could not find a video related to the company"
        else:
            speak_output = "Sorry, the company could not be found."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class YesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = ""
        response_builder = handler_input.response_builder

        global CURRENT_STATE
        global PROMPTING_VIDEO_COMPANY
        if CURRENT_STATE == "PROMPTING_VIDEO":
            company = PROMPTING_VIDEO_COMPANY
            data = get_company(company.split()[0])
            if data:
                if data["VIDEO"] == True:
                    if get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
                        response_builder.add_directive(
                            get_video_directive(company)
                        )
                    else:
                        speak_output = "Sorry, this device does not support video playing."
                else:
                    speak_output = "Sorry, we could not find a video related to the company"
            else:
                speak_output = "Sorry, the company could not be found."
            
            return response_builder.speak(speak_output).response
        elif CURRENT_STATE == "PROMPTING_NEWS":
            global READ_NEWS
            speak_output += get_insignia_news()[READ_NEWS]["title"]
            READ_NEWS += 1
            speak_output += ". Would you like more news?"
            CURRENT_STATE = "PROMPTING_NEWS"
            return response_builder.speak_output(speak_output).ask(speak_output).response
        else: return response_builder.speak_output(speak_output).response

class NoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = ""
        response_builder = handler_input.response_builder

        global CURRENT_STATE
        if CURRENT_STATE == "PROMPTING_VIDEO" or CURRENT_STATE == "PROMPTING_NEWS":
            speak_output += "Okay, that's alright"
        CURRENT_STATE = "IDLE"
        return response_builder.speak(speak_output).response

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response

class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.

sb = SkillBuilder()


sb.add_request_handler(LaunchRequestHandler())

sb.add_request_handler(CompanyInfoIntentHandler())
sb.add_request_handler(CompanyCEOIntentHandler())
sb.add_request_handler(CompanyFounderIntentHandler())
sb.add_request_handler(VideoIntentHandler())
sb.add_request_handler(InsigniaNewsIntentHandler())



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
