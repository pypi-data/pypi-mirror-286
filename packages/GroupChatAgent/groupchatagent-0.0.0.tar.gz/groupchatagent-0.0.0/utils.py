from firebase_admin import storage, firestore
from src.package_DEIDARA285231.firestore_client_singleton import FirestoreClientSingleton
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
import os
from datetime import datetime, date

def save_groupchat_messages(user_id, agent_id, session_id, session_name, final_output):
    db = FirestoreClientSingleton().client
    
    message_id = save_message_firestore(user_id, agent_id, session_id, session_name, final_output)

    update_big_query(user_id, agent_id, session_id, final_output)
    
    save_statistics(final_output["stats"]["wordsPrompt"] + final_output["stats"]["wordsOutput"], user_id, agent_id, session_id)

    counter = update_chatbot_counter(user_id, agent_id, session_id)

    doc_ref = (
        db.collection("users")
        .document(user_id)
        .collection("agents")
        .document(agent_id)
        .collection("sessions")
        .document(session_id)
    )
    update_feedback_counters(doc_ref, 0, 0)
    
    doc_ref = (
        db.collection("users")
        .document(user_id)
        .collection("agents")
        .document(agent_id)
    )
    update_feedback_counters(doc_ref, 0, 0)
    

def save_message_firestore(user_id, agent_id, session_id, session_name, final_output):
    """
    Saves a message to Firestore under the specified user, agent, and session.

    Parameters:
        user_id (str): Identifier for the user.
        agent_id (str): Identifier for the agent.
        session_id (str): Identifier for the session.
        final_output (dict): The final output to be saved, with an added timestamp.
    """
    # Instantiate the firestore database reference
    db = FirestoreClientSingleton().client
    agent_ref = (
        db.collection("users")
        .document(user_id)
        .collection("agents")
        .document(agent_id)
        .collection("sessions")
        .document(session_id)
    )

    # Retrieves the reference to the document
    # of the given agent_id and user_id
    agent_doc = agent_ref.get()
    if agent_doc.exists:
        message_ref = agent_ref.collection("messages")
        if not message_ref.get():
            message_ref = agent_ref.collection("messages")

        message_ref = message_ref.document()
        final_output_with_timestamp = final_output.copy()
        # Adds a timestamp to the final output of the model
        final_output_with_timestamp["timestamp"] = firestore.SERVER_TIMESTAMP
        final_output_with_timestamp["id"] = message_ref.id
        message_ref.set(final_output_with_timestamp)
        print("Message was successfully saved.")
    else:
        agent_ref = (
            db.collection("users")
            .document(user_id)
            .collection("agents")
            .document(agent_id)
            .collection("sessions")
            .document(session_id)
        )

        agent_ref.set({})
        
        agent_ref.update({"first_message_timestamp": firestore.SERVER_TIMESTAMP})
        agent_ref.update({"session_name": session_name})
        agent_ref.update({"deleted": False})

        message_ref = agent_ref.collection("messages")
        message_ref = message_ref.document()
        final_output_with_timestamp = final_output.copy()
        final_output_with_timestamp["timestamp"] = firestore.SERVER_TIMESTAMP
        final_output_with_timestamp["id"] = message_ref.id
        message_ref.set(final_output_with_timestamp)
        print("Message was successfully saved.")
    
    return message_ref.id



def update_big_query(user_id, agent_id, session_id, final_output):
    client = bigquery.Client(project=os.getenv('PROJECT_NAME'))
    
    #table_id = f"{os.getenv('PROJECT_NAME')}.{os.getenv('DATASET')}.{user_id}"

    schema = [
        bigquery.SchemaField("prompt", "STRING", mode="REQUIRED", max_length=5000),
        bigquery.SchemaField("question", "STRING", mode="REQUIRED", max_length=5000),
        bigquery.SchemaField("reply", "STRING",  mode="REQUIRED", max_length=5000),
        bigquery.SchemaField("date", "DATE",  mode="REQUIRED"),
        bigquery.SchemaField("session", "STRING",  mode="REQUIRED"),
        bigquery.SchemaField("agent_id", "STRING",  mode="REQUIRED")
    ]
    
    dataset_ref = client.dataset(os.getenv('DATASET'))
    table_ref = dataset_ref.table(user_id)

    try:
        # Verifica se la tabella esiste
        client.get_table(table_ref)
        print(f"Table {user_id} already exists.")
    except NotFound:
        # Crea la tabella se non esiste
        table = bigquery.Table(table_ref, schema=schema)
        client.create_table(table)
        print(f"Table {user_id} created.")

    rows_to_insert = [
        {"prompt": final_output["why"]["Behavior"], "question": final_output["why"]["HumanInput"], "reply": final_output["content"], "date": (datetime.now().strftime("%Y-%m-%d")), "session": session_id, "agent_id": agent_id}
    ]

    errors = client.insert_rows_json(f"{os.getenv('PROJECT_NAME')}.{os.getenv('DATASET')}.{user_id}", rows_to_insert)  # Make an API request.
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))
        


