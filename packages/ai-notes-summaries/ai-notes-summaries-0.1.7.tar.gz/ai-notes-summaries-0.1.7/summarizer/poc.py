from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


load_dotenv()


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're an expert summarizer. "
            "Give me 3 takeaways from the text I provide, formatted as bullet points.",
        ),
        ("human", "{text}"),
    ]
)


def get_open_ai_summarizer():
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    return prompt | llm


text = "Manchester United Football Club, commonly referred to as Man United (often stylised as Man Utd), or simply United, is a professional football club based in Old Trafford, Greater Manchester, England. The club competes in the Premier League, the top tier of English football. Nicknamed the Red Devils, they were founded as Newton Heath LYR Football Club in 1878, but changed their name to Manchester United in 1902. After a spell playing in Clayton, Manchester, the club moved to their current stadium, Old Trafford, in 1910."

print(get_open_ai_summarizer().invoke({"text": text}).content)
