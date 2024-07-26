import sys
import re

def main():
    if len(sys.argv) < 2:
        print("Please provide a sentence to convert.")
        return

    command = sys.argv[1]
    input_text = " ".join(sys.argv[2:])

    if command == "-sentence":
        print(sentence_format(input_text))
    elif command == "-upper":
        print(input_text.upper())
    elif command == "-lower":
        print(input_text.lower())
    else:
        print("Please format command correctly. Use -sentence, -upper, or -lower.")


def sentence_format(sentence):
    sentence = re.sub(r'\.\.\.', '<<>>', sentence)
    sentences = [s.strip() for s in sentence.split('.')]
    formatted_sentences = []
    
    for s in sentences:
        if s:
            formatted_sentences.append(s[0].upper() + s[1:].lower())
    
    result = '. '.join(formatted_sentences)
    result = re.sub(r'<<>>', '...', result)
    if sentence.strip().endswith('.'):
        result += '.'
    
    return result


if __name__ == '__main__':
    main()

