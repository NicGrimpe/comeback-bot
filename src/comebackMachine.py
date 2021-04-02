import discord
import json
import re

class ComebackMachine:

    def __init__(self, path, botToken):
        self.comebacks = []
        self.comebacksPath = path
        self.client = discord.Client()
        self.BOT_TOKEN = botToken
        
        self.loadComebacks()

        @self.client.event
        async def on_ready():
            self.onReady()

        @self.client.event
        async def on_message(message):
            await self.onMessage(message)

    def run(self):
        self.client.run(self.BOT_TOKEN)

    def onReady(self):
        print('We have logged in as {0.user}'.format(self.client))

    async def onMessage(self, message):
        if message.author == self.client.user:
            return
        if (re.search('^\$help', message.content) != None):
            answer = self.getHelp()
        elif (re.search('^\$add', message.content) != None):
            self.addComeback(message.content)
            answer = "Added."
        elif (re.search('^\$remove', message.content) != None):
            if (self.removeComeback(message.content)):
                answer = "Removed."
            else:
                answer = "Key not present you noob."

        elif (re.search('^\$list', message.content) != None):
            answer = self.getComebacks()
        else:
            comeback = self.checkIfValidComeback(message.content)
            if (comeback != None):
                answer = comeback
            else:
                return
        
        await message.channel.send(answer)

    def checkIfValidComeback(self, querryString):
        for key in self.comebacks:
            if (re.search(key, querryString) != None):
                return self.comebacks[key]
        return None

    def checkKeys(self, querryKey):
        for key in self.comebacks:
            if (querryKey == key):
                return True
        return False

    def addComeback(self, message):
        print("New entry")
        msgSplitted = message.split('-', 3)
        if (len(msgSplitted) != 3):
            return
        print(msgSplitted)
        newCombo = {msgSplitted[1]:msgSplitted[2]}
        self.saveComeback(newCombo)
        return

    def removeComeback(self, message):
        print("Removing an entry")
        msgSplitted = message.split('-', 2)
        print(msgSplitted)
        if (self.checkKeys(msgSplitted[1])):
            self.comebacks.pop(msgSplitted[1], None)
            with open(self.comebacksPath, 'w') as json_file:
                json.dump(self.comebacks, json_file)
            return True
        else:
            return False

    def loadComebacks(self):
        with open(self.comebacksPath, 'r') as json_file:
            self.comebacks = json.load(json_file)

    def saveComeback(self, comebackTuple):
        self.comebacks.update(comebackTuple)
        with open(self.comebacksPath, 'w') as json_file:
            json.dump(self.comebacks, json_file)

    def getComebacks(self):
        comebacksHeader = " --- Comebacks --- \r"
        comebacksFormatted = ""
        count = 1
        for key in self.comebacks:
            comebacksFormatted += str(count) + "- " + str(key) + " ---> " + str(self.comebacks[key]) + "\r"
            count+=1
        return comebacksHeader + comebacksFormatted

    def getHelp(self):
        helpHeader = " --- Help --- \r"
        comebacksFormatted = "$add-StringToWatch-Reply ---> Ajoute une reply \r"
        comebacksFormatted += "$remove-StringWatched ---> Enleve le tuple string/reply \r"
        comebacksFormatted += "$list ---> Liste les tuples string/reply \r"
        return helpHeader + comebacksFormatted

