from flask import Flask, request
import openai


app = Flask(__name__)

api_key = "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"

openai.api_key = api_key

def generateImage(story):
  messagesForImage = []
  imageGenPrompt = "Using the above description, write a prompt for an image generation AI to depict this scene."
  messagesForImage.append({"role": "assistant", "content": story})
  messagesForImage.append({"role": "user", "content": imageGenPrompt})

  imageGenResponse = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messagesForImage)
  promptForImage = "anime like art " + imageGenResponse["choices"][0]["message"]["content"]



  dalleresponse = openai.Image.create(prompt=promptForImage, 
    n=1,
    size="512x512")
  
  displayPicture = dalleresponse['data'][0]['url']



  # b64=dalleresponse['data']['b64_json']
  # with open(f'image_{iteration}.png', 'wb') as f:
  #   f.write(base64.urlsafe_b64decode(b64))

  return displayPicture

@app.route('/api/initialize')
def initialize():
    messages = []
    initialPrompt = "Briefly describe a random historical event, as the starting of a story."
    messages.append({"role": "user", "content": initialPrompt})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=messages)
    story = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": story})
    picture_url = generateImage(story)
    return {'messages': messages, 'story_text': story, 'image_url': picture_url}

@app.route('/api/continue', methods=['POST'])
def continueStory():
  messages = list(request.json['messages'])
  words = []
  word1 = request.json['word_1']
  word2 = request.json['word_2']
  word3 = request.json['word_3']
  words.append(word1)
  words.append(word2)
  words.append(word3)

  inputHandlingPrompt = f'Incorporating these three things, briefly continue the story you were describing before further in the form of a thriller: "{words[0]}, {words[1]}, {words[2]}". Use simple language. Keep the text under 150 words.'
  # conclude inputHandlingPrompt = f'Incorporating these three words, briefly conclude story you were describing before further in the form of a thriller: "{words[0]}, {words[1]}, {words[2]}". Use simple language. Keep the text under 150 words.'
  messages_mod = messages.copy()
  messages_mod.append({"role": "user", "content": inputHandlingPrompt})
  response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=messages_mod)
  story = response["choices"][0]["message"]["content"]
  messages.append({"role": "assistant", "content": story})
  dp = generateImage(story)
  return {'messages': messages, 'story_text': story, 'image_url': dp}

@app.route('/api/test')
def test():
   return {'text': 'texxt output'}

