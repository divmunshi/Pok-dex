import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd 
import requests

st.title("Pokémon Explorer")

@st.cache_data
def get_details(poke_number):
    ''' Create an entry for our favorite Pokémon '''
    try:
        url = f'https://pokeapi.co/api/v2/pokemon/{poke_number}/'
        response = requests.get(url)
        pokemon = response.json()
        # Extract the types of the Pokémon
        types = [type_info['type']['name'] for type_info in pokemon['types']]
        # Extract the sprites
        sprites = pokemon['sprites']
        # Extract stats
        stats = pokemon['stats']
        # Get the URL of the latest Pokémon cry, ensuring key exists
        latest_cry_url = pokemon.get('cries', {}).get('latest', '')
        return pokemon['name'], pokemon['height'] * 10, pokemon['weight'], len(pokemon['moves']), types, latest_cry_url, sprites, stats
    except Exception as e:
        st.error(f"Failed to fetch details: {e}")  # Improved error handling
        return 'Error', None, None, None, [], None, None, []
    
@st.cache_data
def get_type_colors():
    unique_types = set()
    # Assuming you are using a range that covers all your Pokémon types
    for poke_number in range(1, 1026):  # You can adjust this range as needed
        name, height, weight, moves, types, latest_cry_url, sprites, stats = get_details(poke_number)
        unique_types.update(types)
    # Generating a color for each unique type
    colors = sns.color_palette('husl', n_colors=len(unique_types)).as_hex()
    return dict(zip(unique_types, colors))


# Update the range according to your data or requirements
pokemon_number = st.number_input("Enter Pokémon ID", min_value=1, max_value=1025, value=1, step=1)
if st.button('Get Pokémon Details'):
    name, height, weight, moves, types, latest_cry_url, sprites, stats = get_details(pokemon_number)

    if name != 'Error':
        # Display Pokémon information
        st.write(f'**Name:** {name.title()}')
        st.write(f'**Height:** {height} cm')
        st.write(f'**Weight:** {weight} kg')
        st.write(f'**Number of Moves:** {moves}')
        st.write('**Types:**', ', '.join([t.title() for t in types]))

        # Display the latest cry audio if available
        if latest_cry_url:
            st.audio(latest_cry_url)

        # Displaying Pokémon stats
        st.subheader("Stats:")
        cols = st.columns(len(stats))  # Dynamic creation of columns based on stats count
        for col, stat in zip(cols, stats):
            col.metric(stat['stat']['name'].replace('-', ' ').title(), stat['base_stat'])

        # Display official artwork if available
        if sprites and 'official-artwork' in sprites['other']:
            st.image(sprites['other']['official-artwork']['front_default'], caption=f'{name.title()} - Official Artwork')

        # Display type colors (if applicable)
        type_colors = get_type_colors()
        type_color_palette = [type_colors.get(t, 'gray') for t in types]
        height_data = {'Pokemon': ['Weedle', name.title(), 'Victreebel'],
               'Heights': [30, height, 200]}
        sns.barplot(data=height_data, x='Pokemon', y='Heights', palette=type_color_palette)
        st.pyplot(plt.gcf())  # Display the created figure in Streamlit
    else:
        st.error("Failed to retrieve Pokémon details. Please check the ID and try again.")
