from flask import Flask, request, render_template
import requests
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Collect user input from form
        name = request.form.get('name')
        city = request.form.get('city')
        job_title = request.form.get('job_title')
        skills = request.form.get('skills')

        # Prepare the resume data dynamically
        user_info = f"Hi, I'm {name} from {city}. I am a {job_title} with skills in {skills}."

        # Send data to the API
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer <OPENROUTER_API_KEY>",
                "Content-Type": "application/json",
                "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional
                "X-Title": "<YOUR_SITE_NAME>",  # Optional
            },
            data=json.dumps({
                "model": "deepseek/deepseek-r1:free",
                "messages": [
                    {
                        "role": "system",
                        "content": f"Create a professional resume using the following information: {user_info}. Make it concise and highlight the skills of the user."
                    },
                ],
            })
        )

        # Check if the response was successful
        if response.status_code == 200:
            resume = response.json()
            # Assuming the response contains the generated resume text in 'choices' or another field
            generated_resume = resume.get('choices')[0].get('message').get('content')
            return render_template('resume.html', resume=generated_resume)
        else:
            return "Error generating resume, please try again later."

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
