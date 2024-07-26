from webexteamssdk import WebexTeamsAPI

class SpeedyBot:
    def __init__(self, token: str):
        self.token = token
        self.api = WebexTeamsAPI(access_token=self.token)

    def getTokemn(self):
        return self.token
    
    def sendMsg(self, email, msg):
        return self.api.messages.create(toPersonEmail=email, markdown=msg)

