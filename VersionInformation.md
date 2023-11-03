# v4 - 11/2/23 10:11 PM

## Entirely redone prompting for GenAI.
* Repeated instructions to favor short replies (which seems to keep it more on track)
* Context now consists of these seperately defined parameters:
    - Personality
    - Background
    - Knowledgebase
- Added FormatPrompt(message) function
    - User input now inserted into instructive wrapper. 
    - Instructions specify usage of assembled context
## Misc
- Replaced "Louse is busy with customers..." message with a randomly picked away message from a list
- Chat history: header no longer appears if history is empty
- All new parameters are specified in v2_GenAIParameters_v2.py
- Started work on new avatars in away messages


version = 'v3'
date = '11/1/2023 2:36 PM\n'
changelog = '2 to v3\n\n----------\n\nOverall\n\n- add listener for keyword debug\n\n- add listener for keyword version\n\n- add version file for keep track of updates\n\n- update generative AI parameters\n\n----------\n\nGenAI Parameters\n\n- temperature .9 to .8\n\n- top_k 40 to 60\n\n- add two more examples'
