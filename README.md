# BobsBurgersBot
## Todo:
- More error capturing to avoid problems
    - [X] block user from submitting blank messages
    - [ ] check if Dialogflow will filter/censor incoming messages
    - [ ] stop matched intents with no answers from fucking everything up
    - [ ] figure out what PaLM does if the current message is OK but history contains messages it wants to filter
    - [x] trap blank replies from PaLM before they come in like a wrecking ball
- [ ] finish writing todo list
- [ ] more fun easter eggs
    - [X] "I wish it was snowing!"
    - [ ] "Something something celebration"
- [ ] simulate bot "typing" by outputting a couple characters every few milliseconds instead of whole message at once
- [ ] better icons for identifying who the message is front. maybe just the bunny ears for Louise? 
- [ ] possibly seperate out context and examples for PaLM to another file for easier tweaking
- [ ] add more examples to PaLM
- [ ] figure out commands to actually tune model instead of only steering the base model's response
- [ ] unclusterfuck my google cloud console
- [ ] find tool to make writing markdown less of a PITA
- [ ] resist urge to add speech-to-text 
