import openai
import streamlit as st
import requests
import os

# Set up OpenAI API credentials
openai.api_key = os.environ.get('OPENAPI_API_KEY')

# Set up Streamlit app
st.title("DeezerGPT")
prompt = st.text_input("Describe your mix:")
st.write("Examples:")
st.caption("""
* _touareg morrocan music_
* _songs similar to simon and garfunkel, but with harmonica_
* _party songs from the 80s with only female singers_
* _90s pop hits, only boys bands_
* _punk songs that can be listened by kids_
* _songs from albums produced by steve albini_
* _a playlist to break up with someone_
""")


query = "I want you to create a playlist for me containing 20 songs. Each song of the playlist should be written on a separate line with this format: artist name and song title are separated by a | character, don't use bullet points or numbered list. The playlist should match the following description:\n\n"

# Generate answer with OpenAI GPT API
if prompt:
    print(prompt)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=query + prompt + "\n\n",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    
    # display raw response for debugging
    debug = response.choices[0].text.replace("\n", " -- ")
    st.write("raw result:")
    st.write(debug)
    print(response.choices[0].text)

    playlist = response.choices[0].text.strip().split("\n")
    
    deezer_ids = []
    for track in playlist:
        try:
            # Extract artist name and song title from playlist entry
            artist_name, song_title = [ token.strip() for token in track.split("|")[0:2] ]
            # Search for track with Deezer API
            url = "https://api.deezer.com/search/?q=" + f"artist:'{artist_name} 'track:'{song_title}'&limit=1"
            print(url)
            response = requests.get(url)
            data = response.json()

            if data["data"]:
                deezer_id = data["data"][0]["id"]
                deezer_ids.append(deezer_id)
        except Exception as e:
            print(e)
            print("search error with track: ", track)
            pass
        
    print(deezer_ids)
    deezer_ids_str = ','.join([ str(id) for id in deezer_ids])

    # Display Deezer player widget
    st.write("Player:")
    st.write(
        f'<iframe scrolling="no" frameborder="0" allowTransparency="true" src="https://widget.deezer.com/widget/dark/tracks/{deezer_ids_str}" width="700" height="480"></iframe>',
        unsafe_allow_html=True,
    )
