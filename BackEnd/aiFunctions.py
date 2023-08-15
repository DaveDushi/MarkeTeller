import openai


def summarize_text_with_chatgpt(text, description, key):
    # Set up OpenAI API credentials
    openai.api_key = key

    # Define the system and user instructions
    system_instructions = "You are a financial expert. Summarize the text in 800 or fewer tokens."
    user_instructions = description + ':\n' + text

    # Call the OpenAI ChatGPT API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=system_instructions + "\n\n" + user_instructions,
        max_tokens=800
    )

    return response.choices[0].text.strip()


def generate_financial_report(summary, key):
    # Set up OpenAI API credentials
    openai.api_key = key
    user_instructions = summary
    # set prompt for financial report
    # Define the system and user instructions
    system_instructions = "You are a financial expert. Given the following text provide a financial report."

    # Call the OpenAI ChatGPT API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=system_instructions + "\n\n" + user_instructions,
        max_tokens=2000
    )

    # Extract the response from the API
    generated_report = response.choices[0].text.strip()

    # Define the system and user instructions for the recommendation
    rec_system = "You are a financial expert. Based on the provided information, suggest a recommendation: HOLD, BUY, or SELL."

    # Call the OpenAI ChatGPT API to generate the recommendation
    financial_rec_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=rec_system + "\n\n" + user_instructions,
        max_tokens=20
    )

    # Extract the recommendation from the API response
    financial_rec = financial_rec_response.choices[0].text.strip()

    final_report = f'{generated_report}\n\n{financial_rec}'
    # Write the generated report to the output file
    report = f"Financial Report:\n\n{final_report}"

    return report
