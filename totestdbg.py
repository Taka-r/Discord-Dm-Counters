# note: code is a mess, but it still works. modify it however you see fit   -fabrii_h_enjoyer_69

import discord
from discord.ext import tasks # to make the automatic bio update loop
import asyncio # will probably need this one for asynchronous mumbo
import os # to read the counters directory
import os.path # need this for file stuff
import datetime # datetime library
from datetime import datetime as dt # datetime objects
from datetime import timezone as tz # timezone mumbo jumbo


dtFormat = "%d-%m-%Y %H:%M:%S@%z"  # datetime format used throughout the program
uEpoch = dt.fromtimestamp(0, tz.utc)  # unix epoch in UTC, used as a default datetime value
uEpochStr = uEpoch.strftime(dtFormat)  # same but as a string


# function returns the start of day as an aware datetime object in UTC. probably a better way to do it but i don't care
def get_start_of_day():
    # get current local time, naive object
    # convert to aware object using system timezone (pray it's the right one)
    # get start of day by zeroing hour, minute, second, microsecond
    # convert result to UTC
    return dt.now().astimezone().replace(hour=0, minute=0, second=0, microsecond=0).astimezone(tz.utc)


class MyClient(discord.Client):
    def __init__(self):
        super(MyClient, self).__init__()
        self.dayCnts = {}  # dict for day counters. key is datetime object, value is cnt
        self.lastDbg = ""  # stores the last debug info
        self.dbgChannelId = None  # channel to send some of the debug info
        self.onlyCheckUser = None  # if not none, checks only this user ID for messages
        self.onlyCheckChannel = None  # same but for channels
        self.allowGroupDMs = False  # what it says
        self.scanOn = True  # doesn't scan if False
        self.textTarget = 1  # 0 to disable, 1 for Bio (About me), 2 for Activity
        self.maxMinsLeft = 5  # scan every X minutes
        self.minsLeft = 1  # minutes left till next scan
        self.scanning = False


    # updates the dict with the given key and value
    def update_dayCnts(self, keyVal, valVal):
        try:
            self.dayCnts[keyVal] += valVal
        except KeyError:
            self.dayCnts[keyVal] = valVal

    # called once when bot runs to populate the dayCnts dict with the current counters. useful if bot gets ran twice in a day
    async def init_dayCnts(self):
        # iterate over all files in the counters directory
        for fname in os.listdir("counters"):
            fname = "counters/" + fname  # append fname to dirname
            with open(fname, "r") as f:
                flines = f.readlines()

            # parse key and value
            keyVal = dt.strptime(flines[1].strip(), dtFormat)
            valVal = int(flines[2])
            fileFromId = int(flines[3])

            # update if it's from the same bot, otherwise delete .txt file
            if fileFromId == self.user.id:
                self.update_dayCnts(keyVal, valVal)
            else:
                os.remove(fname)


    async def getConfigData(self):
        if not os.path.isfile("cfg.txt"):
            raise ValueError('no config file found')
            return

        with open("cfg.txt", "r") as f:
            flines = f.readlines()

        for fline in flines:
            if 'dbgChannelId' in fline:
                val = fline[fline.index('=')+1:].strip()
                try:
                    val = int(val)
                    if val == 0:
                        self.dbgChannelId = None
                    else:
                        self.dbgChannelId = val
                except:
                    self.dbgChannelId = None
            elif 'onlyCheckUser' in fline:
                val = fline[fline.index('=')+1:].strip()
                if val == "0":
                    self.onlyCheckUser = None
                else:
                    self.onlyCheckUser = val
            elif 'onlyCheckChannel' in fline:
                val = fline[fline.index('=')+1:].strip()
                if val == "0":
                    self.onlyCheckChannel = None
                else:
                    self.onlyCheckChannel = val
            elif 'allowGroupDMs' in fline:
                val = fline[fline.index('=')+1:].strip()
                if val == "0":
                    self.allowGroupDMs = False
                else:
                    self.allowGroupDMs = True
            elif 'scanOn' in fline:
                val = fline[fline.index('=') + 1:].strip()
                if val == "0":
                    self.scanOn = False
                else:
                    self.scanOn = True
            elif 'textTarget' in fline:
                val = fline[fline.index('=')+1:].strip()
                try:
                    val = int(val)
                    if 1 <= val <= 2:
                        self.textTarget = val
                    else:
                        self.textTarget = 0
                except:
                    self.textTarget = 0
            elif 'maxMinsLeft' in fline:
                val = fline[fline.index('=')+1:].strip()
                try:
                    val = int(val)
                    if 1 <= val <= 1440:
                        self.maxMinsLeft = val
                    else:
                        self.maxMinsLeft = 5
                except:
                    self.maxMinsLeft = 5


    async def on_ready(self):
        print(f'logged in as {self.user}. getting config data...')
        try:
            await self.getConfigData()
        except:
            print('no config file found')
            return
        print('initializing internal counters...')
        await self.init_dayCnts()
        print('starting scan loop...')
        await self.update_bio_loop.start()


    async def on_message(self, message):
        # only respond to ourselves
        if message.author != self.user:
            return
        
        if message.content == '!selfping':
            await message.channel.send('selfpong')

        elif message.content == '!selftest':
            print(f"""self.dayCnts {self.dayCnts}
self.dbgChannelId {self.dbgChannelId}
self.onlyCheckUser {self.onlyCheckUser}
self.onlyCheckChannel {self.onlyCheckChannel}
self.allowGroupDMs {self.allowGroupDMs}
self.scanOn {self.scanOn}
self.textTarget {self.textTarget}
self.maxMinsLeft {self.maxMinsLeft}
self.minsLeft {self.minsLeft}
self.scanning {self.scanning}""")

        elif message.content == '!selfdebug':
            with open("debug.txt", "w") as f:
                f.write(self.lastDbg)

            await asyncio.sleep(0.5)
            await message.channel.send(file=discord.File("debug.txt"))

        elif message.content == '!selfon':
            self.scanOn = True

            with open("cfg.txt", "r") as f:
                flines = f.readlines()
            for i in range(len(flines)):
                if 'scanOn' in flines[i]:
                    flines[i] = "scanOn=1\n"
                    break
            with open("cfg.txt", "w") as f:
                f.writelines(flines)

            await asyncio.sleep(0.5)
            await message.add_reaction('✅')

        elif message.content == '!selfoff':
            self.scanOn = False

            with open("cfg.txt", "r") as f:
                flines = f.readlines()
            for i in range(len(flines)):
                if 'scanOn' in flines[i]:
                    flines[i] = "scanOn=0\n"
                    break
            with open("cfg.txt", "w") as f:
                f.writelines(flines)

            await asyncio.sleep(0.5)
            await message.add_reaction('✅')

        elif message.content == '!selfgroupon':
            self.allowGroupDMs = True

            with open("cfg.txt", "r") as f:
                flines = f.readlines()
            for i in range(len(flines)):
                if 'allowGroupDMs' in flines[i]:
                    flines[i] = "allowGroupDMs=1\n"
                    break
            with open("cfg.txt", "w") as f:
                f.writelines(flines)

            await asyncio.sleep(0.5)
            await message.add_reaction('✅')

        elif message.content == '!selfgroupoff':
            self.allowGroupDMs = False

            with open("cfg.txt", "r") as f:
                flines = f.readlines()
            for i in range(len(flines)):
                if 'allowGroupDMs' in flines[i]:
                    flines[i] = "allowGroupDMs=0\n"
                    break
            with open("cfg.txt", "w") as f:
                f.writelines(flines)

            await asyncio.sleep(0.5)
            await message.add_reaction('✅')

        elif message.content.startswith("!selfdbgchannel"):
            contents = message.content.split(" ")
            if len(contents) > 1:
                self.dbgChannelId = contents[1]
                val = contents[1]
            else:
                self.dbgChannelId = None
                val = 0

            with open("cfg.txt", "r") as f:
                flines = f.readlines()
            for i in range(len(flines)):
                if 'dbgChannelId' in flines[i]:
                    flines[i] = f"dbgChannelId={val}\n"
                    break
            with open("cfg.txt", "w") as f:
                f.writelines(flines)

            await asyncio.sleep(0.5)
            await message.add_reaction('✅')

        elif message.content.startswith("!selfonlychannel"):
            contents = message.content.split(" ")
            if len(contents) > 1:
                self.onlyCheckChannel = contents[1]
                val = contents[1]
                self.dayCnts = {}
            else:
                self.onlyCheckChannel = None
                val = 0

            with open("cfg.txt", "r") as f:
                flines = f.readlines()
            for i in range(len(flines)):
                if 'onlyCheckChannel' in flines[i]:
                    flines[i] = f"onlyCheckChannel={val}\n"
                    break
            with open("cfg.txt", "w") as f:
                f.writelines(flines)

            await asyncio.sleep(0.5)
            await message.add_reaction('✅')

        elif message.content.startswith("!selfonlyuser"):
            contents = message.content.split(" ")
            if len(contents) > 1:
                self.onlyCheckUser = contents[1]
                val = contents[1]
                self.dayCnts = {}
            else:
                self.onlyCheckUser = None
                val = 0

            with open("cfg.txt", "r") as f:
                flines = f.readlines()
            for i in range(len(flines)):
                if 'onlyCheckUser' in flines[i]:
                    flines[i] = f"onlyCheckUser={val}\n"
                    break
            with open("cfg.txt", "w") as f:
                f.writelines(flines)

            await asyncio.sleep(0.5)
            await message.add_reaction('✅')

        elif message.content.startswith("!selfchannelinfo"):
            contents = message.content.split(" ")
            if len(contents) > 1:
                await asyncio.sleep(0.5)
                fpath = f"counters/{contents[1]}.txt"
                if os.path.isfile(fpath):
                    with open(fpath, "r") as f:
                        flines = f.readlines()

                    await message.channel.send(f"received counter: {flines[2]} since {flines[1]}")
                else:
                    await message.channel.send('no DMs received or channel not scanned yet')

        elif message.content == '!selfdelhistory':
            failed = False
            numTries = 5
            for fname in os.listdir('counters'):
                try:
                    os.remove(f'counters/{fname}')
                except:
                    failed = True

            if failed:
                await asyncio.sleep(0.5)
                await message.add_reaction('❌')
            else:
                await asyncio.sleep(0.5)
                await message.add_reaction('✅')

        elif message.content.startswith('!selftarget'):
            contents = message.content.split(" ")
            if len(contents) > 1:
                if contents[1] == 'bio':
                    self.textTarget = 1
                elif contents[1] == 'activity':
                    self.textTarget = 2
            else:
                self.textTarget = 0

            with open("cfg.txt", "r") as f:
                flines = f.readlines()
            for i in range(len(flines)):
                if 'textTarget' in flines[i]:
                    flines[i] = f"textTarget={self.textTarget}\n"
                    break
            with open("cfg.txt", "w") as f:
                f.writelines(flines)

            await asyncio.sleep(0.5)
            await message.add_reaction('✅')

        elif message.content.startswith('!selfinterval '):
            contents = message.content.split(" ")
            try:
                val = int(contents[1])
            except:
                await asyncio.sleep(0.5)
                await message.add_reaction('❌')
            else:
                if 1 <= val <= 1440:
                    self.maxMinsLeft = val

                    with open("cfg.txt", "r") as f:
                        flines = f.readlines()
                    for i in range(len(flines)):
                        if 'maxMinsLeft' in flines[i]:
                            flines[i] = f"maxMinsLeft={self.maxMinsLeft}\n"
                            break
                    with open("cfg.txt", "w") as f:
                        f.writelines(flines)

                    await asyncio.sleep(0.5)
                    await message.add_reaction('✅')
                else:
                    await asyncio.sleep(0.5)
                    await message.add_reaction('❌')


        elif message.content == '!selfhelp':
            await asyncio.sleep(0.5)
            await message.channel.send("""The message you want to use should be placed into the `status_message.txt` file, which should be in the same directory as the script. The token `RECEIVED_DM_CNT` will be replaced by the number of DMs received, according to your settings

*Commands that take arguments default to certain values if a bad argument is given*
List of commands:
`!selfhelp`: prints this message
`!selfping`: returns an answer
`!selfon` or `!selfoff`: turn on or off the DM scan feature (also turns off automatic status message)
`!selftarget`: choose what should be replaced with the custom message
-`!selftarget bio` to set your About Me page
-`!selftarget activity` to set it as a custom activity
-`!selftarget` to turn off custom status message (note: to turn off scan, use `!scanoff`)
`!selfinterval MINUTES` where MINUTES is a number between 1 and 1440: set the next scan intervals
`!selfgroupon` or `!selfgroupoff`: allow or disallow scanning of group DMs
`!selfdbgchannel CHANNELID`: replace CHANNELID with a channel ID to get debug info there, or leave empty to reset
`!selfonlyuser USERID`: replace USERID with a user's ID to count DMs ONLY from that user, or leave empty to reset
`!selfonlychannel CHANNELID`: replace CHANNELID with a channel ID to count DMs ONLY from that DM channel, or leave empty to reset
`!selfchannelinfo CHANNELID`: replace CHANNELID with a channel ID to get how many DMs you've received in that channel (does not scan)
`!selfdelhistory`: deletes all counter history, so all DMs will have to get scanned anew
`!selfdebug`: in the script directory, creates a .txt file with debug info from the last DM scan""")

        await asyncio.sleep(1)  # sleep after every command, just in case


    # task that loops every self.maxMinsLeft minutes and updates the bio with the number of DMs received today
    @tasks.loop(minutes=1)
    async def update_bio_loop(self):
        if not self.scanOn:
            return

        self.minsLeft -= 1
        if self.minsLeft > 0:
            return
        else:
            self.minsLeft = self.maxMinsLeft

        self.lastDbg = ""

        # fetch all DM channels
        fetStr = 'fetching DM channels\n'
        print(fetStr)
        self.lastDbg += fetStr
        channels = await self.fetch_private_channels()
        fetStr = f"{len(channels)} channels found, searching for suitable results\n"
        print(fetStr)
        self.lastDbg += fetStr
        try:
            dbgCh = self.get_channel(int(self.dbgChannelId))
        except:
            dbgCh = None
        else:
            await dbgCh.send(fetStr)

        # init variables before any loops
        curGcnt = 0
        startOfDay = get_start_of_day()

        for cha in channels:
            cid = cha.id

            if self.onlyCheckChannel is not None and str(cid) != self.onlyCheckChannel:
                continue

            # filter out channels if needed
            if self.allowGroupDMs:
                self.lastDbg += f"scanning channel ID {cid}\n"
            else:
                if cha.type != discord.ChannelType.private:
                    continue
                try:
                    rec = cha.recipient
                except:
                    continue

                if self.onlyCheckUser is not None and str(rec.id) != self.onlyCheckUser:
                    continue

                self.lastDbg += f"scanning channel ID {cid} of user {rec.name}\n"

            fpath = f"counters/{cid}.txt"

            # read from that DM's file, or create it if it doesn't exist yet
            # file format:
            #stopId
            #cntDate       in dtFormat
            #counter
            #ownId
            if os.path.isfile(fpath):
                with open(fpath, "r") as f:
                    flines = f.readlines()

                stopId = int(flines[0])
                cntDateStr = flines[1].strip()  # read cntDate as string first
                cntDate = dt.strptime(cntDateStr, dtFormat)  # convert to an aware datetime object
                cnt = int(flines[2])
                ownId = int(flines[3])
            else:
                self.lastDbg += f"creating file for channel {cid}\n"
                with open(fpath, "w") as f:
                    # default values. don't touch the indentations
                    f.write(f"""0
{uEpochStr}
0
{self.user.id}""")

                stopId = 0
                cntDate = uEpoch
                cnt = 0
                ownId = self.user.id

            self.lastDbg += f"channel cnt {cnt}, stop at {stopId}\n"

            curCnt = 0
            curStopId = 0

            # iterate over every message in this channel up to the start of the local day
            async for chMsg in cha.history(limit=None, after=startOfDay, oldest_first = False):
                self.lastDbg += f"msg {chMsg.id} from {chMsg.author.id} ({chMsg.author.name})\n"

                # remember the new stop message. ugly but works
                if curStopId == 0:
                    curStopId = chMsg.id
                    self.lastDbg += f"new stop id {curStopId}\n"

                # break if the stop message has been reached (or exceeded, in case message was deleted)
                if chMsg.id <= stopId:
                    break

                # only need messages from the recipient (the other user in the DM)
                if chMsg.author.id != self.user.id:
                    self.lastDbg += f"inc on {chMsg.id}\n"
                    curCnt += 1  # increment the current counter for this user

            # once loop is over, we've either reached the last stop message or iterated through all messages in the day
            # check if the read counter wasn't from yesterday
            if cntDate < startOfDay:
                # that counter is from yesterday. replace it with the new one...
                cnt = curCnt
                # update the date string too
                cntDateStr = startOfDay.strftime(dtFormat)
            else:
                # that counter is from the same day, just increment it
                cnt += curCnt

            # update the internal daily counters
            self.update_dayCnts(startOfDay, curCnt)
            curGcnt += curCnt  # update current global counter

            # just in case...
            if curStopId == 0:
                curStopId = stopId

            # save the count in the user's file. don't touch the indentations
            with open(fpath, "w") as f:
                f.write(f"""{curStopId}
{cntDateStr}
{cnt}
{ownId}""")

            # show result in console
            chaRes = f"channel {cid}: found {curCnt} new received messages, for a total of {cnt}\n"
            self.lastDbg += chaRes
            print(chaRes)

        gres = f"completed. you've received {curGcnt} new messages since the last check, for a total of "
        try:
            recDMsCnt = str(self.dayCnts[startOfDay])
            gres += str(recDMsCnt) + " messages today"
        except KeyError:
            recDMsCnt = "0"
            gres += "0 messages today"

        # show global result in console after all DMs have been checked
        print(gres)
        self.lastDbg += gres + "\n"
        if dbgCh is not None:
            await dbgCh.send(gres)

        # update status
        if 1 <= self.textTarget <= 2:
            with open("status_message.txt", "r") as f:
                statusMessage = f.read().replace("RECEIVED_DM_CNT", str(recDMsCnt))

            try:
                if self.textTarget == 1:
                    await self.user.edit(bio=statusMessage)
                elif self.textTarget == 2:
                    await self.change_presence(activity=discord.CustomActivity(name=statusMessage))
            except Exception as e:
                if dbgCh is not None:
                    await asyncio.sleep(0.5)
                    await dbgCh.send("something went wrong while changing status:\n", e)
                else:
                    print("something went wrong while changing status:\n", e)


    @update_bio_loop.after_loop
    async def after_bio_loop(self):
        self.scanning = False


# reads the first line of that .txt and removes any whitespaces
def readToken():
    with open("token.txt", "r") as f:
        flines = f.readlines()

    return flines[0].strip()


client = MyClient()
client.run(readToken())
