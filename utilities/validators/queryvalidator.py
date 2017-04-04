from validationerror import ValidationError

class QueryValidator(object):
    def validateInput(self, inputJson):
        expectedKeys = [u'queryName', u'mainLogic', u'queryDescription', u'inputDefinition', u'outputDefinition', u'devicesUsed']
        for key in expectedKeys:
            if key not in inputJson:
                print key
                raise ValidationError(key + ' not defined!')