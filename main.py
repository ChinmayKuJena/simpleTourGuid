import os
import pytz
import streamlit as st
import json
from groq import Groq
from email_service import send_email  # Import the email service
from datetime import datetime

# Initialize Groq client with your API key
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Set page configuration to wide layout
st.set_page_config(page_title="Place Info with Groq", page_icon="🗺️", layout="wide")

# Hide the Streamlit header and footer
st.markdown("""
    <style>
    /* Hide header and footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Background Image */
    body {
        background-image: url('https://user-images.githubusercontent.com/35409648/74775140-0373ab80-528d-11ea-8acd-9499c85a697f.gif'); /* Add your background image URL */
        background-size: cover;
        background-repeat: no-repeat;
        animation: backgroundAnimation 30s infinite alternate;
    }

    /* Keyframes for Animation */
    @keyframes backgroundAnimation {
        0% { opacity: 1; }
        100% { opacity: 0.7; } /* Adjust opacity for the animation effect */
    }

    /* Container styling */
    .container {
        width: 90%;
        margin: auto;
        background-color: rgba(255, 255, 255, 0.8); /* Semi-transparent white background */
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Title and Description
# st.markdown("<div class='container'>", unsafe_allow_html=True)  # Start of container
st.title("Get Information About Any Place 🗺️")
st.write("Enter the name of a place to get interesting details about it.")

# Function to generate greeting based on the time of day
# Function to generate greeting based on the user's time zone
def get_greeting():
    # Get the current time in the user's time zone
    tz = pytz.timezone("Asia/Kolkata")
    current_time = datetime.now(tz)
    current_hour = current_time.hour
    current_day = current_time.strftime("%A")

    # Determine greeting based on current hour
    if 5 <= current_hour < 12:
        greeting = "Good Morning"
    elif 12 <= current_hour < 17:
        greeting = "Good Afternoon"
    elif 17 <= current_hour < 21:
        greeting = "Good Evening"
    else:
        greeting = "Good Night"

    return f"{greeting}, Happy {current_day}!"

# Display greeting
st.markdown(f"<h3 style='color:orange;'>{get_greeting()}</h3>", unsafe_allow_html=True)

# User Input with Typing Animation
placeholder_text = "Hy Boss, type here !!!"
place_name = st.text_input("Enter Place Name", placeholder=placeholder_text)

# Function to get details from Groq with different questions
def get_place_details(place):
    questions = {
        "historical_facts": f"Tell me about the historical significance of {place}.",
        "attractions": f"What are the main attractions in {place}?",
        "famous_places": f"Which famous places should I not miss in {place}?",
        "unique_information": f"Share some unique information about {place}."
    }
    place_info = {"place": place}

    for field, question in questions.items():
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": question}],
            model="llama3-8b-8192"
        )
        place_info[field] = response.choices[0].message.content if response.choices else "No details found."

    return place_info

# Button to submit the place name
if st.button("Get Details"):
    if place_name:
        with st.spinner("Fetching details..."):
            try:
                details = get_place_details(place_name)
                st.success("Here are the details:")
                
                # Display details with styled headers for the user
                st.markdown(f"<span style='font-weight:bold; color:orange;'>Historical Facts</span>: {details['historical_facts']}", unsafe_allow_html=True)
                st.markdown(f"<span style='font-weight:bold; color:orange;'>Attractions</span>: {details['attractions']}", unsafe_allow_html=True)
                st.markdown(f"<span style='font-weight:bold; color:orange;'>Famous Places</span>: {details['famous_places']}", unsafe_allow_html=True)
                st.markdown(f"<span style='font-weight:bold; color:orange;'>Unique Information</span>: {details['unique_information']}", unsafe_allow_html=True)
                
                json_data = json.dumps(details)

                # HTML content for the email
                html_content = f"""
                <html>
                    <head>
                        <style>
                            body {{
                                font-family: Arial, sans-serif;
                                background-color: #f4f4f4;
                                color: #333;
                            }}
                            .container {{
                                width: 90%;
                                margin: 0 auto;
                                background-color: #ffffff;
                                padding: 20px;
                                border-radius: 8px;
                                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                            }}
                            .header {{
                                text-align: center;
                                padding: 10px 0;
                                color: #4CAF50;
                            }}
                            .place-details {{
                                width: 100%;
                                margin-top: 20px;
                                border-collapse: collapse;
                            }}
                            .place-details th {{
                                background-color: #4CAF50;
                                color: white;
                                padding: 12px;
                                text-align: left;
                                border: 1px solid #ddd;
                            }}
                            .place-details td {{
                                padding: 12px;
                                border: 1px solid #ddd;
                                color: #555;
                            }}
                            .footer {{
                                text-align: center;
                                margin-top: 20px;
                                color: #888;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h2 class="header">Place Information Request</h2>
                            <p>Here is the information you requested for <strong>{place_name}</strong>:</p>
                            <table class="place-details">
                                <tr><th>Field</th><th>Information</th></tr>
                                <tr><td><strong>Historical Facts</strong></td><td>{details["historical_facts"]}</td></tr>
                                <tr><td><strong>Attractions</strong></td><td>{details["attractions"]}</td></tr>
                                <tr><td><strong>Famous Places</strong></td><td>{details["famous_places"]}</td></tr>
                                <tr><td><strong>Unique Information</strong></td><td>{details["unique_information"]}</td></tr>
                            </table>
                            <div class="footer"><p>Thank you for using our service!</p><p>Made with ❤️ using Streamlit and Groq</p></div>
                        </div>
                    </body>
                </html>
                """
                
                subject = f"Place Info Request: {place_name}"
                
                # Send email with the HTML content
                # send_email(subject, html_content)

            except Exception as e:
                st.error(f"Error fetching details: {e}")

# Close the container
st.markdown("</div>", unsafe_allow_html=True)  # End of container

# Footer
st.markdown("---")
# st.write("Made with ❤️ using Streamlit and Groq By Chinmay Jena")
st.write("Made By Chinmay Jena")
