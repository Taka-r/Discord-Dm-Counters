# Discord DM Counter Bot

## Overview

This Python Discord bot is designed to count the number of Direct Messages (DMs) received and update the user's Discord status message based on the count. The bot scans DM channels and keeps track of the number of new messages received each day. It can be configured to automatically update the user's Discord bio or custom activity with the count of DMs received.

## Getting Started

To use this bot, follow these steps:

1. Clone this repository to your local machine.

2. Create a file named `token.txt` in the same directory as the bot's Python script. Place your Discord bot token in this file. This token is required for the bot to log in.

3. Create a file named `status_message.txt` in the same directory. This file should contain the message you want to set as your Discord status. Use the token `RECEIVED_DM_CNT` to represent the number of received DMs, which will be dynamically replaced by the bot.

4. Configure the bot by editing the `cfg.txt` file. You can set options such as the debug channel, user or channel filtering, group DM allowance, and more.

5. Run the Python script to start the bot. It will log in, initiate the counters, and start scanning for new DMs.

## Commands

The bot supports various commands for controlling its behavior:

- `!selfping`: Returns a response message.
- `!selfon` or `!selfoff`: Turns on or off the DM scan feature (also turns off automatic status message).
- `!selftarget`: Choose what should be replaced with the custom message:
  - `!selftarget bio`: Sets your About Me page.
  - `!selftarget activity`: Sets it as a custom activity.
  - `!selftarget`: Turns off custom status message.
- `!selfinterval MINUTES`: Sets the next scan interval (MINUTES should be a number between 1 and 1440).
- `!selfgroupon` or `!selfgroupoff`: Allows or disallows scanning of group DMs.
- `!selfdbgchannel CHANNELID`: Replace CHANNELID with a channel ID to get debug info there, or leave empty to reset.
- `!selfonlyuser USERID`: Replace USERID with a user's ID to count DMs ONLY from that user, or leave empty to reset.
- `!selfonlychannel CHANNELID`: Replace CHANNELID with a channel ID to count DMs ONLY from that DM channel, or leave empty to reset.
- `!selfchannelinfo CHANNELID`: Replace CHANNELID with a channel ID to get the number of DMs received in that channel (does not scan).
- `!selfdelhistory`: Deletes all counter history, so all DMs will have to get scanned anew.
- `!selfdebug`: Creates a .txt file with debug info from the last DM scan.

Please make sure to configure the bot and customize the status message before running it.

## License

This project is licensed under the [Your License Name] - see the [LICENSE.md](LICENSE.md) file for details.
