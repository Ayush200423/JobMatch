
# JobMatch

JobMatch is an easier and faster way to apply to multiple jobs you may be qualified for.




## How to Use

- Create an account or sign in to JobMatch
- Upload your resume
- Edit your details
- Select the jobs you want to apply for
- Sign in to the JobMatch chrome extension and click "Apply"
## Demo
[Link to YouTube.com]
[![Watch the video](https://img.youtube.com/vi/_jINZZqrpFs/maxresdefault.jpg)](https://youtu.be/_jINZZqrpFs)
## Under the Hood

- JobMatch automatically generates training / testing data, based on your edits, in a JSON format, and uploads it to Firebase Cloud Storage, essential to creating increasingly accurate models in the future
- Natural Language Processing is used to extract resume data and to match them to job descriptions
- The chrome extension communicates with the JobMatch backend API endpoints for retrieval of data
- Cronjob scrapes 4,000 job posting links regularly within seconds
## Technologies

- Python
    - Flask (micro web framework)
    - spaCy
    - NLTK
    - BeautifulSoup4
- Javascript
    - Fetch API
- HTML / CSS
- MySQL
- Firebase Cloud Storage
## Next Steps

As spaCy v3 has changed the method of training models, from JSON files to the .spacy format, next steps include automatically converting that data before uploading to Firebase. 
## Support

For support or further details, feel free to email me at ayush200423@gmail.com.

