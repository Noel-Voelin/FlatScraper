import json
import re

class ComparisScrapper():
    def __init__(self,request_handler, room, price_from, price_to):
        self.request_handler = request_handler
        self.room = room
        self.price_form = price_from
        self.price_to = price_to

    def getFlats(self):
        flatLinks = list()
        try:
            content = self.__getSiteContent__("https://www.comparis.ch/immobilien/result/list?requestobject=%7B%22DealType%22%3A10%2C%22SiteId%22%3A0%2C%22RootPropertyTypes%22%3A%5B1%5D%2C%22PropertyTypes%22%3A%5B%5D%2C%22RoomsFrom%22%3A%222.5%22%2C%22RoomsTo%22%3Anull%2C%22FloorSearchType%22%3A0%2C%22LivingSpaceFrom%22%3Anull%2C%22LivingSpaceTo%22%3Anull%2C%22PriceFrom%22%3Anull%2C%22PriceTo%22%3A%222400%22%2C%22ComparisPointsMin%22%3A0%2C%22AdAgeMax%22%3A0%2C%22AdAgeInHoursMax%22%3Anull%2C%22Keyword%22%3A%22%22%2C%22WithImagesOnly%22%3Afalse%2C%22WithPointsOnly%22%3Anull%2C%22Radius%22%3Anull%2C%22MinAvailableDate%22%3Anull%2C%22MinChangeDate%22%3A%221753-01-01T00%3A00%3A00%22%2C%22LocationSearchString%22%3A%22Z%C3%BCrich%22%2C%22Sort%22%3A%223%22%2C%22HasBalcony%22%3Afalse%2C%22HasTerrace%22%3Afalse%2C%22HasFireplace%22%3Afalse%2C%22HasDishwasher%22%3Afalse%2C%22HasWashingMachine%22%3Afalse%2C%22HasLift%22%3Afalse%2C%22HasParking%22%3Afalse%2C%22PetsAllowed%22%3Afalse%2C%22MinergieCertified%22%3Afalse%2C%22WheelchairAccessible%22%3Afalse%2C%22LowerLeftLatitude%22%3Anull%2C%22LowerLeftLongitude%22%3Anull%2C%22UpperRightLatitude%22%3Anull%2C%22UpperRightLongitude%22%3Anull%7D&page=0".format(self.room, self.price_form, self.price_to))
            jsonContent = self.__paresePageContent__(content)


            for each in jsonContent["props"]["pageProps"]["initialResultData"]["resultItems"]:
                if "Befristet" not in str(each) and "befristet" not in str(each):
                    flatJson = json.loads(json.dumps(each))
                    listOfStrings = ['8046','8052','8051','8050','8053','8038','8041','8064']
                    address = str(flatJson["Address"])
                    if not any(code in address for code in listOfStrings):
                        flatLinks.append("https://www.comparis.ch/immobilien/marktplatz/details/show/" + str(flatJson["AdId"]))
        except Exception as e:
            print("Failed to fetch flats from Comparis with exception: ", e)
        return flatLinks


    def __getSiteContent__(self, url):
        homegateResponse = self.request_handler.get(url)
        return homegateResponse.text


    def __paresePageContent__(self, page_content):
        result = re.search(r"(?<=<script id=\"__NEXT_DATA__\" type=\"application\/json\">).*?(?=</script>)", page_content).group(0)
        j = json.loads(result)
        return j