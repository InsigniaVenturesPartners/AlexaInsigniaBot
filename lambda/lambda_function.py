import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response
from ask_sdk_model.interfaces.alexa.presentation.apl import (RenderDocumentDirective, ExecuteCommandsDirective)

from utils import (load_json_from_path, create_all_video_playlist, create_presigned_url)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

insignia_video_url = create_presigned_url("Media/INSIGNIA_VC_VIDEO.mp4")

currentState = "IDLE"

def playlist():
    return [
        {
            "url": insignia_video_url,
            "title": "Insignia Video",
            "subtitle": ""
        }
    ]

class LaunchRequestHandler(AbstractRequestHandler):
    #Handler for Skill Launch
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = "Welcome, my name is Insignia Bot, I'm here to tell you more about Insignia Ventures Partners"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class IntroductionIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("IntroductionIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "Insignia Ventures Partners is an early-stage technology venture capital firm partnering with unstoppable founders to build great companies in Southeast Asia. Portfolio companies include Goto, Appier, Carro, Ajaib, Shipper, Tonik, Flip, Payfazz, Super and many other technology market leaders. We partner early with founders and support them from seed through growth stage as their companies create meaningful impact for millions of people in Southeast Asia and beyond. Our team of investment and operating professionals bring together decades of experience and proprietary networks to equip our founders with the tools they need for growth. Insignia Ventures Partners manages capital from premier institutional investors including sovereign wealth funds, foundations, university endowments and renowned family offices from Asia, Europe and North America."
        speak_output = ""
        speak_output += " Would you like to watch a video from Insignia Ventures Partners?"
        currentState = "PROMPTING_VIDEO"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class YesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = ""
        if currentState == "PROMPTING_VIDEO":
            video_directive = RenderDocumentDirective(
                token = "VideoPlayer",
                document = load_json_from_path("apl/render-videoplayer.json"),
                datasources = create_all_video_playlist(playlist())
            )
            
            currentState = "IDLE"
            
            return (
                handler_input.response_builder
                    .speak("Here is a video for more information on Insignia Ventures Partners")
                    .add_directive(video_directive)
                    .response
            )
        else:
            
            currentState = "IDLE"
        
        speak_output = "Insignia Ventures Partners is an early-stage technology venture capital firm partnering with unstoppable founders to build great companies in Southeast Asia. Portfolio companies include Goto, Appier, Carro, Ajaib, Shipper, Tonik, Flip, Payfazz, Super and many other technology market leaders. We partner early with founders and support them from seed through growth stage as their companies create meaningful impact for millions of people in Southeast Asia and beyond. Our team of investment and operating professionals bring together decades of experience and proprietary networks to equip our founders with the tools they need for growth. Insignia Ventures Partners manages capital from premier institutional investors including sovereign wealth funds, foundations, university endowments and renowned family offices from Asia, Europe and North America."
        speak_output = ""
        speak_output += " Would you like to watch a video from Insignia Ventures Partners?"
        currentState = "PROMPTING_VIDEO"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
        
class NoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        

class (AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("")(handler_input)
    def handle(self, handler_input):
        


class NoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.NoIntent")(handler_input)
    def handle(self, handler_input):
        speak_output = ""
        if currentState == "PROMPTING_VIDEO":
            speak_output = "Okay, that's alright"
            
        currentState = "IDLE"
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
sb.add_request_handler(IntroductionIntentHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NoIntentHandler())
sb.add_request_handler(PlayIntentHandler())
sb.add_request_handler(PauseIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler())


sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()