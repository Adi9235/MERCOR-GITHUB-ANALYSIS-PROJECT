# get-complex-repo.py

import os
import requests
import openai

openai.api_key = os.environ.get('OPENAI_KEY')

    
def handler(event, context):
    
    username = event.queryStringParameters['username']
    
    def get_repos(username):
        response = requests.get(f'https://api.github.com/users/{username}/repos')
        return response.json()
    # Helper function to preprocess code
    def preprocess_code(repo):
        try:
    # Clone and get code
            os.system(f'git clone {repo["clone_url"]}')
            files = os.listdir(repo['name'])
    
    # Keep first 100 lines
            cleaned_files = []
            for file in files:
                with open(os.path.join(repo['name'], file)) as f:
                    cleaned_files.append('\n'.join(f.readlines()[:100])) 
    # Delete cloned repo
                os.system(f'rm -rf {repo["name"]}')
    
            return cleaned_files
    
        except PermissionError:
            print("Permission denied when accessing the repo directory")
            return []
    # 3. Prompt engineering  # Helper to get complexity from OpenAI
    def get_complexity(files):
        try:
            prompt = "Analyze this code and describe its complexity: \n\n{'\n\n'.join(files)}"
            response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1000    
            )

            return response.choices[0].text
    
        except openai.error.RateLimitError:
            print("Hit OpenAI rate limit")
            return "Rate limited"
    # Main function
    # Print repo details 
    
    # Print repo details nicely
    
    def print_repo(repo):
        print(f"Repository: {repo['name']}")
        print(f"Owner: {repo['owner']['login']}")
        print(f"Stars: {repo['stargazers_count']}") 
        print(f"Forks: {repo['forks_count']}")
        print(f"Open Issues: {repo['open_issues']}")
        print(f"Language: {repo['language']}")
        print() 
    
    username = input("Enter Github username: ")
    
    # Main function
    def get_most_complex(username):
        repos = get_repos(username)
        
        complexity_scores = []
        
        for repo in repos:
            files = preprocess_code(repo)
            complexity = get_complexity(files) 
            complexity_scores.append((repo, complexity))
        for repo, complexity in complexity_scores:
            print_repo(repo)
            print(complexity)
            print()
    
        most_complex = max(complexity_scores, key=lambda x: len(x[1]))
    
    # get_most_complex(username)
        
    
    return {
        "statusCode": 200,
        "body": f"The most complex repo for {username} is {get_most_complex(username)}" 
    }