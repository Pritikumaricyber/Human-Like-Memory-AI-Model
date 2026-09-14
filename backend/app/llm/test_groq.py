from backend.app.llm.groq_provider import GroqProvider


def main():

    provider = GroqProvider()

    response = provider.generate(
        prompt="Explain in one sentence what human-like memory means in AI.",
        system_prompt=(
            "You are a helpful AI assistant. "
            "Give concise and clear answers."
        ),
    )

    print("\n==============================")
    print("GROQ TEST")
    print("==============================")
    print(response)


if __name__ == "__main__":
    main()