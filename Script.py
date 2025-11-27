class script(object):
    LOGO = """
VJ Filter Bot
"""

    RESTART_TXT = """
<b>Bot Restarted!</b>
<b>Date:</b> {}
<b>Time:</b> {}
"""

    START_TXT = """<i><b>Hello {},</b></i>"""



    CAPTION = """<b>File Name:</b> {filename}
<b>Size:</b> {filesize}
<b>Duration:</b> {duration}"""

    MANUELFILTER_TXT = """Help: <b>Filters</b>
- Filter is a feature where users can set automated replies for a particular keyword and I will respond whenever a keyword is found in the message
<b>Note:</b>
1. This bot should have admin privilege.
2. Only admins can add filters in a chat.
3. Alert buttons have a limit of 64 characters.
Commands And Usage:
• /filter - <code>Add a filter in a chat</code>
• /filters - <code>List all the filters of a chat</code>
• /del - <code>Delete a specific filter in a chat</code>
• /delall - <code>Delete the whole filters in a chat (chat owner only)</code>"""



    BUTTON_TXT = """Help: <b>Buttons</b>
- This bot supports both url and alert inline buttons.
<b>Note:</b>
1. Telegram will not allow you to send buttons without any content, so content is mandatory.
2. This bot supports buttons with any telegram media type.
3. Buttons should be properly parsed as markdown format
<b>URL Buttons:</b>
<code>[Button Text](buttonurl:https://t.me/ebookguy)</code>
<b>Alert Buttons:</b>
<code>[Button Text](buttonalert:This is an alert message)</code>"""

    AUTOFILTER_TXT = """Help: <b>Auto Filter</b>
<b>Note: File Index</b>
1. Make me the admin of your channel if it's private.
2. Make sure that your channel does not contains unwanted content, porn and fake files.
3. Forward the last message to me with Quotes. I'll add all the files in that channel to my db.

<b>Note: AutoFilter</b>
1. Add the bot as admin on your group.
2. Use /connect and connect your group to the bot.
3. Use /settings on bot's PM and turn on AutoFilter on the settings menu."""

    CONNECTION_TXT = """Help: <b>Connections</b>
- Used to connect bot to PM for managing filters 
- It helps to avoid spamming in groups.
<b>Note:</b>
1. Only admins can add a connection.
2. Send <code>/connect</code> for connecting me to your PM
Commands And Usage:
• /connect  - <code>Connect a particular chat to your PM</code>
• /disconnect  - <code>Disconnect from a chat</code>
• /connections - <code>List all your connections</code>"""



    EXTRAMOD_TXT = """Help: Extra Modules
<b>Note:</b>
my features Stay here new features coming soon...  
 <b>✯ Maintained by : <a href=https://t.me/ebookguy>☢VJ☢</a></b>
  
 <b>✯ Join here : <a href=https://t.me/ebookguy>☢Join my updateds☢</a></b> 
  
 ./id - <code>Get id of a specified user.</ 
 code> 
  
 ./info  - <code>Get information about a user.</code> 
  
 ./song - Download any song [<code>example /song vaa vaathi song</code>] 
  
 ./telegraph - <code>Telegraph generator sen under 5MB video or photo I give telegraph link</code> 
  
 ./tts - <code>This command usage text to voice converter</code> 
  
 ./video - This command usage any YouTube video download hd [<code>example /video https://youtu.be/Aiue8PMuD-k</code>]

./font - This command usage stylish and cool font generator [<code>example /font hi</code>]"""


    ADMIN_TXT = """Help: Admin Mods
<b>Note:</b>
This Module Only Works For My Admins
Commands And Usage:
• /logs - <code>To get the recent errors</code>
• /stats - <code>To get status of files in db. [This Command Can Be Used By Anyone]</code>
• /delete - <code>To delete a specific file from db.</code>
• /users - <code>To get list of my users and ids.</code>
• /chats - <code>To get list of my chats and ids</code>
• /leave  - <code>To leave from a chat.</code>
• /disable  -  <code>To disable a chat.</code>
• /ban  - <code>To ban a user.</code>
• /unban  - <code>To unban a user.</code>
• /channel - <code>To get list of total connected channels</code>
• /broadcast - <code>To broadcast a message to all users</code>
• /grp_broadcast - <code>To broadcast a message to all connected groups.</code>
• /gfilter - <code>To add global filters</code>
• /gfilters - <code>To view list of all global filters</code>
• /delg - <code>To delete a specific global filter</code>
• /request - <code>To send a Book/Audiobook request to bot admins. Only works on support group. [This Command Can Be Used By Anyone]</code>
• /delallg - <code>To delete all Gfilters from the bot's database.</code>
• /deletefiles - <code>To delete Unwanted Files from the bot's database.</code>"""

    SEC_STATUS_TXT = """<b>★ Total Users: <code>{}</code>
★ Total Chats: <code>{}</code>
★ Total Files: <code>{}</code>
★ Used Storage: <code>{} MB</code>
★ Free Storage: <code>{} MB</code></b>"""
    
    STATUS_TXT = """<b>Total Files From All DBs: <code>{}</code>

USERS DB :-
★ Total Users: <code>{}</code>
★ Total Chats: <code>{}</code>

FILE FIRST DB :-
★ Total Files: <code>{}</code>
★ Used Storage: <code>{} MB</code>
★ Free Storage: <code>{} MB</code>

FILE SECOND DB :-
★ Total Files: <code>{}</code>
★ Used Storage: <code>{} MB</code>
★ Free Storage: <code>{} MB</code>

OTHER DB :-
★ Used Storage: <code>{} MB</code>
★ Free Storage: <code>{} MB</code></b>"""

    LOG_TEXT_G = """#NewGroup
Group = {}(<code>{}</code>)
Total Members = <code>{}</code>
Added By - {}"""

    LOG_TEXT_P = """#NewUser
ID - <code>{}</code>
Name - {}"""

    ALRT_TXT = """Hello {},
This is not your request,
Request yours..."""

    OLD_ALRT_TXT = """Hey {},
You are using one of my old messages, 
Please send the request again."""

    CUDNT_FND = """I couldn't find anything related to {}
Did you mean any of these?"""

    I_CUDNT = """<b>No files were found for your request {} ❌

Check your spelling on Google. 😃

Book Request Format 👇

Example : Atomic Habits, Atomic Habits James Clear or You can send a author name Ex. "Robert Greene"

Audiobook Request Format 👇

Example : 'Audiobook Name' and check the size in the list.

🚯 Don't use ➠ ':(!,./)</b>"""

    I_CUD_NT = """I couldn't find Anything Related to {}.
Please check the spelling on Google..."""


    DEVELOPER_TXT = """
special Thanks To ❤️ Developers -

-Dev 1 [Owner of this bot ]<a href='https://t.me/ebookguy'>EbookGuy</a>

-Dev 2 <a href='https://t.me/ebookguy'>EbookGuy</a>

-Dev 3 <a href='https://t.me/ebookguy>EbookGuy</a>

- Dev 4 <a href='https://t.me/ebookguy'>TEAM EbookGuy</a>
"""

    RENAME_TXT = """
🌌 <b><u>HOW TO SET THUMBNAIL</u></b>
  
•> /set_thumb - send any picture to automatically set thumbnail.
•> /del_thumb use this command and delete your old thumbnail.
•> /view_thumb use this command view your current thumbnail.

📑 <b><u>HOW TO SET CUSTOM CAPTION</u></b>

•> /set_caption - set a custom caption
•> /see_caption - see your custom caption
•> /del_caption - delete custom caption

Example:- /set_caption 📕 File Name: {filename}
💾 Size: {filesize}
⏰ Duration: {duration}

✏️ <b><u>HOW TO RENAME A FILE</u></b>

•> /rename - send any file and click rename option and type new file name and \nthen select [ document, video, audio ]👈 choice this.
"""







    MVE_NT_FND = "I couldn't find any book/audiobook with that name."
    NORSLTS = "#NoResults\nID: {}\nName: {}\nQuery: {}"
    TOP_ALRT_MSG = "Checking for results..."
    REQINFO = "Send me the book name you want."
    SELECT = "Select an option."
    SINFO = "Book Information"