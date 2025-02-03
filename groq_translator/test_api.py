import requests

def test_translation(text, target_language, source_language="English"):
    url = "http://localhost:8001/translate"
    payload = {
        "text": text,
        "target_language": target_language,
        "source_language": source_language
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        result = response.json()
        print(f"\nTranslation Results:")
        print(f"Original ({result['source_language']}): {text}")
        print(f"Translated ({result['target_language']}): {result['translated_text']}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Example usage
    test_translation("Hello, how are you?", "Spanish")
    test_translation("I love programming", "French")
    test_translation("The weather is beautiful today", "Japanese") 