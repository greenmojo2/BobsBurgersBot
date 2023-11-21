### **v4.3.2** - 11/21/2023 1:29 PM 
- tweak: balloons triggered by keyword instead of intent

### **v4.3.1** - 11/21/2023 1:29 PM 
- bugfix: add streamlit-extras to requirements.txt

### **v4.3** - 11/20/2023 6:22 PM
- add balloons and burgerrain eastereggs

### **v4.2** - 11/20/2023 4:16 PM
- add dialogflow response to debug output 

### **v4.1** - 11/6/2023 1:24 AM

- Add "images" folder for potential avatars. Add "obsolete" folder for antiquated code. 
- Added version information expander to top of screen.

### **v4** - 11/3/23 4:39 PM

#### **Entirely redone prompting for GenAI.**  

Context is now assembled from a personality description, a background, and a knowledgebase. All three are embedded within a wrapper instruction to play a character using those three "parts".  

User message sent to GenAI is now wrapped around by instructions as well. New function FormatPrompt(msg) will take passed string and include it within instructions specifying that the answer must come from the assembled entity specified in the context.

#### **Better placeholder message while GenAI is busy.**

Instead of the loading message always saying "Louise is busy with customers...", there is now a list of prewritten "away" messages that sound like something Louise might say. A random one is picked to display while the GenAI is busy

#### **Bot responses simulate being typed**

Replies from the bot will now print characters seperately and wait a configurable number of milliseconds before continuing to the next character. Gives the appearance of being typed instead of poofing into existence all at once

#### **Misc (or minor) upgrades**
"Chat History:" will no longer appear at the top of the page if no messages have been exchanged yet.

Add notes about upgraded generative AI prompting in seperate markdown file.

GenAI parameters and away messages are specified in v2_GenAIParameters_v2.py

VersionInformation.py renamed to VersionInformation.py.old and contains v3 info. v4 and newer in (this) Markdown file and display when typing "version" into chatbot

#### **Work in Progress**
Changing Louse's avatar icon from the bot to her bunny ears.  