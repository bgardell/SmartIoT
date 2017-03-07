from pymongo import MongoClient
import base64
import json
from bson import json_util
from bson.objectid import ObjectId

from validators.skillvalidator import SkillValidator
from validators.validationerror import ValidationError

class SkillHandler:
    def __init__(self):
        self.client = MongoClient()
        self.skillDb = self.client.skillDatabase
        self.skillCollection = self.skillDb["skills"]
        self.skillValidator = SkillValidator()

    def addSkill(self, skill):
        skillName = skill["skillName"]
        try:
            self.skillValidator.validateInput(skill)
        except ValidationError, e:
            return {"Result" : "Failure", "Reason" : e.args}

        if self.skillCollection.find({"skillName" : skillName}).count() > 0:
            return { "Result " : "Failure", "Reason" : "Skill Already Exists!"}

        skillId = self.skillCollection.insert_one(skill).inserted_id
        return {"Result" : "Success", "SkillId" : str(skillId)}

    def deleteSkill(self, skillName):
        try:
            self.skillCollection[skillName].remove({"skillName" : skillName })
        except Exception as e:
            print "Could not delete skill " + e.message

    def getSkill(self, skillName):
        skillBson = self.skillCollection.find_one({"skillName": skillName})
        skillJson = self.skillToJson(skillBson)
        return skillJson

    def getAllSkills(self):
        allSkills = {"skills":[]}
        skillsBson = self.skillCollection.find()
        for skill in skillsBson:
            print skill
            allSkills["skills"].append( self.skillToJson(skill) )
        return allSkills

    def skillToJson(self, skill):
        if type(skill) == dict and "id" in skill:
            skill.pop("_id")
        return skill

class Skill:
    skillName = ""
    skillLogic = ""
    skillInput = {}
    skillOutput = {}
    commonKnowledge = {}

    def __init__(self, skillJson):
        self.skillJson = skillJson
        skillName = skillJson["skillName"]
        skillLogic = base64.decodestring(skillJson["mainLogic"])
        skillInput = skillJson["skilLInput"]
        skillOutput = skillJson["skillOutput"]
        commonKnowledge = skillJson["commonKnowledge"]