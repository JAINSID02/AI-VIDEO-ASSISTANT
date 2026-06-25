from dotenv import load_dotenv
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarize import summarize , generate_title
from core.extractor import extract_action_items, extract_key_decisions , extract_questions

from core.rag_engine import build_rag_chain , ask_question


load_dotenv()
def run_pipeline(source:str,language:str='english')->dict:
    print("  Starting AI VIDEO Assistant   ")
    chunks=process_input(source)
    transcript=transcribe_all(chunks , language = language)
    print("  RAW TRANSCRIPTION (FIRST 300 CHARACTERS)  ",transcript[:300])

    title = generate_title(transcript)
    summary=summarize(transcript)
    action_item=extract_action_items(transcript)
    key_decisions = extract_key_decisions(transcript)
    questions=extract_questions(transcript)
    rag_chain = build_rag_chain(transcript)

    return {"title":title,
            "transcript":transcript,
            "summary":summary,
            "action_item":action_item,
            "key_decisions":key_decisions,
            "questions":questions,
            "rag_chain":rag_chain


            }

if __name__ =="__main__":
    source=input("  Enter youtube url or local file path  ").strip()
    language=input("  english or hinglish  ").strip() or "english"
    result = run_pipeline(source, language)

    print("\n" + "="*50)
    print("TITLE" , result['title'])
    print("\nSUMMARY" , result['summary'])
    print("\nACTION ITEMS" , result['action_item'])
    print("\nKEY DECISIONS" , result['key_decisions'])
    print("\nOPEN QUESTIONS" , result['questions'])
    print("\n" + "="*50)

    print("\n Chat with your meeting")
    rag_chain=result['rag_chain']

    while True:
        question=input("  You  ").strip()
        if question.lower() in ['exit'] :
            print("bye")
            break
        if not question :
            continue

        answer = ask_question(rag_chain , question)
        print("   Assistant ANSWER   ", answer)

