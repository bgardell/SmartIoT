from validationerror import ValidationError

class SkillValidator(object):
    def validateInput(self, inputJson):
        expectedKeys = [u'skillName', u'mainLogic', u'skillDescription', u'inputDefinition', u'outputDefinition', u'commonKnowledge']
        for key in expectedKeys:
            if key not in inputJson:
                print key
                raise ValidationError(key + ' not defined!')