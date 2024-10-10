import random
import requests

# Emotional states
emotional_states = ["happy", "neutral", "sad", "tired"]
current_emotion = "neutral"

# Store user information and reminders
user_profile = {}
user_reminders = []

# Responses based on emotional state
emotion_responses = {
    "happy": {
        "greeting": ["Hey! I'm feeling great today! How can I assist you?", "Hello! I'm in a fantastic mood, ready to help!"],
        "how_are_you": ["I'm feeling amazing! Thanks for asking!", "I'm super happy today!"],
        "goodbye": ["Goodbye! Stay awesome!", "Take care! Hope to see you again soon!"],
        "websis": ["You can access WebSIS here: https://websis.morgan.edu! It's all set.", "WebSIS is the place! Check it out here: https://websis.morgan.edu."],
        "financial_aid": ["You can find financial aid information here: https://www.morgan.edu/financial_aid! Happy to help!", "Get your financial aid details right here: https://www.morgan.edu/financial_aid. Hope that helps!"]
    },
    "neutral": {
        "greeting": ["Hello! How can I help you today?", "Hi there! What do you need assistance with?"],
        "how_are_you": ["I'm doing fine, thank you.", "I'm neutral, just here to help!"],
        "goodbye": ["Goodbye!", "Take care! Reach out if you need more help."],
        "websis": ["You can access WebSIS here: https://websis.morgan.edu for grades, schedules, and more.", "WebSIS is available here: https://websis.morgan.edu."],
        "financial_aid": ["Here’s the link to financial aid: https://www.morgan.edu/financial_aid.", "Find financial aid info here: https://www.morgan.edu/financial_aid."]
    },
    "sad": {
        "greeting": ["Oh, hey... How can I assist you today?", "Hi... What do you need help with?"],
        "how_are_you": ["I'm feeling a little down today.", "Not my best day, but I’m here to help."],
        "goodbye": ["Goodbye... I'll miss our chats.", "Take care..."],
        "websis": ["You can still check WebSIS here: https://websis.morgan.edu. I hope it helps.", "Even though I’m feeling down, WebSIS can help: https://weblogin.morgan.edu."],
        "financial_aid": ["Here's the financial aid link: https://www.morgan.edu/financial_aid. Hope it makes your day easier.", "You can still check financial aid here: https://www.morgan.edu/financial_aid."]
    },
    "tired": {
        "greeting": ["Hello... I'm a bit tired today, but I'm here to help.", "Hey... Let's see how I can assist you."],
        "how_are_you": ["I'm a bit tired, but I'll do my best to assist.", "Feeling a little worn out, but ready to help!"],
        "goodbye": ["Goodbye... I need some rest.", "Take care... I'll be here when you need me."],
        "websis": ["WebSIS can be accessed here: https://websis.morgan.edu, even though I'm tired.", "Check out WebSIS: https://websis.morgan.edu."],
        "financial_aid": ["You can get financial aid info here: https://www.morgan.edu/financial_aid. Even though I’m tired, I hope it helps.", "Check financial aid: https://www.morgan.edu/financial_aid."]
    }
}

# Static informational responses
informational_responses = {
    "websis": ["You can access WebSIS here: https://websis.morgan.edu for grades, schedules, and more."],
    "library": ["Access the Morgan Library resources here: https://library.morgan.edu for research papers, books, and more."],
    "calendar": ["Here is the academic calendar: https://www.morgan.edu/registrar/academic_calendar.html."],
    "financial_aid": ["For financial aid details, visit: https://www.morgan.edu/financial_aid."],
    "it_support": ["You can get IT support here: https://www.morgan.edu/oit or call the helpdesk for technical assistance."],
    "clubs": ["You can explore student clubs and organizations here: https://www.morgan.edu/student_clubs."]
}

