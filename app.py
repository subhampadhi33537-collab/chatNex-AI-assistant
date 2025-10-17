# # Dynamically import flask to avoid static-analysis "could not be resolved" errors
# try:
#     import importlib
#     _flask_mod = importlib.import_module('flask')
#     Flask = getattr(_flask_mod, 'Flask')
#     request = getattr(_flask_mod, 'request')
#     jsonify = getattr(_flask_mod, 'jsonify')
# except Exception:
#     # If Flask is not installed, provide clear runtime errors while keeping static-analysis happy.
#     def _missing_flask(*args, **kwargs):
#         raise RuntimeError("Flask is not installed. Install it with 'pip install flask' to run the server.")
#     Flask = _missing_flask

#     class _RequestProxy:
#         def get_json(self):
#             raise RuntimeError("Flask is not installed; request.get_json is unavailable.")
#     request = _RequestProxy()

#     def jsonify(obj):
#         raise RuntimeError("Flask is not installed; jsonify is unavailable.")
# # Dynamically import flask_cors to avoid static-analysis "could not be resolved" errors
# try:
#     import importlib
#     flask_cors = importlib.import_module('flask_cors')
#     CORS = getattr(flask_cors, 'CORS')
# except Exception:
#     # Fallback lightweight CORS implementation if flask_cors is not installed
#     def CORS(app, resources=None, **kwargs):
#         @app.after_request
#         def _cors_response(response):
#             response.headers['Access-Control-Allow-Origin'] = '*'
#             response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
#             response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
#             return response

# from google import genai
# import os
# # Dynamically import python-dotenv to avoid static-analysis "could not be resolved" errors
# try:
#     import importlib
#     _dotenv_mod = importlib.import_module('dotenv')
#     load_dotenv = getattr(_dotenv_mod, 'load_dotenv')
# except Exception:
#     # Fallback simple .env loader if python-dotenv is not installed
#     def load_dotenv(dotenv_path='.env', *args, **kwargs):
#         try:
#             if not os.path.exists(dotenv_path):
#                 return False
#             with open(dotenv_path, 'r', encoding='utf-8') as f:
#                 for line in f:
#                     line = line.strip()
#                     if not line or line.startswith('#'):
#                         continue
#                     if '=' in line:
#                         key, val = line.split('=', 1)
#                         val = val.strip().strip('"').strip("'")
#                         os.environ.setdefault(key.strip(), val)
#             return True
#         except Exception:
#             return False

# # Load environment variables from .env file
# load_dotenv()

# # Initialize Flask app
# app = Flask(__name__)

# # Enable CORS for all routes (allows your HTML frontend to communicate with backend)
# CORS(app)

# # Configure Gemini API
# api_key = os.getenv("GEMINI_API_KEY")
# if not api_key:
#     raise ValueError("GEMINI_API_KEY not found in environment variables!")

# # Initialize Gemini client
# client = genai.Client(api_key=api_key)

# # Store chat sessions in memory (keyed by session ID)
# # For production, consider using Redis or database
# chat_sessions = {}

# @app.route('/chat', methods=['POST'])
# def chat():
#     """
#     Main chat endpoint that receives user messages and returns AI responses
#     """
#     try:
#         # Get message from request
#         data = request.get_json()
        
#         if not data or 'message' not in data:
#             return jsonify({'error': 'No message provided'}), 400
        
#         user_message = data['message'].strip()
        
#         if not user_message:
#             return jsonify({'error': 'Empty message'}), 400
        
#         # Get or create session ID (optional: use for multi-user support)
#         session_id = data.get('session_id', 'default')
        
#         # Create new chat session if doesn't exist
#         if session_id not in chat_sessions:
#             chat_sessions[session_id] = client.chats.create(
#                 model='gemini-1.5-flash'  # Free tier model
#             )
        
#         chat_session = chat_sessions[session_id]
        
#         # Send message and get response with conversation history
#         response = chat_session.send_message(user_message)
        
#         # Extract text from response
#         bot_reply = response.text
        
#         return jsonify({
#             'reply': bot_reply,
#             'session_id': session_id
#         }), 200
        
#     except Exception as e:
#         print(f"Error in chat endpoint: {str(e)}")
#         return jsonify({
#             'error': f'An error occurred: {str(e)}'
#         }), 500


