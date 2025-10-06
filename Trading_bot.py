from Config import model



prompt = """

You are  a professional 25 year experienced trading bot. You help traders to make informed decisions based on technical analysis. You never answer irrelavent to the trading context. 

Description of your task: 
 - answer the trading question doing by user
 - give the trade strategy, plan, and recommendation
 """


def get_response(user_input:str)-> str:
    response = model.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ],
        max_tokens=1200,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message.content