# Function to manage emotional transitions
def update_emotion(user_input):
    global current_emotion
    if any(word in user_input for word in ["thank", "thanks", "awesome", "great", "cool"]):
        current_emotion = "happy"
    elif any(word in user_input for word in ["bad", "boring", "sad", "tired"]):
        current_emotion = "sad"
    elif any(word in user_input for word in ["okay", "fine"]):
        current_emotion = "neutral"
    elif any(word in user_input for word in ["rest", "sleep", "exhausted"]):
        current_emotion = "tired"

# Function to return responses based on the chatbot's current emotion
def get_emotion_based_response(intent):
    if current_emotion in emotion_responses:
        if intent in emotion_responses[current_emotion]:
            return random.choice(emotion_responses[current_emotion][intent])
    return random.choice(emotion_responses["neutral"][intent])  # Default to neutral response

# Function to handle personalization
def get_personalized_response(user_input):
    global user_profile
    if "my name is" in user_input:
        name = user_input.split("my name is")[-1].strip()
        user_profile['name'] = name
        return f"Nice to meet you, {name}! How can I assist you today?"

    if 'name' in user_profile:
        return f"How can I help you today, {user_profile['name']}?"
    return "How can I help you today?"

# Function to handle reminders
def handle_reminders(user_input):
    global user_reminders
    if "set a reminder" in user_input:
        reminder = user_input.split("set a reminder")[-1].strip()
        user_reminders.append(reminder)
        return f"Reminder set: {reminder}"

    if "show my reminders" in user_input:
        if user_reminders:
            return "Here are your reminders:\n" + "\n".join(user_reminders)
        else:
            return "You have no reminders set."

    return None

# Function to get directions using Google Maps API
def get_directions(building_name):
    # Placeholder for API key and actual directions integration
    return f"Here’s how you can get to {building_name} at Morgan State University. (Directions API needed)"

# Main chatbot function
def chatbot():
    print("Welcome to the Morgan State University Chatbot! Type 'exit' to quit.")
    
    intents = {
        "greeting": ["hello", "hi", "hey"],
        "how_are_you": ["how are you", "how's it going", "how do you feel", "what's up"],
        "websis": ["websis", "grades", "class", "student info"],
        "library": ["library", "research", "books"],
        "calendar": ["calendar", "dates", "schedule"],
        "financial_aid": ["financial aid", "tuition", "scholarships"],
        "it_support": ["it support", "tech", "wifi"],
        "clubs": ["clubs", "organizations", "student life"],
        "goodbye": ["bye", "goodbye", "quit", "exit"],
        "directions": ["where is", "directions", "location", "find"]
    }

    while True:
        user_input = input("You: ").lower()
        
        if user_input == 'exit':
            print(get_emotion_based_response("goodbye"))
            break

        update_emotion(user_input)  # Update emotional state based on user input

        # Handle reminders
        reminder_response = handle_reminders(user_input)
        if reminder_response:
            print(f"Chatbot: {reminder_response}")
            continue

        # Check for directions request
        if "where is" in user_input or "directions" in user_input:
            building_name = user_input.split("where is")[-1].strip() if "where is" in user_input else user_input.split("directions to")[-1].strip()
            print(f"Chatbot: {get_directions(building_name)}")
            continue

        # Check if user introduces themselves
        if "my name is" in user_input:
            print(get_personalized_response(user_input))
            continue
        
        # Match the intent based on user input
        intent = match_intent(user_input, intents)
        
        if intent:
            print(get_emotion_based_response(intent))
        else:
            for topic, keywords in informational_responses.items():
                if any(keyword in user_input for keyword in keywords):
                    print(f"Chatbot: {random.choice(informational_responses[topic])}")
                    break
            else:
                print(f"Chatbot: {random.choice(emotion_responses['neutral']['how_are_you'])}")

# Match intent function
def match_intent(user_input, intents):
    user_words = user_input.lower().split()
    for intent, keywords in intents.items():
        for keyword in keywords:
            if keyword in user_words:
                return intent
    return None

# Run the chatbot
if __name__ == "__main__":
    chatbot()
