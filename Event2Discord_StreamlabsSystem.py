#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Event2Discord for Streamlabs Chatbot
    1.0.5
        Added a button to open the StreamLabs.com API settings page.

    1.0.4
        Fixed donation messages
        
    1.0.3
        Added Boilerplate v1.0.2 of StreamlabsEventReceiver.dll, which should solve the Donations issue.
        
    1.0.2
        Fixed an issue with 0 inputs in "amount" by the user.
        Known issue: Donations without a message might not show up in Discord.

    1.0.1
        Fixed an issue with (re)subs not showing the months.

    1.0.0
        Initial release
    
    StreamlabsEventReceiver.dll (DLL version 1.0.1) has been received from Ocgineer#0042 on the Streamlabs Chatbot discord at https://discord.gg/xFcsxft

"""

#---------------------------------------
# Script Import Libraries
#---------------------------------------
import clr
import os
import json
import codecs
from decimal import Decimal

clr.AddReference("IronPython.Modules.dll")
clr.AddReferenceToFileAndPath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "StreamlabsEventReceiver.dll"))
from StreamlabsEventReceiver import StreamlabsEventClient

#---------------------------------------
# Script Information
#---------------------------------------
ScriptName = "Event2Discord"
Website = "http://www.twitch.tv/masterguy"
Description = "Allows for up to 20 triggers to send messages to Discord when triggered by events. (bits/donations/host/raid/follow/sub/resub)"
Creator = "MasterGuy"
Version = "1.0.4"

#---------------------------------------
# Script Variables
#---------------------------------------
SettingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
EventReceiver = None
Debug = True
lastParsed = 1

#---------------------------------------
# Script Classes
#---------------------------------------
class Settings(object):
    """ Load in saved settings file if available else set default values. """
    def __init__(self, settingsfile=None):
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
                self.__dict__ = json.load(f, encoding="utf-8")
        except:
            self.socket_token = None
            self.Debug = False
            self.trigger1_type = "Disabled"
            self.trigger1_leg = "Equals"
            self.trigger1_amount = "0"
            self.trigger1_discordmsg = "Discord message"
            self.trigger2_type = "Disabled"
            self.trigger2_leg = "Equals"
            self.trigger2_amount = "0"
            self.trigger2_discordmsg = "Discord message"
            self.trigger3_type = "Disabled"
            self.trigger3_leg = "Equals"
            self.trigger3_amount = "0"
            self.trigger3_discordmsg = "Discord message"
            self.trigger4_type = "Disabled"
            self.trigger4_leg = "Equals"
            self.trigger4_amount = "0"
            self.trigger4_discordmsg = "Discord message"
            self.trigger5_type = "Disabled"
            self.trigger5_leg = "Equals"
            self.trigger5_amount = "0"
            self.trigger5_discordmsg = "Discord message"
            self.trigger6_type = "Disabled"
            self.trigger6_leg = "Equals"
            self.trigger6_amount = "0"
            self.trigger6_discordmsg = "Discord message"
            self.trigger7_type = "Disabled"
            self.trigger7_leg = "Equals"
            self.trigger7_amount = "0"
            self.trigger7_discordmsg = "Discord message"
            self.trigger8_type = "Disabled"
            self.trigger8_leg = "Equals"
            self.trigger8_amount = "0"
            self.trigger8_discordmsg = "Discord message"
            self.trigger9_type = "Disabled"
            self.trigger9_leg = "Equals"
            self.trigger9_amount = "0"
            self.trigger9_discordmsg = "Discord message"
            self.trigger10_type = "Disabled"
            self.trigger10_leg = "Equals"
            self.trigger10_amount = "0"
            self.trigger10_discordmsg = "Discord message"
            self.trigger11_type = "Disabled"
            self.trigger11_leg = "Equals"
            self.trigger11_amount = "0"
            self.trigger11_discordmsg = "Discord message"
            self.trigger12_type = "Disabled"
            self.trigger12_leg = "Equals"
            self.trigger12_amount = "0"
            self.trigger12_discordmsg = "Discord message"
            self.trigger13_type = "Disabled"
            self.trigger13_leg = "Equals"
            self.trigger13_amount = "0"
            self.trigger13_discordmsg = "Discord message"
            self.trigger14_type = "Disabled"
            self.trigger14_leg = "Equals"
            self.trigger14_amount = "0"
            self.trigger14_discordmsg = "Discord message"
            self.trigger15_type = "Disabled"
            self.trigger15_leg = "Equals"
            self.trigger15_amount = "0"
            self.trigger15_discordmsg = "Discord message"
            self.trigger16_type = "Disabled"
            self.trigger16_leg = "Equals"
            self.trigger16_amount = "0"
            self.trigger16_discordmsg = "Discord message"
            self.trigger17_type = "Disabled"
            self.trigger17_leg = "Equals"
            self.trigger17_amount = "0"
            self.trigger17_discordmsg = "Discord message"
            self.trigger18_type = "Disabled"
            self.trigger18_leg = "Equals"
            self.trigger18_amount = "0"
            self.trigger18_discordmsg = "Discord message"
            self.trigger19_type = "Disabled"
            self.trigger19_leg = "Equals"
            self.trigger19_amount = "0"
            self.trigger19_discordmsg = "Discord message"
            self.trigger20_type = "Disabled"
            self.trigger20_leg = "Equals"
            self.trigger20_amount = "0"
            self.trigger20_discordmsg = "Discord message"

    def Reload(self, jsondata):
        self.__dict__ = json.loads(jsondata, encoding="utf-8")

#---------------------------------------
# Chatbot Initialize Function
#---------------------------------------
def Init():
    # Load settings from settings file
    global ScriptSettings
    ScriptSettings = Settings(SettingsFile)

    ## Init the Streamlabs Event Receiver
    global EventReceiver
    EventReceiver = StreamlabsEventClient()
    EventReceiver.StreamlabsSocketConnected += EventReceiverConnected
    EventReceiver.StreamlabsSocketDisconnected += EventReceiverDisconnected
    EventReceiver.StreamlabsSocketEvent += EventReceiverEvent

    ## Auto Connect if key is given in settings
    if ScriptSettings.socket_token:
        EventReceiver.Connect(ScriptSettings.socket_token)

    # End of Init
    return

#---------------------------------------
# Chatbot Save Settings Function
#---------------------------------------
def ReloadSettings(jsondata):
    
    if EventReceiver and EventReceiver.IsConnected:
        EventReceiver.Disconnect()
    
    # Reload newly saved settings and verify
    global ScriptSettings
    ScriptSettings.Reload(jsondata)

    # Connect if token has been entered and EventReceiver is not connected
    # This can then connect without having to reload the script
    if EventReceiver and not EventReceiver.IsConnected:
        if ScriptSettings.socket_token:
            EventReceiver.Connect(ScriptSettings.socket_token)

    # End of ReloadSettings
    return

#---------------------------------------
# Script Functions
#---------------------------------------

def OpenAPIsettingsPage():
    Parent.Log("Button click", "Opening the StreamLabs.com API settings page.")
    os.system("explorer https://streamlabs.com/dashboard#/settings/api-settings")
    return

def EventReceiverConnected(sender, args):
    Parent.Log(ScriptName, "Streamlabs event websocket connected")
    return

def EventReceiverDisconnected(sender, args):
    Parent.Log(ScriptName, "Streamlabs event websocket disconnected")
    return

def EventReceiverEvent(sender, args):
    evntdata = args.Data
    global ScriptSettings
    global lastParsed
    if lastParsed == evntdata.GetHashCode():
        return # Fixes a strange bug where Chatbot registers to the DLL multiple times
    lastParsed = evntdata.GetHashCode()
    if ScriptSettings.debug:
        Parent.Log("EventReceiverEvent", "Object: {0}".format(dir(evntdata)))
        Parent.Log("EventReceiverEvent", "HashCode: {0}".format(evntdata.GetHashCode()))
        Parent.Log("EventReceiverEvent", "For: {0}".format(evntdata.For))
        Parent.Log("EventReceiverEvent", "Type: {0}".format(evntdata.Type))
        Parent.Log("EventReceiverEvent", "Message: {0}".format(evntdata.Message))
        for message in evntdata.Message:
            Parent.Log("Message", "Object: {0}".format(dir(message)))

    if evntdata and evntdata.For == "twitch_account":
        if evntdata.Type == "follow":
            for message in evntdata.Message:
                parseFollow(message)

        elif evntdata.Type == "bits":
            for message in evntdata.Message:
                parseBits(message)

        elif evntdata.Type == "host":
            for message in evntdata.Message:
                parseHost(message)

        elif evntdata.Type == "raid":
            for message in evntdata.Message:
                parseRaid(message)

        elif evntdata.Type == "subscription":
            for message in evntdata.Message:
                if message.SubType and message.SubType == "resub":
                    parseResub(message)
                else:
                    parseSub(message)

        elif evntdata.Type == "resub":
            for message in evntdata.Message:
                parseResub(message)

    elif evntdata and evntdata.For == "streamlabs":
        if evntdata.Type == "donation":
            for message in evntdata.Message:
                parseDonation(message)
    return

#---------------------------------------
#    Chatbot Script Unload Function
#---------------------------------------
def Unload():

    # Disconnect EventReceiver cleanly
    global EventReceiver
    if EventReceiver and EventReceiver.IsConnected:
        EventReceiver.Disconnect()
    EventReceiver = None

    # End of Unload
    return

#---------------------------------------
# Chatbot Execute Function
#---------------------------------------
def Execute(data):
    return

#---------------------------------------
# Chatbot Tick Function
#---------------------------------------
def Tick():
    return

#---------------------------------------
# Parsing Functions
#---------------------------------------
def parseMessage(message, par0, par1, par2):
    Parent.SendDiscordMessage(message.format(par0, par1, par2))
    return

def parseFollow(message):
    global ScriptSettings
    if ScriptSettings.debug:
        Parent.Log("FollowMessage", "CreatedAt: {0}".format(message.CreatedAt))
        Parent.Log("FollowMessage", "Id: {0}".format(message.Id))
        Parent.Log("FollowMessage", "IsLive: {0}".format(message.IsLive))
        Parent.Log("FollowMessage", "IsRepeat: {0}".format(message.IsRepeat))
        Parent.Log("FollowMessage", "IsTest: {0}".format(message.IsTest))
        Parent.Log("FollowMessage", "Name: {0}".format(message.Name))
        Parent.SendDiscordMessage("Debug follow message")
    if ScriptSettings.trigger1_type == "Follow":
        parseMessage(ScriptSettings.trigger1_discordmsg, message.Name, "", "")
    if ScriptSettings.trigger2_type == "Follow":
        parseMessage(ScriptSettings.trigger2_discordmsg, message.Name, "", "")
    if ScriptSettings.trigger3_type == "Follow":
        parseMessage(ScriptSettings.trigger3_discordmsg, message.Name, "", "")
    if ScriptSettings.trigger4_type == "Follow":
        parseMessage(ScriptSettings.trigger4_discordmsg, message.Name, "", "")
    if ScriptSettings.trigger5_type == "Follow":
        parseMessage(ScriptSettings.trigger5_discordmsg, message.Name, "", "")
    if ScriptSettings.trigger6_type == "Follow":
        parseMessage(ScriptSettings.trigger6_discordmsg, message.Name, "", "")
    if ScriptSettings.trigger7_type == "Follow":
        parseMessage(ScriptSettings.trigger7_discordmsg, message.Name, "", "")
    if ScriptSettings.trigger8_type == "Follow":
        parseMessage(ScriptSettings.trigger8_discordmsg, message.Name, "", "")
    if ScriptSettings.trigger9_type == "Follow":
        parseMessage(ScriptSettings.trigger9_discordmsg, message.Name, "", "")
    if ScriptSettings.trigger10_type == "Follow":
        parseMessage(ScriptSettings.trigger10_discordmsg, message.Name, "", "")
    if ScriptSettings.trigger11_type == "Follow":
        parseMessage(ScriptSettings.trigger11_discordmsg, message.Name, "", "")
    if ScriptSettings.trigger12_type == "Follow":
        parseMessage(ScriptSettings.trigger12_discordmsg, message.Name, "", "")
    if ScriptSettings.trigger13_type == "Follow":
        parseMessage(ScriptSettings.trigger13_discordmsg, message.Name, "", "")
    if ScriptSettings.trigger14_type == "Follow":
        parseMessage(ScriptSettings.trigger14_discordmsg, message.Name, "", "")
    if ScriptSettings.trigger15_type == "Follow":
        parseMessage(ScriptSettings.trigger15_discordmsg, message.Name, "", "")
    if ScriptSettings.trigger16_type == "Follow":
        parseMessage(ScriptSettings.trigger16_discordmsg, message.Name, "", "")
    if ScriptSettings.trigger17_type == "Follow":
        parseMessage(ScriptSettings.trigger17_discordmsg, message.Name, "", "")
    if ScriptSettings.trigger18_type == "Follow":
        parseMessage(ScriptSettings.trigger18_discordmsg, message.Name, "", "")
    if ScriptSettings.trigger19_type == "Follow":
        parseMessage(ScriptSettings.trigger19_discordmsg, message.Name, "", "")
    if ScriptSettings.trigger20_type == "Follow":
        parseMessage(ScriptSettings.trigger20_discordmsg, message.Name, "", "")
    return

def parseBits(message):
    global ScriptSettings
    if ScriptSettings.debug:
        Parent.Log("BitsMessage", "Amount: {0}".format(message.Amount))
        Parent.Log("BitsMessage", "IsLive: {0}".format(message.IsLive))
        Parent.Log("BitsMessage", "IsRepeat: {0}".format(message.IsRepeat))
        Parent.Log("BitsMessage", "IsTest: {0}".format(message.IsTest))
        Parent.Log("BitsMessage", "Message: {0}".format(message.Message))
        Parent.Log("BitsMessage", "Name: {0}".format(message.Name))
        Parent.SendDiscordMessage("Debug bits message")
    if ScriptSettings.trigger1_type == "Bits" and ((ScriptSettings.trigger1_leg == "More then" and ScriptSettings.trigger1_amount < message.Amount) or (ScriptSettings.trigger1_leg == "Equals" and ScriptSettings.trigger1_amount == message.Amount) or (ScriptSettings.trigger1_leg == "Less then" and ScriptSettings.trigger1_amount > message.Amount)):
        parseMessage(ScriptSettings.trigger1_discordmsg, message.Name, message.Amount, message.Message)
    if ScriptSettings.trigger2_type == "Bits" and ((ScriptSettings.trigger2_leg == "More then" and ScriptSettings.trigger2_amount < message.Amount) or (ScriptSettings.trigger2_leg == "Equals" and ScriptSettings.trigger2_amount == message.Amount) or (ScriptSettings.trigger2_leg == "Less then" and ScriptSettings.trigger2_amount > message.Amount)):
        parseMessage(ScriptSettings.trigger2_discordmsg, message.Name, message.Amount, message.Message)
    if ScriptSettings.trigger3_type == "Bits" and ((ScriptSettings.trigger3_leg == "More then" and ScriptSettings.trigger3_amount < message.Amount) or (ScriptSettings.trigger3_leg == "Equals" and ScriptSettings.trigger3_amount == message.Amount) or (ScriptSettings.trigger3_leg == "Less then" and ScriptSettings.trigger3_amount > message.Amount)):
        parseMessage(ScriptSettings.trigger3_discordmsg, message.Name, message.Amount, message.Message)
    if ScriptSettings.trigger4_type == "Bits" and ((ScriptSettings.trigger4_leg == "More then" and ScriptSettings.trigger4_amount < message.Amount) or (ScriptSettings.trigger4_leg == "Equals" and ScriptSettings.trigger4_amount == message.Amount) or (ScriptSettings.trigger4_leg == "Less then" and ScriptSettings.trigger4_amount > message.Amount)):
        parseMessage(ScriptSettings.trigger4_discordmsg, message.Name, message.Amount, message.Message)
    if ScriptSettings.trigger5_type == "Bits" and ((ScriptSettings.trigger5_leg == "More then" and ScriptSettings.trigger5_amount < message.Amount) or (ScriptSettings.trigger5_leg == "Equals" and ScriptSettings.trigger5_amount == message.Amount) or (ScriptSettings.trigger5_leg == "Less then" and ScriptSettings.trigger5_amount > message.Amount)):
        parseMessage(ScriptSettings.trigger5_discordmsg, message.Name, message.Amount, message.Message)
    if ScriptSettings.trigger6_type == "Bits" and ((ScriptSettings.trigger6_leg == "More then" and ScriptSettings.trigger6_amount < message.Amount) or (ScriptSettings.trigger6_leg == "Equals" and ScriptSettings.trigger6_amount == message.Amount) or (ScriptSettings.trigger6_leg == "Less then" and ScriptSettings.trigger6_amount > message.Amount)):
        parseMessage(ScriptSettings.trigger6_discordmsg, message.Name, message.Amount, message.Message)
    if ScriptSettings.trigger7_type == "Bits" and ((ScriptSettings.trigger7_leg == "More then" and ScriptSettings.trigger7_amount < message.Amount) or (ScriptSettings.trigger7_leg == "Equals" and ScriptSettings.trigger7_amount == message.Amount) or (ScriptSettings.trigger7_leg == "Less then" and ScriptSettings.trigger7_amount > message.Amount)):
        parseMessage(ScriptSettings.trigger7_discordmsg, message.Name, message.Amount, message.Message)
    if ScriptSettings.trigger8_type == "Bits" and ((ScriptSettings.trigger8_leg == "More then" and ScriptSettings.trigger8_amount < message.Amount) or (ScriptSettings.trigger8_leg == "Equals" and ScriptSettings.trigger8_amount == message.Amount) or (ScriptSettings.trigger8_leg == "Less then" and ScriptSettings.trigger8_amount > message.Amount)):
        parseMessage(ScriptSettings.trigger8_discordmsg, message.Name, message.Amount, message.Message)
    if ScriptSettings.trigger9_type == "Bits" and ((ScriptSettings.trigger9_leg == "More then" and ScriptSettings.trigger9_amount < message.Amount) or (ScriptSettings.trigger9_leg == "Equals" and ScriptSettings.trigger9_amount == message.Amount) or (ScriptSettings.trigger9_leg == "Less then" and ScriptSettings.trigger9_amount > message.Amount)):
        parseMessage(ScriptSettings.trigger9_discordmsg, message.Name, message.Amount, message.Message)
    if ScriptSettings.trigger10_type == "Bits" and ((ScriptSettings.trigger10_leg == "More then" and ScriptSettings.trigger10_amount < message.Amount) or (ScriptSettings.trigger10_leg == "Equals" and ScriptSettings.trigger10_amount == message.Amount) or (ScriptSettings.trigger10_leg == "Less then" and ScriptSettings.trigger10_amount > message.Amount)):
        parseMessage(ScriptSettings.trigger10_discordmsg, message.Name, message.Amount, message.Message)
    if ScriptSettings.trigger11_type == "Bits" and ((ScriptSettings.trigger11_leg == "More then" and ScriptSettings.trigger11_amount < message.Amount) or (ScriptSettings.trigger11_leg == "Equals" and ScriptSettings.trigger11_amount == message.Amount) or (ScriptSettings.trigger11_leg == "Less then" and ScriptSettings.trigger11_amount > message.Amount)):
        parseMessage(ScriptSettings.trigger11_discordmsg, message.Name, message.Amount, message.Message)
    if ScriptSettings.trigger12_type == "Bits" and ((ScriptSettings.trigger12_leg == "More then" and ScriptSettings.trigger12_amount < message.Amount) or (ScriptSettings.trigger12_leg == "Equals" and ScriptSettings.trigger12_amount == message.Amount) or (ScriptSettings.trigger12_leg == "Less then" and ScriptSettings.trigger12_amount > message.Amount)):
        parseMessage(ScriptSettings.trigger12_discordmsg, message.Name, message.Amount, message.Message)
    if ScriptSettings.trigger13_type == "Bits" and ((ScriptSettings.trigger13_leg == "More then" and ScriptSettings.trigger13_amount < message.Amount) or (ScriptSettings.trigger13_leg == "Equals" and ScriptSettings.trigger13_amount == message.Amount) or (ScriptSettings.trigger13_leg == "Less then" and ScriptSettings.trigger13_amount > message.Amount)):
        parseMessage(ScriptSettings.trigger13_discordmsg, message.Name, message.Amount, message.Message)
    if ScriptSettings.trigger14_type == "Bits" and ((ScriptSettings.trigger14_leg == "More then" and ScriptSettings.trigger14_amount < message.Amount) or (ScriptSettings.trigger14_leg == "Equals" and ScriptSettings.trigger14_amount == message.Amount) or (ScriptSettings.trigger14_leg == "Less then" and ScriptSettings.trigger14_amount > message.Amount)):
        parseMessage(ScriptSettings.trigger14_discordmsg, message.Name, message.Amount, message.Message)
    if ScriptSettings.trigger15_type == "Bits" and ((ScriptSettings.trigger15_leg == "More then" and ScriptSettings.trigger15_amount < message.Amount) or (ScriptSettings.trigger15_leg == "Equals" and ScriptSettings.trigger15_amount == message.Amount) or (ScriptSettings.trigger15_leg == "Less then" and ScriptSettings.trigger15_amount > message.Amount)):
        parseMessage(ScriptSettings.trigger15_discordmsg, message.Name, message.Amount, message.Message)
    if ScriptSettings.trigger16_type == "Bits" and ((ScriptSettings.trigger16_leg == "More then" and ScriptSettings.trigger16_amount < message.Amount) or (ScriptSettings.trigger16_leg == "Equals" and ScriptSettings.trigger16_amount == message.Amount) or (ScriptSettings.trigger16_leg == "Less then" and ScriptSettings.trigger16_amount > message.Amount)):
        parseMessage(ScriptSettings.trigger16_discordmsg, message.Name, message.Amount, message.Message)
    if ScriptSettings.trigger17_type == "Bits" and ((ScriptSettings.trigger17_leg == "More then" and ScriptSettings.trigger17_amount < message.Amount) or (ScriptSettings.trigger17_leg == "Equals" and ScriptSettings.trigger17_amount == message.Amount) or (ScriptSettings.trigger17_leg == "Less then" and ScriptSettings.trigger17_amount > message.Amount)):
        parseMessage(ScriptSettings.trigger17_discordmsg, message.Name, message.Amount, message.Message)
    if ScriptSettings.trigger18_type == "Bits" and ((ScriptSettings.trigger18_leg == "More then" and ScriptSettings.trigger18_amount < message.Amount) or (ScriptSettings.trigger18_leg == "Equals" and ScriptSettings.trigger18_amount == message.Amount) or (ScriptSettings.trigger18_leg == "Less then" and ScriptSettings.trigger18_amount > message.Amount)):
        parseMessage(ScriptSettings.trigger18_discordmsg, message.Name, message.Amount, message.Message)
    if ScriptSettings.trigger19_type == "Bits" and ((ScriptSettings.trigger19_leg == "More then" and ScriptSettings.trigger19_amount < message.Amount) or (ScriptSettings.trigger19_leg == "Equals" and ScriptSettings.trigger19_amount == message.Amount) or (ScriptSettings.trigger19_leg == "Less then" and ScriptSettings.trigger19_amount > message.Amount)):
        parseMessage(ScriptSettings.trigger19_discordmsg, message.Name, message.Amount, message.Message)
    if ScriptSettings.trigger20_type == "Bits" and ((ScriptSettings.trigger20_leg == "More then" and ScriptSettings.trigger20_amount < message.Amount) or (ScriptSettings.trigger20_leg == "Equals" and ScriptSettings.trigger20_amount == message.Amount) or (ScriptSettings.trigger20_leg == "Less then" and ScriptSettings.trigger20_amount > message.Amount)):
        parseMessage(ScriptSettings.trigger20_discordmsg, message.Name, message.Amount, message.Message)
    return

def parseHost(message):
    global ScriptSettings
    if ScriptSettings.debug:
        Parent.Log("HostMessage", "IsLive: {0}".format(message.IsLive))
        Parent.Log("HostMessage", "IsRepeat: {0}".format(message.IsRepeat))
        Parent.Log("HostMessage", "IsTest: {0}".format(message.IsTest))
        Parent.Log("HostMessage", "Name: {0}".format(message.Name))
        Parent.Log("HostMessage", "Viewers: {0}".format(message.Viewers))
        Parent.SendDiscordMessage("Debug host message")
    if ScriptSettings.trigger1_type == "Host" and ((ScriptSettings.trigger1_leg == "More then" and ScriptSettings.trigger1_amount < message.Viewers) or (ScriptSettings.trigger1_leg == "Equals" and ScriptSettings.trigger1_amount == message.Viewers) or (ScriptSettings.trigger1_leg == "Less then" and ScriptSettings.trigger1_amount > message.Viewers)):
        parseMessage(ScriptSettings.trigger1_discordmsg, message.Name, message.Viewers, "")
    if ScriptSettings.trigger2_type == "Host" and ((ScriptSettings.trigger2_leg == "More then" and ScriptSettings.trigger2_amount < message.Viewers) or (ScriptSettings.trigger2_leg == "Equals" and ScriptSettings.trigger2_amount == message.Viewers) or (ScriptSettings.trigger2_leg == "Less then" and ScriptSettings.trigger2_amount > message.Viewers)):
        parseMessage(ScriptSettings.trigger2_discordmsg, message.Name, message.Viewers, "")
    if ScriptSettings.trigger3_type == "Host" and ((ScriptSettings.trigger3_leg == "More then" and ScriptSettings.trigger3_amount < message.Viewers) or (ScriptSettings.trigger3_leg == "Equals" and ScriptSettings.trigger3_amount == message.Viewers) or (ScriptSettings.trigger3_leg == "Less then" and ScriptSettings.trigger3_amount > message.Viewers)):
        parseMessage(ScriptSettings.trigger3_discordmsg, message.Name, message.Viewers, "")
    if ScriptSettings.trigger4_type == "Host" and ((ScriptSettings.trigger4_leg == "More then" and ScriptSettings.trigger4_amount < message.Viewers) or (ScriptSettings.trigger4_leg == "Equals" and ScriptSettings.trigger4_amount == message.Viewers) or (ScriptSettings.trigger4_leg == "Less then" and ScriptSettings.trigger4_amount > message.Viewers)):
        parseMessage(ScriptSettings.trigger4_discordmsg, message.Name, message.Viewers, "")
    if ScriptSettings.trigger5_type == "Host" and ((ScriptSettings.trigger5_leg == "More then" and ScriptSettings.trigger5_amount < message.Viewers) or (ScriptSettings.trigger5_leg == "Equals" and ScriptSettings.trigger5_amount == message.Viewers) or (ScriptSettings.trigger5_leg == "Less then" and ScriptSettings.trigger5_amount > message.Viewers)):
        parseMessage(ScriptSettings.trigger5_discordmsg, message.Name, message.Viewers, "")
    if ScriptSettings.trigger6_type == "Host" and ((ScriptSettings.trigger6_leg == "More then" and ScriptSettings.trigger6_amount < message.Viewers) or (ScriptSettings.trigger6_leg == "Equals" and ScriptSettings.trigger6_amount == message.Viewers) or (ScriptSettings.trigger6_leg == "Less then" and ScriptSettings.trigger6_amount > message.Viewers)):
        parseMessage(ScriptSettings.trigger6_discordmsg, message.Name, message.Viewers, "")
    if ScriptSettings.trigger7_type == "Host" and ((ScriptSettings.trigger7_leg == "More then" and ScriptSettings.trigger7_amount < message.Viewers) or (ScriptSettings.trigger7_leg == "Equals" and ScriptSettings.trigger7_amount == message.Viewers) or (ScriptSettings.trigger7_leg == "Less then" and ScriptSettings.trigger7_amount > message.Viewers)):
        parseMessage(ScriptSettings.trigger7_discordmsg, message.Name, message.Viewers, "")
    if ScriptSettings.trigger8_type == "Host" and ((ScriptSettings.trigger8_leg == "More then" and ScriptSettings.trigger8_amount < message.Viewers) or (ScriptSettings.trigger8_leg == "Equals" and ScriptSettings.trigger8_amount == message.Viewers) or (ScriptSettings.trigger8_leg == "Less then" and ScriptSettings.trigger8_amount > message.Viewers)):
        parseMessage(ScriptSettings.trigger8_discordmsg, message.Name, message.Viewers, "")
    if ScriptSettings.trigger9_type == "Host" and ((ScriptSettings.trigger9_leg == "More then" and ScriptSettings.trigger9_amount < message.Viewers) or (ScriptSettings.trigger9_leg == "Equals" and ScriptSettings.trigger9_amount == message.Viewers) or (ScriptSettings.trigger9_leg == "Less then" and ScriptSettings.trigger9_amount > message.Viewers)):
        parseMessage(ScriptSettings.trigger9_discordmsg, message.Name, message.Viewers, "")
    if ScriptSettings.trigger10_type == "Host" and ((ScriptSettings.trigger10_leg == "More then" and ScriptSettings.trigger10_amount < message.Viewers) or (ScriptSettings.trigger10_leg == "Equals" and ScriptSettings.trigger10_amount == message.Viewers) or (ScriptSettings.trigger10_leg == "Less then" and ScriptSettings.trigger10_amount > message.Viewers)):
        parseMessage(ScriptSettings.trigger10_discordmsg, message.Name, message.Viewers, "")
    if ScriptSettings.trigger11_type == "Host" and ((ScriptSettings.trigger11_leg == "More then" and ScriptSettings.trigger11_amount < message.Viewers) or (ScriptSettings.trigger11_leg == "Equals" and ScriptSettings.trigger11_amount == message.Viewers) or (ScriptSettings.trigger11_leg == "Less then" and ScriptSettings.trigger11_amount > message.Viewers)):
        parseMessage(ScriptSettings.trigger11_discordmsg, message.Name, message.Viewers, "")
    if ScriptSettings.trigger12_type == "Host" and ((ScriptSettings.trigger12_leg == "More then" and ScriptSettings.trigger12_amount < message.Viewers) or (ScriptSettings.trigger12_leg == "Equals" and ScriptSettings.trigger12_amount == message.Viewers) or (ScriptSettings.trigger12_leg == "Less then" and ScriptSettings.trigger12_amount > message.Viewers)):
        parseMessage(ScriptSettings.trigger12_discordmsg, message.Name, message.Viewers, "")
    if ScriptSettings.trigger13_type == "Host" and ((ScriptSettings.trigger13_leg == "More then" and ScriptSettings.trigger13_amount < message.Viewers) or (ScriptSettings.trigger13_leg == "Equals" and ScriptSettings.trigger13_amount == message.Viewers) or (ScriptSettings.trigger13_leg == "Less then" and ScriptSettings.trigger13_amount > message.Viewers)):
        parseMessage(ScriptSettings.trigger13_discordmsg, message.Name, message.Viewers, "")
    if ScriptSettings.trigger14_type == "Host" and ((ScriptSettings.trigger14_leg == "More then" and ScriptSettings.trigger14_amount < message.Viewers) or (ScriptSettings.trigger14_leg == "Equals" and ScriptSettings.trigger14_amount == message.Viewers) or (ScriptSettings.trigger14_leg == "Less then" and ScriptSettings.trigger14_amount > message.Viewers)):
        parseMessage(ScriptSettings.trigger14_discordmsg, message.Name, message.Viewers, "")
    if ScriptSettings.trigger15_type == "Host" and ((ScriptSettings.trigger15_leg == "More then" and ScriptSettings.trigger15_amount < message.Viewers) or (ScriptSettings.trigger15_leg == "Equals" and ScriptSettings.trigger15_amount == message.Viewers) or (ScriptSettings.trigger15_leg == "Less then" and ScriptSettings.trigger15_amount > message.Viewers)):
        parseMessage(ScriptSettings.trigger15_discordmsg, message.Name, message.Viewers, "")
    if ScriptSettings.trigger16_type == "Host" and ((ScriptSettings.trigger16_leg == "More then" and ScriptSettings.trigger16_amount < message.Viewers) or (ScriptSettings.trigger16_leg == "Equals" and ScriptSettings.trigger16_amount == message.Viewers) or (ScriptSettings.trigger16_leg == "Less then" and ScriptSettings.trigger16_amount > message.Viewers)):
        parseMessage(ScriptSettings.trigger16_discordmsg, message.Name, message.Viewers, "")
    if ScriptSettings.trigger17_type == "Host" and ((ScriptSettings.trigger17_leg == "More then" and ScriptSettings.trigger17_amount < message.Viewers) or (ScriptSettings.trigger17_leg == "Equals" and ScriptSettings.trigger17_amount == message.Viewers) or (ScriptSettings.trigger17_leg == "Less then" and ScriptSettings.trigger17_amount > message.Viewers)):
        parseMessage(ScriptSettings.trigger17_discordmsg, message.Name, message.Viewers, "")
    if ScriptSettings.trigger18_type == "Host" and ((ScriptSettings.trigger18_leg == "More then" and ScriptSettings.trigger18_amount < message.Viewers) or (ScriptSettings.trigger18_leg == "Equals" and ScriptSettings.trigger18_amount == message.Viewers) or (ScriptSettings.trigger18_leg == "Less then" and ScriptSettings.trigger18_amount > message.Viewers)):
        parseMessage(ScriptSettings.trigger18_discordmsg, message.Name, message.Viewers, "")
    if ScriptSettings.trigger19_type == "Host" and ((ScriptSettings.trigger19_leg == "More then" and ScriptSettings.trigger19_amount < message.Viewers) or (ScriptSettings.trigger19_leg == "Equals" and ScriptSettings.trigger19_amount == message.Viewers) or (ScriptSettings.trigger19_leg == "Less then" and ScriptSettings.trigger19_amount > message.Viewers)):
        parseMessage(ScriptSettings.trigger19_discordmsg, message.Name, message.Viewers, "")
    if ScriptSettings.trigger20_type == "Host" and ((ScriptSettings.trigger20_leg == "More then" and ScriptSettings.trigger20_amount < message.Viewers) or (ScriptSettings.trigger20_leg == "Equals" and ScriptSettings.trigger20_amount == message.Viewers) or (ScriptSettings.trigger20_leg == "Less then" and ScriptSettings.trigger20_amount > message.Viewers)):
        parseMessage(ScriptSettings.trigger20_discordmsg, message.Name, message.Viewers, "")
    return

def parseRaid(message):
    global ScriptSettings
    if ScriptSettings.debug:
        Parent.Log("RaidMessage", "IsLive: {0}".format(message.IsLive))
        Parent.Log("RaidMessage", "IsRepeat: {0}".format(message.IsRepeat))
        Parent.Log("RaidMessage", "IsTest: {0}".format(message.IsTest))
        Parent.Log("RaidMessage", "Name: {0}".format(message.Name))
        Parent.Log("RaidMessage", "Raiders: {0}".format(message.Raiders))
        Parent.SendDiscordMessage("Debug raid message")
    if ScriptSettings.trigger1_type == "Raid" and ((ScriptSettings.trigger1_leg == "More then" and ScriptSettings.trigger1_amount < message.Raiders) or (ScriptSettings.trigger1_leg == "Equals" and ScriptSettings.trigger1_amount == message.Raiders) or (ScriptSettings.trigger1_leg == "Less then" and ScriptSettings.trigger1_amount > message.Raiders)):
        parseMessage(ScriptSettings.trigger1_discordmsg, message.Name, message.Raiders, "")
    if ScriptSettings.trigger2_type == "Raid" and ((ScriptSettings.trigger2_leg == "More then" and ScriptSettings.trigger2_amount < message.Raiders) or (ScriptSettings.trigger2_leg == "Equals" and ScriptSettings.trigger2_amount == message.Raiders) or (ScriptSettings.trigger2_leg == "Less then" and ScriptSettings.trigger2_amount > message.Raiders)):
        parseMessage(ScriptSettings.trigger2_discordmsg, message.Name, message.Raiders, "")
    if ScriptSettings.trigger3_type == "Raid" and ((ScriptSettings.trigger3_leg == "More then" and ScriptSettings.trigger3_amount < message.Raiders) or (ScriptSettings.trigger3_leg == "Equals" and ScriptSettings.trigger3_amount == message.Raiders) or (ScriptSettings.trigger3_leg == "Less then" and ScriptSettings.trigger3_amount > message.Raiders)):
        parseMessage(ScriptSettings.trigger3_discordmsg, message.Name, message.Raiders, "")
    if ScriptSettings.trigger4_type == "Raid" and ((ScriptSettings.trigger4_leg == "More then" and ScriptSettings.trigger4_amount < message.Raiders) or (ScriptSettings.trigger4_leg == "Equals" and ScriptSettings.trigger4_amount == message.Raiders) or (ScriptSettings.trigger4_leg == "Less then" and ScriptSettings.trigger4_amount > message.Raiders)):
        parseMessage(ScriptSettings.trigger4_discordmsg, message.Name, message.Raiders, "")
    if ScriptSettings.trigger5_type == "Raid" and ((ScriptSettings.trigger5_leg == "More then" and ScriptSettings.trigger5_amount < message.Raiders) or (ScriptSettings.trigger5_leg == "Equals" and ScriptSettings.trigger5_amount == message.Raiders) or (ScriptSettings.trigger5_leg == "Less then" and ScriptSettings.trigger5_amount > message.Raiders)):
        parseMessage(ScriptSettings.trigger5_discordmsg, message.Name, message.Raiders, "")
    if ScriptSettings.trigger6_type == "Raid" and ((ScriptSettings.trigger6_leg == "More then" and ScriptSettings.trigger6_amount < message.Raiders) or (ScriptSettings.trigger6_leg == "Equals" and ScriptSettings.trigger6_amount == message.Raiders) or (ScriptSettings.trigger6_leg == "Less then" and ScriptSettings.trigger6_amount > message.Raiders)):
        parseMessage(ScriptSettings.trigger6_discordmsg, message.Name, message.Raiders, "")
    if ScriptSettings.trigger7_type == "Raid" and ((ScriptSettings.trigger7_leg == "More then" and ScriptSettings.trigger7_amount < message.Raiders) or (ScriptSettings.trigger7_leg == "Equals" and ScriptSettings.trigger7_amount == message.Raiders) or (ScriptSettings.trigger7_leg == "Less then" and ScriptSettings.trigger7_amount > message.Raiders)):
        parseMessage(ScriptSettings.trigger7_discordmsg, message.Name, message.Raiders, "")
    if ScriptSettings.trigger8_type == "Raid" and ((ScriptSettings.trigger8_leg == "More then" and ScriptSettings.trigger8_amount < message.Raiders) or (ScriptSettings.trigger8_leg == "Equals" and ScriptSettings.trigger8_amount == message.Raiders) or (ScriptSettings.trigger8_leg == "Less then" and ScriptSettings.trigger8_amount > message.Raiders)):
        parseMessage(ScriptSettings.trigger8_discordmsg, message.Name, message.Raiders, "")
    if ScriptSettings.trigger9_type == "Raid" and ((ScriptSettings.trigger9_leg == "More then" and ScriptSettings.trigger9_amount < message.Raiders) or (ScriptSettings.trigger9_leg == "Equals" and ScriptSettings.trigger9_amount == message.Raiders) or (ScriptSettings.trigger9_leg == "Less then" and ScriptSettings.trigger9_amount > message.Raiders)):
        parseMessage(ScriptSettings.trigger9_discordmsg, message.Name, message.Raiders, "")
    if ScriptSettings.trigger10_type == "Raid" and ((ScriptSettings.trigger10_leg == "More then" and ScriptSettings.trigger10_amount < message.Raiders) or (ScriptSettings.trigger10_leg == "Equals" and ScriptSettings.trigger10_amount == message.Raiders) or (ScriptSettings.trigger10_leg == "Less then" and ScriptSettings.trigger10_amount > message.Raiders)):
        parseMessage(ScriptSettings.trigger10_discordmsg, message.Name, message.Raiders, "")
    if ScriptSettings.trigger11_type == "Raid" and ((ScriptSettings.trigger11_leg == "More then" and ScriptSettings.trigger11_amount < message.Raiders) or (ScriptSettings.trigger11_leg == "Equals" and ScriptSettings.trigger11_amount == message.Raiders) or (ScriptSettings.trigger11_leg == "Less then" and ScriptSettings.trigger11_amount > message.Raiders)):
        parseMessage(ScriptSettings.trigger11_discordmsg, message.Name, message.Raiders, "")
    if ScriptSettings.trigger12_type == "Raid" and ((ScriptSettings.trigger12_leg == "More then" and ScriptSettings.trigger12_amount < message.Raiders) or (ScriptSettings.trigger12_leg == "Equals" and ScriptSettings.trigger12_amount == message.Raiders) or (ScriptSettings.trigger12_leg == "Less then" and ScriptSettings.trigger12_amount > message.Raiders)):
        parseMessage(ScriptSettings.trigger12_discordmsg, message.Name, message.Raiders, "")
    if ScriptSettings.trigger13_type == "Raid" and ((ScriptSettings.trigger13_leg == "More then" and ScriptSettings.trigger13_amount < message.Raiders) or (ScriptSettings.trigger13_leg == "Equals" and ScriptSettings.trigger13_amount == message.Raiders) or (ScriptSettings.trigger13_leg == "Less then" and ScriptSettings.trigger13_amount > message.Raiders)):
        parseMessage(ScriptSettings.trigger13_discordmsg, message.Name, message.Raiders, "")
    if ScriptSettings.trigger14_type == "Raid" and ((ScriptSettings.trigger14_leg == "More then" and ScriptSettings.trigger14_amount < message.Raiders) or (ScriptSettings.trigger14_leg == "Equals" and ScriptSettings.trigger14_amount == message.Raiders) or (ScriptSettings.trigger14_leg == "Less then" and ScriptSettings.trigger14_amount > message.Raiders)):
        parseMessage(ScriptSettings.trigger14_discordmsg, message.Name, message.Raiders, "")
    if ScriptSettings.trigger15_type == "Raid" and ((ScriptSettings.trigger15_leg == "More then" and ScriptSettings.trigger15_amount < message.Raiders) or (ScriptSettings.trigger15_leg == "Equals" and ScriptSettings.trigger15_amount == message.Raiders) or (ScriptSettings.trigger15_leg == "Less then" and ScriptSettings.trigger15_amount > message.Raiders)):
        parseMessage(ScriptSettings.trigger15_discordmsg, message.Name, message.Raiders, "")
    if ScriptSettings.trigger16_type == "Raid" and ((ScriptSettings.trigger16_leg == "More then" and ScriptSettings.trigger16_amount < message.Raiders) or (ScriptSettings.trigger16_leg == "Equals" and ScriptSettings.trigger16_amount == message.Raiders) or (ScriptSettings.trigger16_leg == "Less then" and ScriptSettings.trigger16_amount > message.Raiders)):
        parseMessage(ScriptSettings.trigger16_discordmsg, message.Name, message.Raiders, "")
    if ScriptSettings.trigger17_type == "Raid" and ((ScriptSettings.trigger17_leg == "More then" and ScriptSettings.trigger17_amount < message.Raiders) or (ScriptSettings.trigger17_leg == "Equals" and ScriptSettings.trigger17_amount == message.Raiders) or (ScriptSettings.trigger17_leg == "Less then" and ScriptSettings.trigger17_amount > message.Raiders)):
        parseMessage(ScriptSettings.trigger17_discordmsg, message.Name, message.Raiders, "")
    if ScriptSettings.trigger18_type == "Raid" and ((ScriptSettings.trigger18_leg == "More then" and ScriptSettings.trigger18_amount < message.Raiders) or (ScriptSettings.trigger18_leg == "Equals" and ScriptSettings.trigger18_amount == message.Raiders) or (ScriptSettings.trigger18_leg == "Less then" and ScriptSettings.trigger18_amount > message.Raiders)):
        parseMessage(ScriptSettings.trigger18_discordmsg, message.Name, message.Raiders, "")
    if ScriptSettings.trigger19_type == "Raid" and ((ScriptSettings.trigger19_leg == "More then" and ScriptSettings.trigger19_amount < message.Raiders) or (ScriptSettings.trigger19_leg == "Equals" and ScriptSettings.trigger19_amount == message.Raiders) or (ScriptSettings.trigger19_leg == "Less then" and ScriptSettings.trigger19_amount > message.Raiders)):
        parseMessage(ScriptSettings.trigger19_discordmsg, message.Name, message.Raiders, "")
    if ScriptSettings.trigger20_type == "Raid" and ((ScriptSettings.trigger20_leg == "More then" and ScriptSettings.trigger20_amount < message.Raiders) or (ScriptSettings.trigger20_leg == "Equals" and ScriptSettings.trigger20_amount == message.Raiders) or (ScriptSettings.trigger20_leg == "Less then" and ScriptSettings.trigger20_amount > message.Raiders)):
        parseMessage(ScriptSettings.trigger20_discordmsg, message.Name, message.Raiders, "")
    return

def parseSub(message):
    global ScriptSettings
    if ScriptSettings.debug:
        Parent.Log("SubscriptionMessage", "DisplayName: {0}".format(message.DisplayName))
        Parent.Log("SubscriptionMessage", "Gifter: {0}".format(message.Gifter))
        Parent.Log("SubscriptionMessage", "IsLive: {0}".format(message.IsLive))
        Parent.Log("SubscriptionMessage", "IsRepeat: {0}".format(message.IsRepeat))
        Parent.Log("SubscriptionMessage", "IsTest: {0}".format(message.IsTest))
        Parent.Log("SubscriptionMessage", "Message: {0}".format(message.Messsage))
        Parent.Log("SubscriptionMessage", "Months: {0}".format(message.Months))
        Parent.Log("SubscriptionMessage", "Name: {0}".format(message.Name))
        Parent.Log("SubscriptionMessage", "StreakMonths: {0}".format(message.StreakMonths))
        Parent.Log("SubscriptionMessage", "SubPlan: {0}".format(message.SubPlan))
        Parent.Log("SubscriptionMessage", "SubPlanName: {0}".format(message.SubPlanName))
        Parent.Log("SubscriptionMessage", "SubType: {0}".format(message.SubType))
        Parent.SendDiscordMessage("Debug subscription message")
    if (ScriptSettings.trigger1_type == "Subscription" or ScriptSettings.trigger1_type == "Subscription & resub") and ((ScriptSettings.trigger1_leg == "More then" and ScriptSettings.trigger1_amount < message.Months) or (ScriptSettings.trigger1_leg == "Equals" and ScriptSettings.trigger1_amount == message.Months) or (ScriptSettings.trigger1_leg == "Less then" and ScriptSettings.trigger1_amount > message.Months)):
        parseMessage(ScriptSettings.trigger1_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger2_type == "Subscription" or ScriptSettings.trigger2_type == "Subscription & resub") and ((ScriptSettings.trigger2_leg == "More then" and ScriptSettings.trigger2_amount < message.Months) or (ScriptSettings.trigger2_leg == "Equals" and ScriptSettings.trigger2_amount == message.Months) or (ScriptSettings.trigger2_leg == "Less then" and ScriptSettings.trigger2_amount > message.Months)):
        parseMessage(ScriptSettings.trigger2_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger3_type == "Subscription" or ScriptSettings.trigger3_type == "Subscription & resub") and ((ScriptSettings.trigger3_leg == "More then" and ScriptSettings.trigger3_amount < message.Months) or (ScriptSettings.trigger3_leg == "Equals" and ScriptSettings.trigger3_amount == message.Months) or (ScriptSettings.trigger3_leg == "Less then" and ScriptSettings.trigger3_amount > message.Months)):
        parseMessage(ScriptSettings.trigger3_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger4_type == "Subscription" or ScriptSettings.trigger4_type == "Subscription & resub") and ((ScriptSettings.trigger4_leg == "More then" and ScriptSettings.trigger4_amount < message.Months) or (ScriptSettings.trigger4_leg == "Equals" and ScriptSettings.trigger4_amount == message.Months) or (ScriptSettings.trigger4_leg == "Less then" and ScriptSettings.trigger4_amount > message.Months)):
        parseMessage(ScriptSettings.trigger4_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger5_type == "Subscription" or ScriptSettings.trigger5_type == "Subscription & resub") and ((ScriptSettings.trigger5_leg == "More then" and ScriptSettings.trigger5_amount < message.Months) or (ScriptSettings.trigger5_leg == "Equals" and ScriptSettings.trigger5_amount == message.Months) or (ScriptSettings.trigger5_leg == "Less then" and ScriptSettings.trigger5_amount > message.Months)):
        parseMessage(ScriptSettings.trigger5_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger6_type == "Subscription" or ScriptSettings.trigger6_type == "Subscription & resub") and ((ScriptSettings.trigger6_leg == "More then" and ScriptSettings.trigger6_amount < message.Months) or (ScriptSettings.trigger6_leg == "Equals" and ScriptSettings.trigger6_amount == message.Months) or (ScriptSettings.trigger6_leg == "Less then" and ScriptSettings.trigger6_amount > message.Months)):
        parseMessage(ScriptSettings.trigger6_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger7_type == "Subscription" or ScriptSettings.trigger7_type == "Subscription & resub") and ((ScriptSettings.trigger7_leg == "More then" and ScriptSettings.trigger7_amount < message.Months) or (ScriptSettings.trigger7_leg == "Equals" and ScriptSettings.trigger7_amount == message.Months) or (ScriptSettings.trigger7_leg == "Less then" and ScriptSettings.trigger7_amount > message.Months)):
        parseMessage(ScriptSettings.trigger7_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger8_type == "Subscription" or ScriptSettings.trigger8_type == "Subscription & resub") and ((ScriptSettings.trigger8_leg == "More then" and ScriptSettings.trigger8_amount < message.Months) or (ScriptSettings.trigger8_leg == "Equals" and ScriptSettings.trigger8_amount == message.Months) or (ScriptSettings.trigger8_leg == "Less then" and ScriptSettings.trigger8_amount > message.Months)):
        parseMessage(ScriptSettings.trigger8_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger9_type == "Subscription" or ScriptSettings.trigger9_type == "Subscription & resub") and ((ScriptSettings.trigger9_leg == "More then" and ScriptSettings.trigger9_amount < message.Months) or (ScriptSettings.trigger9_leg == "Equals" and ScriptSettings.trigger9_amount == message.Months) or (ScriptSettings.trigger9_leg == "Less then" and ScriptSettings.trigger9_amount > message.Months)):
        parseMessage(ScriptSettings.trigger9_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger100_type == "Subscription" or ScriptSettings.trigger10_type == "Subscription & resub") and ((ScriptSettings.trigger10_leg == "More then" and ScriptSettings.trigger10_amount < message.Months) or (ScriptSettings.trigger10_leg == "Equals" and ScriptSettings.trigger10_amount == message.Months) or (ScriptSettings.trigger10_leg == "Less then" and ScriptSettings.trigger10_amount > message.Months)):
        parseMessage(ScriptSettings.trigger100_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger11_type == "Subscription" or ScriptSettings.trigger11_type == "Subscription & resub") and ((ScriptSettings.trigger11_leg == "More then" and ScriptSettings.trigger11_amount < message.Months) or (ScriptSettings.trigger11_leg == "Equals" and ScriptSettings.trigger11_amount == message.Months) or (ScriptSettings.trigger11_leg == "Less then" and ScriptSettings.trigger11_amount > message.Months)):
        parseMessage(ScriptSettings.trigger11_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger12_type == "Subscription" or ScriptSettings.trigger12_type == "Subscription & resub") and ((ScriptSettings.trigger12_leg == "More then" and ScriptSettings.trigger12_amount < message.Months) or (ScriptSettings.trigger12_leg == "Equals" and ScriptSettings.trigger12_amount == message.Months) or (ScriptSettings.trigger12_leg == "Less then" and ScriptSettings.trigger12_amount > message.Months)):
        parseMessage(ScriptSettings.trigger12_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger13_type == "Subscription" or ScriptSettings.trigger13_type == "Subscription & resub") and ((ScriptSettings.trigger13_leg == "More then" and ScriptSettings.trigger13_amount < message.Months) or (ScriptSettings.trigger13_leg == "Equals" and ScriptSettings.trigger13_amount == message.Months) or (ScriptSettings.trigger13_leg == "Less then" and ScriptSettings.trigger13_amount > message.Months)):
        parseMessage(ScriptSettings.trigger13_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger14_type == "Subscription" or ScriptSettings.trigger14_type == "Subscription & resub") and ((ScriptSettings.trigger14_leg == "More then" and ScriptSettings.trigger14_amount < message.Months) or (ScriptSettings.trigger14_leg == "Equals" and ScriptSettings.trigger14_amount == message.Months) or (ScriptSettings.trigger14_leg == "Less then" and ScriptSettings.trigger14_amount > message.Months)):
        parseMessage(ScriptSettings.trigger14_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger15_type == "Subscription" or ScriptSettings.trigger15_type == "Subscription & resub") and ((ScriptSettings.trigger15_leg == "More then" and ScriptSettings.trigger15_amount < message.Months) or (ScriptSettings.trigger15_leg == "Equals" and ScriptSettings.trigger15_amount == message.Months) or (ScriptSettings.trigger15_leg == "Less then" and ScriptSettings.trigger15_amount > message.Months)):
        parseMessage(ScriptSettings.trigger15_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger16_type == "Subscription" or ScriptSettings.trigger16_type == "Subscription & resub") and ((ScriptSettings.trigger16_leg == "More then" and ScriptSettings.trigger16_amount < message.Months) or (ScriptSettings.trigger16_leg == "Equals" and ScriptSettings.trigger16_amount == message.Months) or (ScriptSettings.trigger16_leg == "Less then" and ScriptSettings.trigger16_amount > message.Months)):
        parseMessage(ScriptSettings.trigger16_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger17_type == "Subscription" or ScriptSettings.trigger17_type == "Subscription & resub") and ((ScriptSettings.trigger17_leg == "More then" and ScriptSettings.trigger17_amount < message.Months) or (ScriptSettings.trigger17_leg == "Equals" and ScriptSettings.trigger17_amount == message.Months) or (ScriptSettings.trigger17_leg == "Less then" and ScriptSettings.trigger17_amount > message.Months)):
        parseMessage(ScriptSettings.trigger17_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger18_type == "Subscription" or ScriptSettings.trigger18_type == "Subscription & resub") and ((ScriptSettings.trigger18_leg == "More then" and ScriptSettings.trigger18_amount < message.Months) or (ScriptSettings.trigger18_leg == "Equals" and ScriptSettings.trigger18_amount == message.Months) or (ScriptSettings.trigger18_leg == "Less then" and ScriptSettings.trigger18_amount > message.Months)):
        parseMessage(ScriptSettings.trigger18_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger19_type == "Subscription" or ScriptSettings.trigger19_type == "Subscription & resub") and ((ScriptSettings.trigger19_leg == "More then" and ScriptSettings.trigger19_amount < message.Months) or (ScriptSettings.trigger19_leg == "Equals" and ScriptSettings.trigger19_amount == message.Months) or (ScriptSettings.trigger19_leg == "Less then" and ScriptSettings.trigger19_amount > message.Months)):
        parseMessage(ScriptSettings.trigger19_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger20_type == "Subscription" or ScriptSettings.trigger20_type == "Subscription & resub") and ((ScriptSettings.trigger20_leg == "More then" and ScriptSettings.trigger20_amount < message.Months) or (ScriptSettings.trigger20_leg == "Equals" and ScriptSettings.trigger20_amount == message.Months) or (ScriptSettings.trigger20_leg == "Less then" and ScriptSettings.trigger20_amount > message.Months)):
        parseMessage(ScriptSettings.trigger20_discordmsg, message.Name, message.Months, "")
    return

def parseResub(message):
    global ScriptSettings
    if ScriptSettings.debug:
        Parent.Log("ReSubMessage", "DisplayName: {0}".format(message.DisplayName))
        Parent.Log("ReSubMessage", "Gifter: {0}".format(message.Gifter))
        Parent.Log("ReSubMessage", "IsLive: {0}".format(message.IsLive))
        Parent.Log("ReSubMessage", "IsRepeat: {0}".format(message.IsRepeat))
        Parent.Log("ReSubMessage", "IsTest: {0}".format(message.IsTest))
        Parent.Log("ReSubMessage", "Message: {0}".format(message.Messsage))
        Parent.Log("ReSubMessage", "Months: {0}".format(message.Months))
        Parent.Log("ReSubMessage", "Name: {0}".format(message.Name))
        Parent.Log("ReSubMessage", "StreakMonths: {0}".format(message.StreakMonths))
        Parent.Log("ReSubMessage", "SubPlan: {0}".format(message.SubPlan))
        Parent.Log("ReSubMessage", "SubPlanName: {0}".format(message.SubPlanName))
        Parent.Log("ReSubMessage", "SubType: {0}".format(message.SubType))
        Parent.SendDiscordMessage("Debug resub message")
    if (ScriptSettings.trigger1_type == "Resub" or ScriptSettings.trigger1_type == "Subscription & resub") and ((ScriptSettings.trigger1_leg == "More then" and ScriptSettings.trigger1_amount < message.Months) or (ScriptSettings.trigger1_leg == "Equals" and ScriptSettings.trigger1_amount == message.Months) or (ScriptSettings.trigger1_leg == "Less then" and ScriptSettings.trigger1_amount > message.Months)):
        parseMessage(ScriptSettings.trigger1_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger2_type == "Resub" or ScriptSettings.trigger2_type == "Subscription & resub") and ((ScriptSettings.trigger2_leg == "More then" and ScriptSettings.trigger2_amount < message.Months) or (ScriptSettings.trigger2_leg == "Equals" and ScriptSettings.trigger2_amount == message.Months) or (ScriptSettings.trigger2_leg == "Less then" and ScriptSettings.trigger2_amount > message.Months)):
        parseMessage(ScriptSettings.trigger2_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger3_type == "Resub" or ScriptSettings.trigger3_type == "Subscription & resub") and ((ScriptSettings.trigger3_leg == "More then" and ScriptSettings.trigger3_amount < message.Months) or (ScriptSettings.trigger3_leg == "Equals" and ScriptSettings.trigger3_amount == message.Months) or (ScriptSettings.trigger3_leg == "Less then" and ScriptSettings.trigger3_amount > message.Months)):
        parseMessage(ScriptSettings.trigger3_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger4_type == "Resub" or ScriptSettings.trigger4_type == "Subscription & resub") and ((ScriptSettings.trigger4_leg == "More then" and ScriptSettings.trigger4_amount < message.Months) or (ScriptSettings.trigger4_leg == "Equals" and ScriptSettings.trigger4_amount == message.Months) or (ScriptSettings.trigger4_leg == "Less then" and ScriptSettings.trigger4_amount > message.Months)):
        parseMessage(ScriptSettings.trigger4_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger5_type == "Resub" or ScriptSettings.trigger5_type == "Subscription & resub") and ((ScriptSettings.trigger5_leg == "More then" and ScriptSettings.trigger5_amount < message.Months) or (ScriptSettings.trigger5_leg == "Equals" and ScriptSettings.trigger5_amount == message.Months) or (ScriptSettings.trigger5_leg == "Less then" and ScriptSettings.trigger5_amount > message.Months)):
        parseMessage(ScriptSettings.trigger5_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger6_type == "Resub" or ScriptSettings.trigger6_type == "Subscription & resub") and ((ScriptSettings.trigger6_leg == "More then" and ScriptSettings.trigger6_amount < message.Months) or (ScriptSettings.trigger6_leg == "Equals" and ScriptSettings.trigger6_amount == message.Months) or (ScriptSettings.trigger6_leg == "Less then" and ScriptSettings.trigger6_amount > message.Months)):
        parseMessage(ScriptSettings.trigger6_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger7_type == "Resub" or ScriptSettings.trigger7_type == "Subscription & resub") and ((ScriptSettings.trigger7_leg == "More then" and ScriptSettings.trigger7_amount < message.Months) or (ScriptSettings.trigger7_leg == "Equals" and ScriptSettings.trigger7_amount == message.Months) or (ScriptSettings.trigger7_leg == "Less then" and ScriptSettings.trigger7_amount > message.Months)):
        parseMessage(ScriptSettings.trigger7_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger8_type == "Resub" or ScriptSettings.trigger8_type == "Subscription & resub") and ((ScriptSettings.trigger8_leg == "More then" and ScriptSettings.trigger8_amount < message.Months) or (ScriptSettings.trigger8_leg == "Equals" and ScriptSettings.trigger8_amount == message.Months) or (ScriptSettings.trigger8_leg == "Less then" and ScriptSettings.trigger8_amount > message.Months)):
        parseMessage(ScriptSettings.trigger8_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger9_type == "Resub" or ScriptSettings.trigger9_type == "Subscription & resub") and ((ScriptSettings.trigger9_leg == "More then" and ScriptSettings.trigger9_amount < message.Months) or (ScriptSettings.trigger9_leg == "Equals" and ScriptSettings.trigger9_amount == message.Months) or (ScriptSettings.trigger9_leg == "Less then" and ScriptSettings.trigger9_amount > message.Months)):
        parseMessage(ScriptSettings.trigger9_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger100_type == "Resub" or ScriptSettings.trigger10_type == "Subscription & resub") and ((ScriptSettings.trigger10_leg == "More then" and ScriptSettings.trigger10_amount < message.Months) or (ScriptSettings.trigger10_leg == "Equals" and ScriptSettings.trigger10_amount == message.Months) or (ScriptSettings.trigger10_leg == "Less then" and ScriptSettings.trigger10_amount > message.Months)):
        parseMessage(ScriptSettings.trigger100_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger11_type == "Resub" or ScriptSettings.trigger11_type == "Subscription & resub") and ((ScriptSettings.trigger11_leg == "More then" and ScriptSettings.trigger11_amount < message.Months) or (ScriptSettings.trigger11_leg == "Equals" and ScriptSettings.trigger11_amount == message.Months) or (ScriptSettings.trigger11_leg == "Less then" and ScriptSettings.trigger11_amount > message.Months)):
        parseMessage(ScriptSettings.trigger11_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger12_type == "Resub" or ScriptSettings.trigger12_type == "Subscription & resub") and ((ScriptSettings.trigger12_leg == "More then" and ScriptSettings.trigger12_amount < message.Months) or (ScriptSettings.trigger12_leg == "Equals" and ScriptSettings.trigger12_amount == message.Months) or (ScriptSettings.trigger12_leg == "Less then" and ScriptSettings.trigger12_amount > message.Months)):
        parseMessage(ScriptSettings.trigger12_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger13_type == "Resub" or ScriptSettings.trigger13_type == "Subscription & resub") and ((ScriptSettings.trigger13_leg == "More then" and ScriptSettings.trigger13_amount < message.Months) or (ScriptSettings.trigger13_leg == "Equals" and ScriptSettings.trigger13_amount == message.Months) or (ScriptSettings.trigger13_leg == "Less then" and ScriptSettings.trigger13_amount > message.Months)):
        parseMessage(ScriptSettings.trigger13_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger14_type == "Resub" or ScriptSettings.trigger14_type == "Subscription & resub") and ((ScriptSettings.trigger14_leg == "More then" and ScriptSettings.trigger14_amount < message.Months) or (ScriptSettings.trigger14_leg == "Equals" and ScriptSettings.trigger14_amount == message.Months) or (ScriptSettings.trigger14_leg == "Less then" and ScriptSettings.trigger14_amount > message.Months)):
        parseMessage(ScriptSettings.trigger14_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger15_type == "Resub" or ScriptSettings.trigger15_type == "Subscription & resub") and ((ScriptSettings.trigger15_leg == "More then" and ScriptSettings.trigger15_amount < message.Months) or (ScriptSettings.trigger15_leg == "Equals" and ScriptSettings.trigger15_amount == message.Months) or (ScriptSettings.trigger15_leg == "Less then" and ScriptSettings.trigger15_amount > message.Months)):
        parseMessage(ScriptSettings.trigger15_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger16_type == "Resub" or ScriptSettings.trigger16_type == "Subscription & resub") and ((ScriptSettings.trigger16_leg == "More then" and ScriptSettings.trigger16_amount < message.Months) or (ScriptSettings.trigger16_leg == "Equals" and ScriptSettings.trigger16_amount == message.Months) or (ScriptSettings.trigger16_leg == "Less then" and ScriptSettings.trigger16_amount > message.Months)):
        parseMessage(ScriptSettings.trigger16_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger17_type == "Resub" or ScriptSettings.trigger17_type == "Subscription & resub") and ((ScriptSettings.trigger17_leg == "More then" and ScriptSettings.trigger17_amount < message.Months) or (ScriptSettings.trigger17_leg == "Equals" and ScriptSettings.trigger17_amount == message.Months) or (ScriptSettings.trigger17_leg == "Less then" and ScriptSettings.trigger17_amount > message.Months)):
        parseMessage(ScriptSettings.trigger17_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger18_type == "Resub" or ScriptSettings.trigger18_type == "Subscription & resub") and ((ScriptSettings.trigger18_leg == "More then" and ScriptSettings.trigger18_amount < message.Months) or (ScriptSettings.trigger18_leg == "Equals" and ScriptSettings.trigger18_amount == message.Months) or (ScriptSettings.trigger18_leg == "Less then" and ScriptSettings.trigger18_amount > message.Months)):
        parseMessage(ScriptSettings.trigger18_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger19_type == "Resub" or ScriptSettings.trigger19_type == "Subscription & resub") and ((ScriptSettings.trigger19_leg == "More then" and ScriptSettings.trigger19_amount < message.Months) or (ScriptSettings.trigger19_leg == "Equals" and ScriptSettings.trigger19_amount == message.Months) or (ScriptSettings.trigger19_leg == "Less then" and ScriptSettings.trigger19_amount > message.Months)):
        parseMessage(ScriptSettings.trigger19_discordmsg, message.Name, message.Months, "")
    if (ScriptSettings.trigger20_type == "Resub" or ScriptSettings.trigger20_type == "Subscription & resub") and ((ScriptSettings.trigger20_leg == "More then" and ScriptSettings.trigger20_amount < message.Months) or (ScriptSettings.trigger20_leg == "Equals" and ScriptSettings.trigger20_amount == message.Months) or (ScriptSettings.trigger20_leg == "Less then" and ScriptSettings.trigger20_amount > message.Months)):
        parseMessage(ScriptSettings.trigger20_discordmsg, message.Name, message.Months, "")
    return

def parseDonation(message):
    global ScriptSettings
    decAmount = Decimal(message.Amount)
    if ScriptSettings.debug:
        Parent.Log("Donation", "Amount: {0}".format(message.Amount))
        Parent.Log("Donation", "Currency: {0}".format(message.Currency))
        Parent.Log("Donation", "FormattedAmount: {0}".format(message.FormattedAmount))
        Parent.Log("Donation", "FromId: {0}".format(message.FromId))
        Parent.Log("Donation", "FromName: {0}".format(message.FromName))
        Parent.Log("Donation", "IsLive: {0}".format(message.IsLive))
        Parent.Log("Donation", "IsRepeat: {0}".format(message.IsRepeat))
        Parent.Log("Donation", "IsTest: {0}".format(message.IsTest))
        Parent.Log("Donation", "Message: {0}".format(message.Message))
        Parent.Log("Donation", "Name: {0}".format(message.Name))
        Parent.Log("Donation", "PaymentSource: {0}".format(message.PaymentSource))
        Parent.SendDiscordMessage("Debug donation message")
    #1
    if ScriptSettings.trigger1_amount == 0:
        decTriggerAmount = 0
    else:
        decTriggerAmount = Decimal(ScriptSettings.trigger1_amount)/100
    if ScriptSettings.trigger1_type == "Donation" and ((ScriptSettings.trigger1_leg == "More then" and decTriggerAmount < decAmount) or (ScriptSettings.trigger1_leg == "Equals" and decTriggerAmount == decAmount) or (ScriptSettings.trigger1_leg == "Less then" and decTriggerAmount > decAmount)):
        parseMessage(ScriptSettings.trigger1_discordmsg, message.Name, message.FormattedAmount, message.Currency)
    #2
    if ScriptSettings.trigger2_amount == 0:
        decTriggerAmount = 0
    else:
        decTriggerAmount = Decimal(ScriptSettings.trigger2_amount)/100
    if ScriptSettings.trigger2_type == "Donation" and ((ScriptSettings.trigger2_leg == "More then" and decTriggerAmount < decAmount) or (ScriptSettings.trigger2_leg == "Equals" and decTriggerAmount == decAmount) or (ScriptSettings.trigger2_leg == "Less then" and decTriggerAmount > decAmount)):
        parseMessage(ScriptSettings.trigger2_discordmsg, message.Name, message.FormattedAmount, message.Currency)
    #3
    if ScriptSettings.trigger3_amount == 0:
        decTriggerAmount = 0
    else:
        decTriggerAmount = Decimal(ScriptSettings.trigger3_amount)/100
    if ScriptSettings.trigger3_type == "Donation" and ((ScriptSettings.trigger3_leg == "More then" and decTriggerAmount < decAmount) or (ScriptSettings.trigger3_leg == "Equals" and decTriggerAmount == decAmount) or (ScriptSettings.trigger3_leg == "Less then" and decTriggerAmount > decAmount)):
        parseMessage(ScriptSettings.trigger3_discordmsg, message.Name, message.FormattedAmount, message.Currency)
    #4
    if ScriptSettings.trigger4_amount == 0:
        decTriggerAmount = 0
    else:
        decTriggerAmount = Decimal(ScriptSettings.trigger4_amount)/100
    if ScriptSettings.trigger4_type == "Donation" and ((ScriptSettings.trigger4_leg == "More then" and decTriggerAmount < decAmount) or (ScriptSettings.trigger4_leg == "Equals" and decTriggerAmount == decAmount) or (ScriptSettings.trigger4_leg == "Less then" and decTriggerAmount > decAmount)):
        parseMessage(ScriptSettings.trigger4_discordmsg, message.Name, message.FormattedAmount, message.Currency)
    #5
    if ScriptSettings.trigger5_amount == 0:
        decTriggerAmount = 0
    else:
        decTriggerAmount = Decimal(ScriptSettings.trigger5_amount)/100
    if ScriptSettings.trigger5_type == "Donation" and ((ScriptSettings.trigger5_leg == "More then" and decTriggerAmount < decAmount) or (ScriptSettings.trigger5_leg == "Equals" and decTriggerAmount == decAmount) or (ScriptSettings.trigger5_leg == "Less then" and decTriggerAmount > decAmount)):
        parseMessage(ScriptSettings.trigger5_discordmsg, message.Name, message.FormattedAmount, message.Currency)
    #6
    if ScriptSettings.trigger6_amount == 0:
        decTriggerAmount = 0
    else:
        decTriggerAmount = Decimal(ScriptSettings.trigger6_amount)/100
    if ScriptSettings.trigger6_type == "Donation" and ((ScriptSettings.trigger6_leg == "More then" and decTriggerAmount < decAmount) or (ScriptSettings.trigger6_leg == "Equals" and decTriggerAmount == decAmount) or (ScriptSettings.trigger6_leg == "Less then" and decTriggerAmount > decAmount)):
        parseMessage(ScriptSettings.trigger6_discordmsg, message.Name, message.FormattedAmount, message.Currency)
    #7
    if ScriptSettings.trigger7_amount == 0:
        decTriggerAmount = 0
    else:
        decTriggerAmount = Decimal(ScriptSettings.trigger7_amount)/100
    if ScriptSettings.trigger7_type == "Donation" and ((ScriptSettings.trigger7_leg == "More then" and decTriggerAmount < decAmount) or (ScriptSettings.trigger7_leg == "Equals" and decTriggerAmount == decAmount) or (ScriptSettings.trigger7_leg == "Less then" and decTriggerAmount > decAmount)):
        parseMessage(ScriptSettings.trigger7_discordmsg, message.Name, message.FormattedAmount, message.Currency)
    #8
    if ScriptSettings.trigger8_amount == 0:
        decTriggerAmount = 0
    else:
        decTriggerAmount = Decimal(ScriptSettings.trigger8_amount)/100
    if ScriptSettings.trigger8_type == "Donation" and ((ScriptSettings.trigger8_leg == "More then" and decTriggerAmount < decAmount) or (ScriptSettings.trigger8_leg == "Equals" and decTriggerAmount == decAmount) or (ScriptSettings.trigger8_leg == "Less then" and decTriggerAmount > decAmount)):
        parseMessage(ScriptSettings.trigger8_discordmsg, message.Name, message.FormattedAmount, message.Currency)
    #9
    if ScriptSettings.trigger9_amount == 0:
        decTriggerAmount = 0
    else:
        decTriggerAmount = Decimal(ScriptSettings.trigger9_amount)/100
    if ScriptSettings.trigger9_type == "Donation" and ((ScriptSettings.trigger9_leg == "More then" and decTriggerAmount < decAmount) or (ScriptSettings.trigger9_leg == "Equals" and decTriggerAmount == decAmount) or (ScriptSettings.trigger9_leg == "Less then" and decTriggerAmount > decAmount)):
        parseMessage(ScriptSettings.trigger9_discordmsg, message.Name, message.FormattedAmount, message.Currency)
    #10
    if ScriptSettings.trigger10_amount == 0:
        decTriggerAmount = 0
    else:
        decTriggerAmount = Decimal(ScriptSettings.trigger10_amount)/100
    if ScriptSettings.trigger10_type == "Donation" and ((ScriptSettings.trigger10_leg == "More then" and decTriggerAmount < decAmount) or (ScriptSettings.trigger10_leg == "Equals" and decTriggerAmount == decAmount) or (ScriptSettings.trigger10_leg == "Less then" and decTriggerAmount > decAmount)):
        parseMessage(ScriptSettings.trigger10_discordmsg, message.Name, message.FormattedAmount, message.Currency)
    #11
    if ScriptSettings.trigger11_amount == 0:
        decTriggerAmount = 0
    else:
        decTriggerAmount = Decimal(ScriptSettings.trigger11_amount)/100
    if ScriptSettings.trigger11_type == "Donation" and ((ScriptSettings.trigger11_leg == "More then" and decTriggerAmount < decAmount) or (ScriptSettings.trigger11_leg == "Equals" and decTriggerAmount == decAmount) or (ScriptSettings.trigger11_leg == "Less then" and decTriggerAmount > decAmount)):
        parseMessage(ScriptSettings.trigger11_discordmsg, message.Name, message.FormattedAmount, message.Currency)
    #12
    if ScriptSettings.trigger12_amount == 0:
        decTriggerAmount = 0
    else:
        decTriggerAmount = Decimal(ScriptSettings.trigger12_amount)/100
    if ScriptSettings.trigger12_type == "Donation" and ((ScriptSettings.trigger12_leg == "More then" and decTriggerAmount < decAmount) or (ScriptSettings.trigger12_leg == "Equals" and decTriggerAmount == decAmount) or (ScriptSettings.trigger12_leg == "Less then" and decTriggerAmount > decAmount)):
        parseMessage(ScriptSettings.trigger12_discordmsg, message.Name, message.FormattedAmount, message.Currency)
    #13
    if ScriptSettings.trigger13_amount == 0:
        decTriggerAmount = 0
    else:
        decTriggerAmount = Decimal(ScriptSettings.trigger13_amount)/100
    if ScriptSettings.trigger13_type == "Donation" and ((ScriptSettings.trigger13_leg == "More then" and decTriggerAmount < decAmount) or (ScriptSettings.trigger13_leg == "Equals" and decTriggerAmount == decAmount) or (ScriptSettings.trigger13_leg == "Less then" and decTriggerAmount > decAmount)):
        parseMessage(ScriptSettings.trigger13_discordmsg, message.Name, message.FormattedAmount, message.Currency)
    #14
    if ScriptSettings.trigger14_amount == 0:
        decTriggerAmount = 0
    else:
        decTriggerAmount = Decimal(ScriptSettings.trigger14_amount)/100
    if ScriptSettings.trigger14_type == "Donation" and ((ScriptSettings.trigger14_leg == "More then" and decTriggerAmount < decAmount) or (ScriptSettings.trigger14_leg == "Equals" and decTriggerAmount == decAmount) or (ScriptSettings.trigger14_leg == "Less then" and decTriggerAmount > decAmount)):
        parseMessage(ScriptSettings.trigger14_discordmsg, message.Name, message.FormattedAmount, message.Currency)
    #15
    if ScriptSettings.trigger15_amount == 0:
        decTriggerAmount = 0
    else:
        decTriggerAmount = Decimal(ScriptSettings.trigger15_amount)/100
    if ScriptSettings.trigger15_type == "Donation" and ((ScriptSettings.trigger15_leg == "More then" and decTriggerAmount < decAmount) or (ScriptSettings.trigger15_leg == "Equals" and decTriggerAmount == decAmount) or (ScriptSettings.trigger15_leg == "Less then" and decTriggerAmount > decAmount)):
        parseMessage(ScriptSettings.trigger15_discordmsg, message.Name, message.FormattedAmount, message.Currency)
    #16
    if ScriptSettings.trigger16_amount == 0:
        decTriggerAmount = 0
    else:
        decTriggerAmount = Decimal(ScriptSettings.trigger16_amount)/100
    if ScriptSettings.trigger16_type == "Donation" and ((ScriptSettings.trigger16_leg == "More then" and decTriggerAmount < decAmount) or (ScriptSettings.trigger16_leg == "Equals" and decTriggerAmount == decAmount) or (ScriptSettings.trigger16_leg == "Less then" and decTriggerAmount > decAmount)):
        parseMessage(ScriptSettings.trigger16_discordmsg, message.Name, message.FormattedAmount, message.Currency)
    #17
    if ScriptSettings.trigger17_amount == 0:
        decTriggerAmount = 0
    else:
        decTriggerAmount = Decimal(ScriptSettings.trigger17_amount)/100
    if ScriptSettings.trigger17_type == "Donation" and ((ScriptSettings.trigger17_leg == "More then" and decTriggerAmount < decAmount) or (ScriptSettings.trigger17_leg == "Equals" and decTriggerAmount == decAmount) or (ScriptSettings.trigger17_leg == "Less then" and decTriggerAmount > decAmount)):
        parseMessage(ScriptSettings.trigger17_discordmsg, message.Name, message.FormattedAmount, message.Currency)
    #18
    if ScriptSettings.trigger18_amount == 0:
        decTriggerAmount = 0
    else:
        decTriggerAmount = Decimal(ScriptSettings.trigger18_amount)/100
    if ScriptSettings.trigger18_type == "Donation" and ((ScriptSettings.trigger18_leg == "More then" and decTriggerAmount < decAmount) or (ScriptSettings.trigger18_leg == "Equals" and decTriggerAmount == decAmount) or (ScriptSettings.trigger18_leg == "Less then" and decTriggerAmount > decAmount)):
        parseMessage(ScriptSettings.trigger18_discordmsg, message.Name, message.FormattedAmount, message.Currency)
    #19
    if ScriptSettings.trigger19_amount == 0:
        decTriggerAmount = 0
    else:
        decTriggerAmount = Decimal(ScriptSettings.trigger19_amount)/100
    if ScriptSettings.trigger19_type == "Donation" and ((ScriptSettings.trigger19_leg == "More then" and decTriggerAmount < decAmount) or (ScriptSettings.trigger19_leg == "Equals" and decTriggerAmount == decAmount) or (ScriptSettings.trigger19_leg == "Less then" and decTriggerAmount > decAmount)):
        parseMessage(ScriptSettings.trigger19_discordmsg, message.Name, message.FormattedAmount, message.Currency)
    #20
    if ScriptSettings.trigger20_amount == 0:
        decTriggerAmount = 0
    else:
        decTriggerAmount = Decimal(ScriptSettings.trigger20_amount)/100
    if ScriptSettings.trigger20_type == "Donation" and ((ScriptSettings.trigger20_leg == "More then" and decTriggerAmount < decAmount) or (ScriptSettings.trigger20_leg == "Equals" and decTriggerAmount == decAmount) or (ScriptSettings.trigger20_leg == "Less then" and decTriggerAmount > decAmount)):
        parseMessage(ScriptSettings.trigger20_discordmsg, message.Name, message.FormattedAmount, message.Currency)
    return