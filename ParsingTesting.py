import pandas as pd
import openai

def extract_values_from_text(text):
    # Replace 'YOUR_API_KEY' with your OpenAI API key
    openai.api_key = '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'

    # Define the prompt with instructions
    prompt = """
    Given the following text, extract the desired values:
    
    Text: {}
    
    Values to extract:
    - Value 1: [Date]
    - Value 2: [Lesson Number (for example שיעור 1)]
    - Value 3: [teacher(No matter what DO NOT PUT THE WORD לקבוצה in this value)]
    - Value 4: [action (could be 2 things: ביטול שיעור or החלפת חדר)]
    """
    
    # Format the prompt with the provided text
    formatted_prompt = prompt.format(text)
    
    # Generate the response using ChatGPT
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=formatted_prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7
    )
    
    # Retrieve the extracted values from the response
    extracted_values = response.choices[0].text.strip().split('\n')
    
    # Return the extracted values
    return extracted_values

# Example usage
data = pd.read_csv('Test.csv')
df = pd.DataFrame(data)

# Iterate over each column
for text in df['lesson_info']:
    # Extract the values using ChatGPT
    extracted_values = extract_values_from_text(text)
    
    # Print the extracted values
    print("Extracted Values:")
    for value in extracted_values:
        print(value.strip())
    print()
