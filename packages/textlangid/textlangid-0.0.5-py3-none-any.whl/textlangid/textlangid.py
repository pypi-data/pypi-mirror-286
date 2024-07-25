import fasttext
from huggingface_hub import hf_hub_download
from processors import TextProcessor

model_path = hf_hub_download(repo_id="facebook/fasttext-language-identification", filename="model.bin")
# Load the FastText model
model = fasttext.load_model(model_path)

class TextLanguageIdentifier:
    @staticmethod
    def detect(text):
        # Predict the language of the text
        text = TextProcessor.preprocess_for_lang_id(text)
        if len(text) > 3:
            prediction = model.predict(text)
            return prediction[0][0].replace('__label__', '')
        else:
            return "unknown"
    
# Example usage
if __name__ == "__main__":
    text = "Ceci est un texte en français.%20  ✏️"
    lang = TextLanguageIdentifier.detect(text)
    print(lang)