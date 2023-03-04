from mycroft import MycroftSkill, intent_file_handler, intent_handler
from adapt.intent import IntentBuilder

class EasyShopping(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    # Padatious intent cause no voc file
    # this is an older version decorator
    # @intent_file_handler('shopping.easy.intent')
    # def handle_shopping_easy(self, message):
    #     self.speak_dialog('shopping.easy')

    # use case 1
    @intent_handler('view.goods.intent')
    def handle_view_goods(self, message):
        self.speak('Taking a photo now. Please wait a second for me to get the result.')
        self.speak('I find some goods here, you can ask me whatever goods you want.')
        # self.speak_dialog('take.photo',{'item' : 'apple'})

    # the intent_handler() decorator can be used to create a Padatious intent handler by passing in the filename of the .intent file as a string
    # every single line in the intent needs to have the variable category
    @intent_handler('is.there.any.goods.intent')
    def handle_is_there_any_goods(self, message):
        category_label = message.data.get('category')
        str = 'yes, I find ' +  category_label + ' in front of you'
        self.speak(str)

    # use case 2
    @intent_handler(IntentBuilder('AskItemBrand').require('Brand').build())
    def handle_ask_item_brand(self, message):
        self.speak('I am talking about the brand of the item')

    @intent_handler(IntentBuilder('ViewItemInHand').require('ViewItemInHandKeyWord'))
    def handle_view_item_in_hand(self, message):
        self.speak('Taking a photo now. Please wait a second for me to get the result.')
        self.speak('The item is possible to be something. You can ask me any details about the item now, such as brand, color or complete information.')

    @intent_handler(IntentBuilder('AskItemCategory').require('Category').build())
    def handle_ask_item_category(self, message):
        self.speak('I am talking about the category of the item')

    @intent_handler(IntentBuilder('AskItemColor').require('Color').build())
    def handle_ask_item_color(self, message):
        self.speak('I am talking about the color of the item')

    @intent_handler(IntentBuilder('AskItemKw').require('Kw').build())
    def handle_ask_item_keywords(self, message):
        self.speak('I am talking about the keywords of the item')

    @intent_handler(IntentBuilder('AskItemInfo').require('Info').build())
    def handle_ask_item_complete_info(self, message):
        self.speak('I am speaking the complete information of the item')

    @intent_handler(IntentBuilder('FinishOneItem').require('Finish').build())
    def handle_finish_current_item(self, message):
        self.speak('Got you request. Let\'s continue shopping!')

    # https://mycroft-ai.gitbook.io/docs/skill-development/user-interaction/intents/adapt-intents
    # @intent_handler(IntentBuilder('FaqIntent').require('What').optionally('Is').optionally('Can'))
    # def handle_thank_you_intent(self, message):
    #     """ This is an Adapt intent handler, it is triggered by a keyword."""
    #     self.speak_dialog("welcome")

    # @intent_file_handler('HowAreYou.intent')
    # def handle_how_are_you_intent(self, message):
    #     """ This is a Padatious intent handler. It is triggered using a list of sample phrases."""
    #     self.speak_dialog("how.are.you")

def create_skill():
    return EasyShopping()

