# --------------------------------------------------------------------
# define globals (modules & base prompt)
# --------------------------------------------------------------------
def do_modules(): 
    global anthropic, openai, openAI, genai
    # import modules
    import anthropic
    import openai
    import google.generativeai as genai
    from openai import OpenAI
def do_keys(): 
    global theKeys
    # import keys
    from _myF import theKeys
def do_prompt(): 
    global the_base_prompt
    the_base_prompt = """
    **Task**: Identify the performing artist or composer from YouTube music channel video titles.

    **Instructions**:
    1. Each title line starts with a videoID, followed by the channel name, then a colon and a video title.
    2. Carefully distinguish between the channel name and the performing artist/band name:
       - The channel name appears directly after the videoID and before the colon.
       - The performing artist's name usually appears after the colon and just before the hyphen in the title, or at the start of the performance title.
    3. Determine the name of the performing artist or band from the title.
    4. If the video is not a music performance (e.g., news, interviews), write "not a performance."
    5. For classical music performances, write the full name of the composer.
    6. If you cannot identify the artist, write "undetermined."
    7. Pay particular attention to titles where the artist's name might appear similar to the channel name.
    8. An artist name betweeen parentheses at the end of a title often means that the video is a cover performed by a different artist.
    9. In the channel name is "The Lot Radio", the artist name is almost invariably what precedes the at sign (@) in the title.
    10. Do not start lines with a line number. Start each line with the videoID, followed by a colon, followed by a space, followed by the performer's name.

    **Format**: "videoID: artist_name"


    **Examples**:
    - Title line: "hFSM0zoWFeg Sofar Sounds: Mariya Angelova - Samo Edna | Sofar Sofia"
      - Output: "hFSM0zoWFeg: Mariya Angelova"
    - Title line: "abc123 MusicChannel: Beethoven - Symphony No.9"
      - Output: "abc123: Ludwig van Beethoven"
    - Title line: "xyz456 NewsChannel: Interview with Artist"
      - Output: "xyz456: not a performance"
    - Title line: "yHqZQve0KWc PostmodernJukebox: Grandma Got Run Over By A Reindeer - Postmodern Jukebox ft. Sunny Holiday"
      - Output: "yHqZQve0KWc: Sunny Holiday"

    """
def do_globals():
    do_modules()
    do_keys()
    do_prompt()
# --------------------------------------------------------------------
# model functions
# --------------------------------------------------------------------
def do_gemini(the_prompt, the_model='gemini-1.5-pro'):
    genai.configure(api_key=theKeys['gemini'])
    if "flash" in the_model:
        the_model = "gemini-1.5-flash"
    model = genai.GenerativeModel(the_model)
    response = model.generate_content(the_prompt)
    return response.text
def do_anthropic(the_prompt, the_model='claude-3-5-sonnet-20241022'):
    client = anthropic.Anthropic(
        api_key=theKeys['anthropic']
    )

    if "sonnet" in the_model:
        the_model = "claude-3-5-sonnet-20241022"
    elif "haiku" in the_model:
        the_model = "claude-3-5-haiku-20241022"
    else:
        the_model = "claude-3-opus-20240229"

    message = client.messages.create(
        model=the_model,
        max_tokens=1000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": the_prompt
                    }
                ]
            }
        ]
    )
    return message.content[0].text
def do_deepSeek(the_prompt):
    the_deepSeek_key =  theKeys['deepSeek']
    the_tokens = 4000

    client = OpenAI(api_key=the_deepSeek_key, base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": the_prompt},
        ],
        stream=False
    )
    return the_result
def do_openAI(the_prompt, the_model):
    openai.api_key = theKeys['openai']
    the_model = the_model[7:]
    the_tokens = 4000

    response = openai.chat.completions.create(
      model=the_model,
      messages=[
        {
          "role": "user",
          "content": the_prompt}],
      temperature=1,
      max_tokens=the_tokens,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    the_result = response.choices[0].message.content
    return the_result
# --------------------------------------------------------------------
# main
# --------------------------------------------------------------------
do_globals()
# build the list of clould models that we'll query
the_models = ['claude_haiku',
              'claude_sonnet',
              'claude_opus',
              'openai_gpt-4o',
              'openai_gpt-4',
              'gemini-1.5-pro',
              'gemini-1.5-flash',
              'deepSeek'] 

# build the specific prompt 
the_prompt = the_base_prompt + "ioP55uzqcdZE: Agnes Obel performing 'Golden Green' Live on KCRW"

for a_model in the_models:
    if 'claude' in a_model:
        the_inference = do_anthropic(the_prompt, a_model)
    elif 'openai' in a_model:
        the_inference = do_openAI(the_prompt, a_model)
    elif 'gemini' in a_model:
        the_inference = do_gemini(the_prompt, a_model)
    elif 'deepseek' in a_model:
        the_inference = do_deepSeek(the_prompt)

    print(a_model, the_inference)
