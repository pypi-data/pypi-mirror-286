from langchain_openai import ChatOpenAI
import dotenv

from summarizer.prompting.prompt import get_summarizer_prompt


dotenv.load_dotenv()


def get_open_ai_summarizer():
    return get_summarizer_prompt() | ChatOpenAI(model="gpt-4o", temperature=0)


def perform_summarization(text: str):
    return get_open_ai_summarizer().invoke({"text": text})
