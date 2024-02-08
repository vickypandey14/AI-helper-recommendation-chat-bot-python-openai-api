import openai
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Checking if dotenv file is loaded
if os.getenv('OPENAI_API_KEY'):
    print("Dotenv file loaded and OPENAI_API_KEY is set.")
    openai.api_key = os.getenv('OPENAI_API_KEY')
else:
    print("Dotenv file not found or OPENAI_API_KEY is not set.")
    # Optionally, exit the program if the API key is not set
    exit()

# Set the name of the Copilot
chatbot_name = "I am an AI assistant designed by bytewebster."

# Sample projects data
projects = [
    {
        "project_name": "Responsive Smooth Accordion using Alpine.js and Tailwind CSS",
        "project_url": "https://bytewebster.com/javascriptprojects/smooth-faq-accordion-using-alpinejs-and-tailwind-css",
        "project_description": "In this Javascript project we will make a responsive Smooth FAQ (Frequently Asked Questions) Accordion. For this we will use Tailwind CSS and Alpine.js Frameworks. This accordion allows users to expand and collapse individual questions and answers, making it easy to navigate and find the information they need.",
    },
    {
        "project_name": "A Custom Captcha Using HTML, CSS, and JavaScript",
        "project_url": "https://bytewebster.com/javascriptprojects/build-a-custom-captcha-using-html-css-and-javascript",
        "project_description": "This JavaScript-made custom captcha is a way to add security to a website by providing a challenge that only humans can solve easily. It generates a random text using JavaScript which contains alphanumeric characters and displays it on an input field. The user has to enter the same text in an input box to verify they are human.",
    },
]

def find_project(user_input):
    # Score projects based on the number of matches
    project_scores = []

    for project in projects:
        score = 0

        for field, value in project.items():
            if isinstance(value, str) and user_input.lower() in value.lower():
                score += 1

        project_scores.append((project, score))

    # Sort projects by score in descending order
    sorted_projects = sorted(project_scores, key=lambda x: x[1], reverse=True)

    # Return projects with the highest scores
    matching_projects = [project for project, score in sorted_projects if score > 0]

    return matching_projects

def get_project_info(project):
    print(f"Project Name: {project['project_name']}")
    print(f"Project URL: {project['project_url']}")
    print(f"Project Description: {project['project_description']}")
    
    # Use OpenAI API to provide additional information based on the project description
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Why is the project '{project['project_name']}' useful?\n\n{project['project_description']}\n\n",
        max_tokens=150,
    )
    print("AI Assistant:", response.choices[0].text)

# Start a conversation loop
while True:
    # Ask for user input
    user_input = input("Ask AI assistant: ")

    # Check if the user wants to exit
    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break  # Exit the loop

    # Find projects related to user input
    matching_projects = find_project(user_input)

    # Print project information if projects are found
    if matching_projects:
        for project in matching_projects:
            get_project_info(project)
            break  # Break out of the loop after printing the information once
    else:
        print("No projects are found.")