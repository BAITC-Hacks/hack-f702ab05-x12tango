from faq_engine import load_faq, find_answer


def main():
    faq = load_faq()
    print("FAQ-бот про репетицию хакатона. Задайте вопрос (или 'выход').")
    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue
        if user_input.lower() in ("выход", "exit", "quit"):
            break

        answer = find_answer(user_input, faq)
        print(answer if answer else "не знаю")


if __name__ == "__main__":
    main()