# @app.route('/reset', methods=['POST'])
# def reset_chat():
#     """
#     Optional endpoint to reset chat history for a session
#     """
#     try:
#         data = request.get_json()
#         session_id = data.get('session_id', 'default')
        
#         if session_id in chat_sessions:
#             del chat_sessions[session_id]
#             return jsonify({'message': 'Chat history reset successfully'}), 200
        
#         return jsonify({'message': 'No active session found'}), 404
        
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# @app.route('/health', methods=['GET'])
# def health_check():
#     """
#     Health check endpoint to verify server is running
#     """
#     return jsonify({'status': 'healthy', 'message': 'ChatNex backend is running!'}), 200


# if __name__ == '__main__':
#     print("🚀 Starting ChatNex backend server...")
#     print(f"✅ Gemini API configured")
#     print(f"🌐 Server running on http://127.0.0.1:5000")
#     app.run(host='0.0.0.0', port=5000, debug=True)


# app.py

# Dynamically import flask to avoid static-analysis errors




# Dynamic Flask, CORS, and dotenv imports for compatibility/static analysis
try:
    import importlib
    _ngrok_mod = importlib.import_module('pyngrok')
    ngrok = getattr(_ngrok_mod, 'ngrok')
    # Open a tunnel on port 5000
    public_url = ngrok.connect(5000)
    print("Ngrok URL:", public_url)
except Exception:
    # pyngrok not installed; fallback stub that mimics connect()
    class _NgrokStub:
        def connect(self, port):
            print("pyngrok not installed; skipping ngrok tunnel.")
            return f"http://127.0.0.1:{port}"
    ngrok = _NgrokStub()
    public_url = ngrok.connect(5000)
    print("Ngrok URL (local):", public_url)

# Then start your Flask app as usual

try:
    import importlib
    _flask_mod = importlib.import_module('flask')
    Flask = getattr(_flask_mod, 'Flask')
    request = getattr(_flask_mod, 'request')
    jsonify = getattr(_flask_mod, 'jsonify')
except Exception:
    def _missing_flask(*args, **kwargs):
        raise RuntimeError("Flask is not installed. Install it with 'pip install flask'.")
    Flask = _missing_flask
    class _RequestProxy:
        def get_json(self):
            raise RuntimeError("Flask missing; request.get_json unavailable.")
    request = _RequestProxy()
    def jsonify(obj):
        raise RuntimeError("Flask missing; jsonify unavailable.")

try:
    flask_cors = importlib.import_module('flask_cors')
    CORS = getattr(flask_cors, 'CORS')
except Exception:
    def CORS(app, resources=None, **kwargs):
        @app.after_request
        def _cors_response(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
            response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
            return response

from google import genai
import os
try:
    _dotenv_mod = importlib.import_module('dotenv')
    load_dotenv = getattr(_dotenv_mod, 'load_dotenv')
except Exception:
    def load_dotenv(dotenv_path='.env', *args, **kwargs):
        try:
            if not os.path.exists(dotenv_path):
                return False
            with open(dotenv_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        key, val = line.split('=', 1)
                        val = val.strip().strip('"').strip("'")
                        os.environ.setdefault(key.strip(), val)
            return True
        except Exception:
            return False

# Load environment vars
load_dotenv()
app = Flask(__name__)
CORS(app)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables!")

client = genai.Client(api_key=api_key)
chat_sessions = {}

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        session_id = data.get('session_id', 'default')
        # USE THE LATEST SUPPORTED MODEL HERE:
        if session_id not in chat_sessions:
            chat_sessions[session_id] = client.chats.create(
                model='gemini-2.5-flash'  # This is the current supported model name
            )
        chat_session = chat_sessions[session_id]
        response = chat_session.send_message(user_message)
        bot_reply = response.text
        return jsonify({'reply': bot_reply, 'session_id': session_id}), 200
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/reset', methods=['POST'])
def reset_chat():
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default')
        if session_id in chat_sessions:
            del chat_sessions[session_id]
            return jsonify({'message': 'Chat history reset successfully'}), 200
        return jsonify({'message': 'No active session found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'ChatNex backend is running!'}), 200

if __name__ == '__main__':
    print("🚀 Starting ChatNex backend server...")
    print(f"✅ Gemini API configured")
    print(f"🌐 Server running on http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
