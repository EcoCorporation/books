class script(object):
    LOGO = """
Filter Bot
"""

    BTN_LABEL_1 = "🔥 Our Main Channel 🔥"
    BTN_LABEL_2 = "📚 How to Search Book Properly"
    BTN_LABEL_3 = "🔥 Fat Burning Kitchen"
    BTN_LABEL_4 = "💖 His Secret Obsession"

    RESTART_TXT = """
<b>Bot Restarted!</b>
<b>Date:</b> {}
<b>Time:</b> {}
"""

    START_TXT = """<b>👋 Hello {},</b>

Welcome to your personal <b>Digital Library</b> 📚.

I can help you find <b>E-Books</b> and <b>Audiobooks</b> in seconds.

<b>🚀 How to use me:</b>
Simply type the <b>Book Name</b> or <b>Author Name</b> and I will search my library for you.

<i>👇 Join our channels for updates & support.</i>"""



    CAPTION = """<b>File Name:</b> {filename}
<b>Size:</b> {filesize}
<b>Duration:</b> {duration}"""

    MELCOW_ENG = """<b>👋 Hello {},\n\nWelcome to {} 📚.\n\nI can help you find E-Books and Audiobooks in seconds.</b>"""

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
    TOP_ALRT_MSG = "Checking for results..."
    PLEASE_WAIT = "<b>Please wait...</b>"
    UNABLE_TO_OPEN_FILE = "UNABLE TO OPEN FILE."
    INVALID_LINK = "<b>Invalid link or expired link</b>"
    VERIFY_SUCCESS = "<b>Hey {} 👋,\n\nYou have completed the verification...\n\nNow you have unlimited access till today now enjoy\n\n</b>"
    FILE_READY = "<b>✅ Your file ready click on download now button then open link to get file\n\n</b>"
    NO_FILE_EXIST = "<b><i>No such file exist.</b></i>"
    VERIFY_MSG = "<b>Hey {} 👋,\n\nYou are not verified today, please click on verify & get unlimited access for today</b>"
    SEARCH_AGAIN = "<b>Please Search Again in Group</b>"
    GET_FILE_AGAIN = "✅ Get File Again ✅"
    IMPORTANT_DELETE_MSG = "<blockquote><b><u>❗️❗️❗️IMPORTANT❗️️❗️❗️</u></b>\n\nThis message will be deleted in <b><u>10 mins</u> 🫥 <i></b>(due to copyright issues)</i>.\n\n<b><i>Please forward this message to your saved messages or any private chat.</i></b></blockquote>"
    FILE_DELETED_BTN = "<b>✅ File Deleted, If you want the file CLick on below button.</b>"
    MSG_DELETED = "<b>✅ Your message is successfully deleted</b>"
    
    BACKUP_CHANNEL_NOT_JOINED = "**🕵️ You have not joined my backup channel. First join channel then try again**"
    BACKUP_CHANNEL_NOT_JOINED_2 = "**🕵️ You have not joined my backup channel. First join channel**"
    FORCE_SUB_ADMIN_ERROR = "Make sure Bot is admin in Forcesub channel"
    FORCE_SUB_ERROR = "something wrong with force subscribe."
    BACKUP_CHANNEL_BTN = "Backup Channel"
    TRY_AGAIN_BTN = "↻ Try Again"
    
    UNMUTE_TEXT = "👋 Hello {},\n\nPlease join the channel then click on unmute me button. 😇"
    SUPPORT_GROUP_TEXT = "<b>Hey {}, {} results are found in my Library for your query {}. \n\nThis is a support group so that you can't get files from here...\n\nJoin and Search Here - {}</b>"
    NO_RESULTS_MSG = """<b>❌ No Results Found</b>

We couldn't find <b>"{}"</b> in our Library.

<b>👇 Try these steps:</b>
1. Check spelling on <a href="https://www.google.com/search?q={}+book">Google</a>.
2. Search for the <b>Author</b> instead.
3. Still can't find it? Type <code>/request {}</code> to notify admins."""