import json
import requests
import re

class HomeGateScrapper:
    def __init__(self,request_handler, room, price_from, price_to):
        self.request_handler = request_handler
        self.room = room
        self.price_form = price_from
        self.price_to = price_to

    def getFlats(self):
        flatLinks = list()
        try:
            content = self.__getSiteContent__("https://www.homegate.ch/mieten/immobilien/ort-zuerich/trefferliste?ac={}&o=dateCreated-desc&ag={}&ah={}".format(self.room, self.price_form, self.price_to))
            jsonContent = self.__paresePageContent__(content)

            for each in jsonContent['resultList']["search"]["fullSearch"]["result"]["listings"]:
                if "Befristet" not in str(each) and "befristet" not in str(each):
                    flatJson = json.loads(json.dumps(each))
                    listOfStrings = ['8046','8052','8051','8050','8053','8038','8041','8064']
                    postalCode = flatJson["listing"]["address"]["postalCode"]
                    if postalCode not in listOfStrings and postalCode.startswith("80"):
                        flatLinks.append("https://www.homegate.ch/mieten/" + flatJson["id"])
        except Exception as e:
            print("Failed to fetch flats from Homegate with exception: ", e)
        return flatLinks


    def __getSiteContent__(self, url):
        homegateResponse = self.request_handler.get(url)
        return homegateResponse.text


    def __paresePageContent__(self, page_content):
        result = re.search(r"(?<=__INITIAL_STATE__=).*?(?=</script>)", page_content).group(0)
        j = json.loads(result)
        return j