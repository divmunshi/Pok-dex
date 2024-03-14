import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd 
import requests

st.title("Pokemon ex")

# Display image of pokemon, (latest sprite from front!)
# Stretch version > display the many sprites from the API
# make it look better
# add the audio of the latest battle cry
# use the whole pokedex!
# use the pokemon type to change colour of barchar!
#

# @st.cache_data
# def get_all_id_numbers():
    # codes to get all numbers
#     return list_of_all_numbers


def get_details(poke_number):
    ''' Create an entry for our favourite pokemon '''
    try:
        url = f'https://pokeapi.co/api/v2/pokemon/{poke_number}/'
        response = requests.get(url)
        pokemon = response.json()
        types = [type_info['type']['name'] for type_info in pokemon['types']]
        return pokemon['name'], pokemon['height'], pokemon['weight'], len(pokemon['moves']),types
    except:
        return 'Error', np.NAN, np.NAN, np.NAN  

pokemon_number = st.slider("Pick a pokemon", min_value=1, max_value=250)  
name, height, weight, moves, types = get_details(pokemon_number)
height = height * 10
height_data = {'Pokemon':['Weedle', name.title(), 'victreebel'],
               'Heights':[30, height, 200]}

# colors = {'bug':'green', 'grass': 'limegreen'}

# type_colors = [colors.get(t, 'gray') for t in types]

# Get all types and assign colors dynamically


def get_type_colors():
    unique_types = set()
    for poke_number in range(1, 251):  # Adjust range according to your data
        name, height, weight, moves, types = get_details(poke_number)
        unique_types.update(types)
    colors = sns.color_palette('husl', n_colors=len(unique_types)).as_hex()
    return dict(zip(unique_types, colors))

# Get type colors
type_colors = get_type_colors()

# Map colors based on the types of the chosen Pokemon
type_color_palette = [type_colors.get(t, 'gray') for t in types]

graph = sns.barplot(data = height_data,
                    x = 'Pokemon',
                    y = 'Heights',
                    palette= type_color_palette)

st.write(f'Name: {name}')
st.write(f'Height: {height}')
st.write(f'Weight: {weight}')
st.write(f'Moves: {moves}')
st.write(f'Type: {", ".join(types)}')

st.pyplot(graph.figure)
                  
