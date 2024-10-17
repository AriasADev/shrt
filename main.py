from flask import Flask, request, redirect, render_template
import string
import random
import json

app = Flask(__name__)


# Define a function to generate a random short URL
def generate_short_url():
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(7))


# Load the URL mappings from the file
with open('mappings.json', 'r') as f:
    url_map = json.load(f)


# Define the route for the index page
@app.route('/')
def index():
    return render_template('index.html')


# Define the route for the URL shortening endpoint
@app.route('/shorten', methods=['POST'])
def shorten():
    # Get the original URL and custom URL from the form
    original_url = request.form['url']
    custom_url = request.form['custom_url']


    # If the custom URL is already taken, show an error message
    if custom_url and custom_url in url_map:
        return render_template('index.html', error='That custom URL is already taken.')

    # If the user did not specify a custom URL, generate a random one
    if not custom_url:
        custom_url = generate_short_url()

    # Add the prefix to the original URL if it doesn't already have it
    if not original_url.startswith(('http://', 'https://')):
        original_url = 'http://' + original_url

    # Add the mapping to the URL mappings dictionary
    url_map[custom_url] = original_url

    # Save the mappings to the file
    with open('mappings.json', 'w') as f:
        json.dump(url_map, f)

    # Show the success page with the shortened URL
    short_url = f'{custom_url}'
    return render_template('success.html', short_url=short_url)


# Define the route for the short URL redirections
@app.route('/<short_url>')
def redirect_url(short_url):
    # Check if the shortened URL is in the mappings dictionary
    if short_url in url_map:
        original_url = url_map[short_url]
        return redirect(original_url)
    else:
        return render_template('index.html', error='That shortened URL does not exist.')


# Set up the app to listen on all IP addresses
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
