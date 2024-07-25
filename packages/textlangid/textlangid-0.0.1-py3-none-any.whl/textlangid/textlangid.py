import fasttext
from huggingface_hub import hf_hub_download

class TextLanguageIdentifier:
    def __init__(self, repo_id="facebook/fasttext-language-identification", filename="model.bin"):
        # Download the model from Hugging Face Hub
        self.model_path = hf_hub_download(repo_id=repo_id, filename=filename)
        # Load the FastText model
        self.model = fasttext.load_model(self.model_path)

    def identify_language(self, text):
        # Predict the language of the text
        prediction = self.model.predict(text)
        return prediction[0][0].replace('__label__', '')

    def identify_top_k_languages(self, text, k=5):
        # Predict the top k languages of the text
        predictions = self.model.predict(text, k=k)
        languages = [label.replace('__label__', '') for label in predictions[0]]
        probabilities = predictions[1]
        return list(zip(languages, probabilities))

# Example usage
if __name__ == "__main__":
    text = "Ceci est un texte en français."
    lang_identifier = TextLanguageIdentifier()
    
    # Identify the primary language
    language = lang_identifier.identify_language(text)
    print(f"The primary language of the text is: {language}")
    
    # Identify the top 5 languages
    top_languages = lang_identifier.identify_top_k_languages(text, k=5)
    print("The top 5 predicted languages and their probabilities are:")
    for lang, prob in top_languages:
        print(f"Language: {lang}, Probability: {prob}")
