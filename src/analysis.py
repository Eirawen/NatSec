from utils import ask_ai

def analyze_data(datapoint: str):
    prompt = "Identify any entities in this data (people, places, organizations, products, etc.) \
    and the sentiment associated with them. Provide your output in the following format: \
    {entity: '...', sentiment: '...'}\n\
    Where 'sentiment' is one of 'positive', 'negative', or 'neutral', and 'entity' is the name of the entity. \
    If the entity has a Wikipedia page, use the title of the page as the entity name, otherwise use your best guess of what \
    name the Wikipedia page would have if it existed. If the entity isn't consequential enough to meet Wikipedia's notability \
    guidelines, don't include it or include a broader category that it falls under. \
    \n\nData:\n" + data

    response = ask_ai(prompt)
    return response

# %%
def coalesce_entities(data: str, entities: dict):
    for entity in entities:
        data = data.replace(entity, entities[entity])
    return data

