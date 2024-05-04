from utils import ask_ai
from utils import get_example
import sqlite3

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

# %%
def is_similar(entity1: str, entity2: str) -> bool:
    response = ask_ai(f"Do the strings '{entity1}' and '{entity2}' refer to the same entity? Please answer 'yes', 'no', or 'unsure' only.")

    response = response.lower()

    if "yes" in response:
        return True
    elif "no" in response:
        return False
    
    entity1_example = get_example(entity1)
    entity2_example = get_example(entity2)
    
    new_prompt = "Do the strings '{entity1}' and '{entity2}' refer to the same entity? Please answer 'yes', 'no', or 'unsure' only. \
    Here is an example of {entity1}: {entity1_example}. \n\nHere is an example of {entity2}: {entity2_example}."

    response = ask_ai(new_prompt)

    response = response.lower()

    if "yes" in response:
        return True
    elif "no" in response:
        return False
    
    return False
# %%
def coalesce_entities(conn: sqlite3.Connection):
    # get the names of entities from the entities table where "canonical" is False
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM entities WHERE canonical = False")
    entities = cursor.fetchall()
    cursor.close()

    # look at entities where "canonical" is True and see if they are similar to any entities where "canonical" is False
    for entity in entities:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM entities WHERE canonical = True")
        for row in cursor:
            canonical_entity = row[0]
            if is_similar(entity, canonical_entity):
                # go through the snippets table and replace the entity with the canonical entity
                cursor.execute("SELECT snippet FROM snippets WHERE entity = ?", (entity,))
                for row in cursor:
                    snippet = row[0]
                    snippet = snippet.replace(entity, canonical_entity)
                    cursor.execute("UPDATE snippets SET snippet = ? WHERE entity = ?", (snippet, entity))
                # delete the entity from the entities table
                cursor.execute("DELETE FROM entities WHERE name = ?", (entity,))
        cursor.close()

# %%

