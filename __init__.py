from mycroft import MycroftSkill, intent_file_handler, intent_handler
from mycroft.skills.context import removes_context
from adapt.intent import IntentBuilder

LOGSTR = '********************====================########## '

def generate_str(possible_list):
    '''
    Generate string for Mycroft to speak it
    Args: 
        possible_list: array list with len = 3, each element is a string
    Returns:
        a string, e.g. possible_list = ['a', 'b', 'c'], res = 'a, b, and c'
    '''
    res = ''
    if len(possible_list) == 3:
        res = possible_list[0] + ' ' + \
            possible_list[1] + ' and ' + possible_list[2]
    elif len(possible_list) == 2:
        res = possible_list[0] + ' and ' + possible_list[1]
    elif len(possible_list) == 1:
        res = possible_list[0]

    return res

class EasyShopping(MycroftSkill):
    # Edit in main class: class EasyShopping(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.category_str = ''
        self.color_str = ''
        self.brand_str = ''
        self.kw_str = ''
        self.img_multi = ''
        self.img_hand = ''
        self.log.info(LOGSTR + "_init_ EasyShoppingSkill")

    # Padatious intent cause no voc file
    # this is an older version decorator
    # @intent_file_handler('shopping.easy.intent')
    # def handle_shopping_easy(self, message):
    #     self.speak_dialog('shopping.easy')

    # use case 1
    @intent_handler('view.goods.intent')
    def handle_view_goods(self, message):
        self.speak_dialog('take.photo')
        self.img_multi = ''
        self.img_hand = ''

        # suppose we use camera to take a photo here, 
        # then the function will return an image path
        self.img_multi = 'testPhoto/multi.jpeg'

        self.speak('I find some goods here, you can ask me whatever goods you want.')

    # the intent_handler() decorator can be used to create a Padatious intent handler by passing in the filename of the .intent file as a string
    # every single line in the intent needs to have the variable category
    # @intent_handler('is.there.any.goods.intent')
    # def handle_is_there_any_goods(self, message):
    #     category_label = message.data.get('category')
    #     str = 'yes, I find ' +  category_label + ' in front of you'
    #     self.speak(str)

    @intent_handler('is.there.any.goods.intent')
    def handle_is_there_any_goods(self, message):
        if self.img_multi == '':
            # if self.img_multi == '', 
            # then it means that user hasn't invoked intent(handle_view_goods)
            self.handle_no_context1(message)
        else:
            # in real application, label_str and loc_list will return from CV API
            label_list = [['milk', 'drink', 'bottle'], ['milk', 'drink', 'bottle']]
            loc_list = ['left top', 'right top']

            category_label = message.data.get('category')
            detected = 0

            for i in range(len(label_list)):
                label_str = generate_str(label_list[i])
                label_str = label_str.lower()

                if category_label is not None:
                    if category_label in label_str:
                        self.speak_dialog('yes.goods',
                                        {'category': category_label,
                                        'location': loc_list[i]})
                        detected = 1
                        break
                else:
                    continue

            if detected == 0:
                self.speak_dialog('no.goods',
                                {'category': category_label})

    # use case 2

    # @intent_handler(IntentBuilder('ViewItemInHand').require('ViewItemInHandKeyWord'))
    # def handle_view_item_in_hand(self, message):
    #     self.speak('Taking a photo now. Please wait a second for me to get the result.')
    #     self.speak('The item is possible to be something. You can ask me any details about the item now, such as brand, color or complete information.')

    # @intent_handler(IntentBuilder('AskItemBrand').require('Brand').build())
    # def handle_ask_item_brand(self, message):
    #     self.speak('I am talking about the brand of the item')

    # @intent_handler(IntentBuilder('AskItemCategory').require('Category').build())
    # def handle_ask_item_category(self, message):
    #     self.speak('I am talking about the category of the item')

    # @intent_handler(IntentBuilder('AskItemColor').require('Color').build())
    # def handle_ask_item_color(self, message):
    #     self.speak('I am talking about the color of the item')

    # @intent_handler(IntentBuilder('AskItemKw').require('Kw').build())
    # def handle_ask_item_keywords(self, message):
    #     self.speak('I am talking about the keywords of the item')

    # @intent_handler(IntentBuilder('AskItemInfo').require('Info').build())
    # def handle_ask_item_complete_info(self, message):
    #     self.speak('I am speaking the complete information of the item')

    # @intent_handler(IntentBuilder('FinishOneItem').require('Finish').build())
    # def handle_finish_current_item(self, message):
    #     self.speak('Got you request. Let\'s continue shopping!')

    @intent_handler(IntentBuilder('ViewItemInHand').require('ViewItemInHandKeyWord'))
    def handle_view_item_in_hand(self, message):
        self.speak_dialog('take.photo')
        self.img_multi = ''
        self.img_hand = ''

        # suppose we use camera to take a photo here,
        # then the function will return an image path
        self.img_hand = 'testPhoto/2.jpeg'

        # suppose we call CV API here to get the result,
        # the result will all be list, then we use generate_str() to create string
        self.category_str = generate_str(['milk', 'bottle', 'drink'])
        self.brand_str = generate_str(['Dutch Lady', 'Lady'])
        self.color_str = generate_str(['white', 'black', 'blue'])
        self.kw_str = ' '.join(['milk', 'bottle', 'protein', 'pure', 'farm'])

        # set the context
        self.set_context('getDetailContext')

        # speak dialog
        self.speak_dialog('item.category', {'category': self.category_str})

    @intent_handler(IntentBuilder('AskItemBrand').require('Brand').require('getDetailContext').build())
    def handle_ask_item_brand(self, message):
        self.speak('I am talking about the brand of the item')
        # self.handle_ask_item_detail('brand', self.brand_str)

    @intent_handler(IntentBuilder('AskItemCategory').require('Category').require('getDetailContext').build())
    def handle_ask_item_category(self, message):
        self.speak('I am talking about the category of the item')
        # self.handle_ask_item_detail('category', self.category_str)

    @intent_handler(IntentBuilder('AskItemColor').require('Color').require('getDetailContext').build())
    def handle_ask_item_color(self, message):
        self.speak('I am talking about the color of the item')
        # self.handle_ask_item_detail('color', self.color_str)

    @intent_handler(IntentBuilder('AskItemKw').require('Kw').require('getDetailContext').build())
    def handle_ask_item_keywords(self, message):
        self.speak('I am talking about the keywords of the item')
        # self.handle_ask_item_detail('keyword', self.kw_str)

    @intent_handler(IntentBuilder('AskItemInfo').require('Info').require('getDetailContext').build())
    def handle_ask_item_complete_info(self, message):
        self.speak('I am speaking the complete information of the item')
        # self.speak_dialog('item.complete.info', {'category': self.category_str})
        # self.handle_ask_item_detail('color', self.color_str)
        # self.handle_ask_item_detail('brand', self.brand_str)
        # self.handle_ask_item_detail('keyword', self.kw_str)

    # under class EasyShoppingSkill(MycroftSkill):

    @intent_handler(IntentBuilder('FinishOneItem').require('Finish').require('getDetailContext').build())
    @removes_context('getDetailContext')
    def handle_finish_current_item(self, message):
        self.speak('Got you request. Let\'s continue shopping!')
        self.types_str = ''
        self.color_str = ''
        self.logo_str = ''
        self.kw_str = ''
        self.img_hand = ''
        self.img_multi = ''


    # https://mycroft-ai.gitbook.io/docs/skill-development/user-interaction/intents/adapt-intents
    # @intent_handler(IntentBuilder('FaqIntent').require('What').optionally('Is').optionally('Can'))
    # def handle_thank_you_intent(self, message):
    #     """ This is an Adapt intent handler, it is triggered by a keyword."""
    #     self.speak_dialog("welcome")

    # @intent_file_handler('HowAreYou.intent')
    # def handle_how_are_you_intent(self, message):
    #     """ This is a Padatious intent handler. It is triggered using a list of sample phrases."""
    #     self.speak_dialog("how.are.you")

    def handle_no_context1(self, message):
        self.speak('Please let me have a look at what\'s in front of you first.')
        # add prompts
        take_photo = self.ask_yesno('do.you.want.to.take.a.photo') # This calls .dialog file.
        if take_photo == 'yes':
            self.handle_view_goods(message)
        elif take_photo == 'no':
            self.speak('OK. I won\'t take photo')
        else:
            self.speak('I cannot understand what you are saying')

def create_skill():
    return EasyShopping()
