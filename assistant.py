"""A small personal assistant with text mode and optional speech support."""
import argparse
import ast
import datetime as dt
import operator
from pathlib import Path

NOTES = Path("notes.txt")
OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
       ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv,
       ast.Mod: operator.mod, ast.Pow: operator.pow}
UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def calculate(expression):
    """Safely evaluate basic arithmetic without eval()."""
    if len(expression) > 100:
        raise ValueError("Expression is too long.")

    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return float(node.value)
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 8:
                raise ValueError("Exponent is too large.")
            result = OPS[type(node.op)](left, right)
            if abs(result) > 1e100:
                raise ValueError("Result is too large.")
            return result
        if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY:
            return UNARY[type(node.op)](visit(node.operand))
        raise ValueError("Use numbers and basic arithmetic operators only.")

    try:
        return visit(ast.parse(expression, mode="eval"))
    except (SyntaxError, ZeroDivisionError, OverflowError) as exc:
        raise ValueError("Invalid calculation.") from exc


class Assistant:
    def __init__(self, notes_file=NOTES):
        self.notes_file = Path(notes_file)

    def respond(self, message):
        raw = message.strip()
        command = raw.lower()
        if not command:
            return "I didn't catch that. Type 'help' for commands."
        if command in ("help", "commands"):
            return "Commands: hello, time, date, calculate 4 * (2 + 3), note <text>, read notes, exit."
        if command in ("hello", "hi", "hey"):
            return "Hello! How can I help?"
        if command in ("time", "what time is it"):
            return dt.datetime.now().astimezone().strftime("The time is %I:%M %p.")
        if command in ("date", "what is the date"):
            return dt.date.today().strftime("Today is %A, %d %B %Y.")
        if command.startswith("calculate "):
            return f"The answer is {calculate(raw[10:]):g}."
        if command == "note" or command.startswith("note "):
            note = raw[4:].strip()
            if not note:
                return "Please provide some note text."
            with self.notes_file.open("a", encoding="utf-8") as file:
                file.write(note + "\n")
            return "I've saved your note."
        if command == "read notes":
            if not self.notes_file.exists():
                return "You don't have any saved notes yet."
            content = self.notes_file.read_text(encoding="utf-8").strip()
            return content or "Your notes file is empty."
        return "I don't know that command yet. Type 'help' for options."


def listen():
    try:
        import speech_recognition as sr
    except ImportError as exc:
        raise RuntimeError("Install voice packages with: pip install -r requirements-voice.txt") from exc
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as exc:
        raise RuntimeError(f"Speech recognition service error: {exc}") from exc


def speak(message):
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(message)
        engine.runAndWait()
    except (ImportError, RuntimeError):
        print("[Text response: speech output is unavailable]")


def main():
    parser = argparse.ArgumentParser(description="A simple personal voice assistant.")
    parser.add_argument("--voice", action="store_true", help="Use microphone and spoken responses.")
    args = parser.parse_args()
    assistant = Assistant()
    print("Astra Assistant ready. Type 'help' for commands.")
    while True:
        try:
            message = listen() if args.voice else input("\nYou: ")
            if args.voice:
                print("You:", message)
            if message.strip().lower() in {"exit", "quit", "stop"}:
                reply = "Goodbye! Have a great day."
                print("Assistant:", reply)
                if args.voice:
                    speak(reply)
                break
            reply = assistant.respond(message)
            print("Assistant:", reply)
            if args.voice:
                speak(reply)
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
        except (RuntimeError, OSError) as exc:
            print("Assistant:", exc)
            if args.voice:
                print("Stopping voice mode. Run without --voice to use text mode.")
                break


if __name__ == "__main__":
    main()
