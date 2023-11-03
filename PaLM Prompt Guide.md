# GenAI prompting
## Context
Context is used to give the LLM a better understanding of the conversation. Here is the structure of the context (preamble):
```
{
  context: `Your task is to acting as a character that has this personality: "${config.state.personality}". Your response must be based on your personality. You have this backstory: "${config.state.backStory}". Your knowledge base is: "${config.state.knowledgeBase}". The response should be one single sentence only.`;
}
```
- The personality is a string variable that describes the character's personality traits.
- The backStory is a string variable that describes the character's back story.
- The knowledgeBase is a string variable that describes the facts that the character would know.

## Prompt generator
In every user's turn, the user's input message <code>${message}</code> will be formatted into this structure:
```
{
    author: '0',
    content: `Please answer within 100 characters. {${message}}. The response must be based on the personality, backstory, and knowledge base that you have. The answer must be concise and short.`
}
```
The message is the user's input message.
Combined with the context, here is the final structure of the prompt sending to the LLM:
```
{
    prompt: {
        context: `Your task is to acting as a character that has this personality: "${config.state.personality}". Your response must be based on your personality. You have this backstory: "${config.state.backStory}". Your knowledge base is: "${config.state.knowledgeBase}". The response should be one single sentence only.`,
        messages: [
            {
                author: '0',
                content: `Please answer within 100 characters. {${message}}. The response must be based on the personality, backstory, and knowledge base that you have. The answer must be concise and short.`
            },
            ...
        ]
    },
    temperature: 0.25,
    candidate_count: 1,
}
```
- The messages is an array of chat messages from past to present alternating between the user (author=0) and the LLM (author=1). The first message is always from the user.
- The temperature is a float number between 0 and 1. The higher the temperature, the more creative the response will be. The lower the temperature, the more likely the response will be a correct one.
- The candidate_count is the number of responses that the LLM will return.

