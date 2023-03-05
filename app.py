import openai
import requests
from PIL import Image
from io import BytesIO

# Set up the API keys
openai.api_key = "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"

# Define a function to generate the blog content
def generate_blog_content():
    # Initialize the chat history
    chat_history = []
    while True:
    # Keep adding messages to the chat history until the user is satisfied

        # Prompt the user for input
        user_input = input("Enter your idea for the blog post: ")
        messages = [
            {"role": "system", "content": "You are advanced marketing and seo assistant."},
            {"role": "user", "content": f"Create a blog post for {user_input}, refrain from using a phrase before the blog post i.e Sure, here's a blog post on how to make pizza:"}
                  ]
        messages += chat_history
        # Add the user's message to the chat history

        # Generate the response using GPT-3

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.8,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        print(f"Here is the body of the Blog post:\n{response['choices'][0]['message']['content']}")
     
        #Add the response to the chat history
        chat_history.append(
            {"role": "system", "content": response["choices"][0]["message"]["content"]}
        )
        messages += chat_history

        title = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages= [{"role": "system", "content": response["choices"][0]["message"]["content"]}, {"role": "user", "content": "now give me the tittle for the blogpost you've created"}],
            temperature=0.7,
            max_tokens=50,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        chat_history.append(
            {"role": "system", "content": title["choices"][0]["message"]["content"]}
        )
        print(f"\nHere is the tittle of the Blog post: \n{title['choices'][0]['message']['content']}")

        imgprompt = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = [    {"role": "system", "content": title["choices"][0]["message"]["content"]},
                {"role": "user", "content": "now give me a DALL-E prompt to generate a fun image for the tittle you gave me, ideally photoreallistic images and non creepy, the reply should be assertive and without 'how about'"}
                    ],
            temperature=0.7,
            max_tokens=80,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        print(f" \nHere is the prompt for the DALL-E image of the Blog post:\n{imgprompt['choices'][0]['message']['content']}")
        chat_history.append(
            {"role": "system", "content": imgprompt["choices"][0]["message"]["content"]}
        )
            # Check if the user is satisfied
        satisfied = input("Are you satisfied with the generated content? (yes/no): ")
        if satisfied.lower() == "yes":
            break

    # Return the chat history

    return chat_history

# Define a function to generate an image
def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )

    image_url = response["data"][0]["url"]
    image = Image.open(BytesIO(requests.get(image_url).content))

    return image

# Define a function to format the blog post
def format_post(title, content, image_url, alt, deep_link):
    post = f"""
    <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css">
            <link rel="stylesheet" type="text/css" href="style.css">
        </head>
        <body>
            <div class="container">
                <h1>{title}</h1>
                <p>{content}</p>
                <img src="{image_url}" alt="{alt}" class="img-fluid">
                <p>Read more <a href="{deep_link}">here</a></p>
            </div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js" crossorigin="anonymous"></script>
        </body>
    </html>
    """
    return post



# Define a function to create the HTML file
def create_html_file(title, content):
    file_name = title.replace('', "").replace(" ", "_").lower() + ".html"
    with open(file_name, "w") as f:
        f.write(content)
    print(f"Blog post saved to {file_name}")

# Generate the blog content
chat_history = generate_blog_content()

# Extract the title and body from the chat history
title = chat_history[1]["content"]
body = chat_history[0]["content"]

# Generate the image prompt
image_prompt = chat_history[2]["content"]
alt = chat_history[2]["content"]
# Generate the image
image = generate_image(image_prompt)

# Save the image to a file
truncated_response = image_prompt[:5]
image_path = f"{truncated_response.replace(' ', '_').replace('', '').lower()}.jpg"


image.save(image_path)

# Format the blog post
deep_link = "www.google.com"
post = format_post(title, body, image_path, alt, deep_link)

# Create the HTML file
create_html_file(title, post)