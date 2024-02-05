import streamlit as st
from streamlit_chat import message
import google.generativeai as genai
from utils import chat

st.set_page_config(
    page_title="Nidhi: An AI chatbot NITRR Edition",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Report a bug': "mailto:vkumar.btech2022.bme@nitrr.ac.in?subject=Bug%20Report%20in%20Pioneer%20Chat%20Application&body=Hey%2C%20I%20have%20found%20a%20bug%20in%20your%20WebApp%20%22Pioneer%20Chat%22.%20Here%20are%20the%20details%20of%20the%20bug.%20also%2C%20I%20will%20attach%20the%20relevant%20docs%20or%20screenshots%20if%20it%20will%20be%20necessary.",
        'About': "# This is a Nidhi AI Chat Assistant. This is an *extremely* cool app!\n Developed by Nidhi and Vivek at MakerSpace NIT Raipur"
    }
)
st.markdown(f"""
    <style>
        #animated-text {{
            font-size: 60px;
            font-weight: bold;
            font-family: Arial, sans-serif;
            animation: color-change 6s infinite alternate;
        }}
        @keyframes color-change {{
            0% {{color: red;}}
            33% {{color: green;}}
            66% {{color: blue;}}
            100% {{color: red;}} /* Cycle back to red */
        }}
    </style>
    <div id="animated-text">WELCOME</div>
    <script>
        // JavaScript for animation control (optional)
        // You can use JavaScript to control more complex animations
    </script>
""", unsafe_allow_html=True)


st.caption("Nidhi: A Chatbot assistant Powered by Google Gemini Pro")  
with st.expander("ℹ️ Disclaimer"):
    st.caption(
        "We appreciate your engagement! Please note, this chatbot can also produce wrong response and limited data is provided to the chatbot."
    )
GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
with st.sidebar:
        st.header("Enter your own Gemini API Key")
        input_api_key = st.text_input("(ignore if you haven't, it still works)", key="input",type='password')
        enter_key = st.button("Apply the API key",use_container_width=True,type="secondary")
        st.info(" This is only in the case if the current API limit is reached which is max 1 query per sec. ")

        st.markdown("Click [here](https://makersuite.google.com/app/apikey) to get your own API Key.", unsafe_allow_html=True)
        if enter_key:
            if input_api_key:
                genai.configure(api_key=input_api_key)
                st.balloons()
            else:
                genai.configure(api_key=GOOGLE_API_KEY)
                st.balloons()      

        if st.button("Clear Chat Window", use_container_width=True, type="primary"):
            st.session_state.chat_history = []
            st.rerun()


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Initialize chat history in session state
    st.session_state.chat_history.append({"role":"user","content": "Hi" })
    st.session_state.chat_history.append({"role":"assistant","content": "Hello there! I am Nidhi, How can I assist you today?" })    

i = 0  
j = 0

user_input = st.chat_input("Enter your question...", key=f"chat_input{i}")
i+=1
if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})  # Add user message
    
        try:
            response = chat(user_input)
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})  # Add assistant response
            user_input = ""

        except ValueError:
            if response.prompt_feedback.safety_ratings:
                safety_rating = response.prompt_feedback.safety_ratings[0]
                st.session_state.chat_history.append({"role": "error", "content": f"Could not answer due to safety reason,\n{safety_rating}"})
            else:
                st.session_state.chat_history.append({"role": "error", "content": "Could not answer due to safety reason"})

for j, message_data in enumerate(st.session_state.chat_history):
        message(
            message_data["content"],
            is_user=message_data["role"] == "user",
            key=f"message_{i}_{j}",  # Ensure unique keys for messages
        )  
