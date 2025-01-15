import json


def save_to_file(data, filename):
    with open(f"{filename}.json", "a") as f:
        json.dump(data, f)

def load_from_file(filename):
    try:
        with open(f"{filename}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    
def load_user_data(filename):
    try:
        with open(f"{filename}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # If the file does not exist, return an empty dictionary
    except Exception as e:
        print(f"Error loading user data: {e}")
        return {}
    
def save_user_data(user_id, currency, filename):
    try:
        # Load existing data
        data = load_user_data(filename)
        
        # Update user data
        data[str(user_id)] = currency
        
        # Save updated data back to the file
        with open(f"{filename}.json", "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Error saving user data: {e}")