def save_statistics(words, user_id, agent_id, session_id):
    """
    Successfully saves statistics on firebase after a message
    has been generated.

    Parameters:
        words (str): How many words have been used.
        user_id (str): Identifier of the user.
        agent_id (str): Identifier of the agent.
        session_id (str): Identifier of the session.
    """
    # Update "Global" statistics
    db = FirestoreClientSingleton().client
    user_doc_ref = db.collection("users").document(user_id)

    user_doc = user_doc_ref.get()
    if user_doc.exists:
        transaction = db.transaction()

        update_stats(transaction=transaction, doc_ref=user_doc_ref, words=words)

    # Update "Agent" statistics
    agent_doc_ref = (
        db.collection("users").document(user_id).collection("agents").document(agent_id)
    )
    agent_doc = agent_doc_ref.get()
    if agent_doc.exists:
        transaction = db.transaction()

        update_stats(transaction=transaction, doc_ref=agent_doc_ref, words=words)

    # Update "Session" statistics
    session_doc_ref = (
        db.collection("users")
        .document(user_id)
        .collection("agents")
        .document(agent_id)
        .collection("sessions")
        .document(session_id)
    )

    session_doc = session_doc_ref.get()
    if session_doc.exists:
        transaction = db.transaction()

        update_stats(transaction=transaction, doc_ref=session_doc_ref, words=words)

    update_msg_stats_chatbot(agent_id=agent_id, user_id=user_id)
    
    
def update_chatbot_counter(user_id, agent_id, session_id):
    """
    This function sets the message counter for a given
    user_id, agent_id and session.

    Parameters:
        user_id (str) : Identifier of the user.
        agent_id (str) : Identifier of the agent.
        session_id (str) : Identifier of the session.
    """

    # Instantiate the firestore database reference
    db = FirestoreClientSingleton().client
    agent_ref = (
        db.collection("users")
        .document(user_id)
        .collection("agents")
        .document(agent_id)
        .collection("sessions")
        .document(session_id)
    )

    try:
        transaction = db.transaction()
        counter = update_msg_counter(transaction=transaction, doc_ref=agent_ref)
    except:
        raise Exception("Unknown chatbot")

    return counter


def update_feedback_counters(doc_ref, current_feedback, new_feedback):
    doc = doc_ref.get()
    feedback = doc.to_dict().get('feedback', {'positive': 0, 'negative': 0, 'neutral': 0})

    if new_feedback == 1:
        feedback['positive'] += 1
        if current_feedback == 0:
            feedback['neutral'] = max(0, feedback['neutral'] - 1)
        elif current_feedback == -1:
            feedback['negative'] = max(0, feedback['negative'] - 1)
    elif new_feedback == -1:
        feedback['negative'] += 1
        if current_feedback == 0:
            feedback['neutral'] = max(0, feedback['neutral'] - 1)
        elif current_feedback == 1:
            feedback['positive'] = max(0, feedback['positive'] - 1)
    elif new_feedback == 0:
        feedback['neutral'] += 1
        if current_feedback == 1:
            feedback['positive'] = max(0, feedback['positive'] - 1)
        elif current_feedback == -1:
            feedback['negative'] = max(0, feedback['negative'] - 1)

    doc_ref.update({'feedback': feedback})


@firestore.transactional
def update_stats(transaction, doc_ref, words):
    """
    Updates stats for a given document.

    Parameters:
        transaction : Firebase transaction.
        doc_ref : Reference to the document inside firebase.
        words (str): How many words have been used.
    """
    data = doc_ref.get(transaction=transaction)

    if data.exists:
        data_dict = data.to_dict()
        statistics = data_dict.get("Statistics", {})

        if "total_words" in statistics:
            statistics["total_words"] += words
        else:
            statistics["total_words"] = words

        if "total_calls" in statistics:
            statistics["total_calls"] += 1
        else:
            statistics["total_calls"] = 1

        transaction.update(doc_ref, {"Statistics": statistics})
        
        

@firestore.transactional
def update_msg_counter(transaction, doc_ref):
    """
    This function updates the message counter.

    Parameters:
        transaction : Firebase transaction.
        doc_ref : Reference to the document inside firebase.
    """
    snapshot = doc_ref.get(transaction=transaction)

    if "messages_sent" in snapshot.to_dict():
        current_count = snapshot.get("messages_sent")
        transaction.update(doc_ref, {"messages_sent": current_count + 1})
    else:
        transaction.set(doc_ref, {"messages_sent": 1}, merge=True)
        current_count = 0
    return current_count + 1


def update_msg_stats_chatbot(agent_id, user_id):
    """
    Updates the message stats for a given chatbot.

    Parameters:
        agent_id (str) : Identifier of the agent.
        user_id (str) : Identifier of the user.
    """
    current_date = datetime.today().date().strftime("%Y-%m-%d")

    db = FirestoreClientSingleton().client

    agent_doc_ref = (
        db.collection("users").document(user_id).collection("agents").document(agent_id)
    )

    statistics = agent_doc_ref.get().to_dict().get("Statistics", {})
    value = statistics.get("msgs_counters", {}).get(current_date, 0)

    data = {"Statistics": {"msgs_counters": {current_date: (value + 1)}}}

    try:
        transaction = db.transaction()
        update_msg_counters_chatbot(
            transaction=transaction, doc_ref=agent_doc_ref, data=data
        )
    except Exception as e:
        print(str(e))
        

@firestore.transactional
def update_msg_counters_chatbot(transaction, doc_ref, data):
    """
    Updates the message counter for a given chatbot.

    Parameters:
        transaction : Firebase transaction.
        doc_ref : Reference to the document inside firebase.
        data :
    """
    transaction.set(doc_ref, data, merge=True)