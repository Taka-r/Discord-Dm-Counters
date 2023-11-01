# Discord DM Counter Bot

## Getting Started

To use this bot, follow these steps:

1. Clone this repository to your local machine.

2. Run 

3. 

4. Install the required dependencies using pip:

```pip install -r requirements.txt```

6. Run the Python script `discordm.py` to start the bot. It will log in, initiate the counters, and start scanning for new DMs.

**Note:** It's essential to run `start.py` script to initialize the `token.txt` and `status_message.txt` files. This script will create the necessary files and set up your bot for use.

## Usage

Once the bot is up and running, you can use the following commands to control its behavior:

- `!selfon` or `!selfoff`: Turn on or off the DM scan feature. This also turns off the automatic status message.
- `!selftarget`: Choose what should be replaced with the custom message. Use `!selftarget bio` to set your About Me page and `!selftarget activity` to set it as a custom activity. Use `!selftarget` to turn off the custom status message.
- `!selfinterval MINUTES`: Set the next scan interval in minutes (between 1 and 1440).
- `!selfgroupon` or `!selfgroupoff`: Allow or disallow scanning of group DMs.
- `!selfdbgchannel CHANNELID`: Set the debug channel to receive debug information, or leave it empty to reset.
- `!selfonlyuser USERID`: Count DMs only from a specific user by providing their USERID, or leave it empty to reset.
- `!selfonlychannel CHANNELID`: Count DMs only from a specific DM channel by providing its CHANNELID, or leave it empty to reset.
- `!selfchannelinfo CHANNELID`: Get the number of DMs you've received in a specific channel (this does not trigger a scan).
- `!selfdelhistory`: Delete all counter history, causing all DMs to be scanned anew.
- `!selfdebug`: Create a `.txt` file with debug information from the last DM scan.

For more detailed information on how to use these commands, use `!selfhelp` in your Discord chat.

## Disclaimer

This bot is designed for personal use and may require modifications to fit your specific needs. This is topically a self bot made for educational purposes. You can get banned if you use it.

Feel free to modify and extend this project to suit your requirements.