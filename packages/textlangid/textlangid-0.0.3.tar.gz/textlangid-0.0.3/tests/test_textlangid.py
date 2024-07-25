import textlangid

def test_lang_id():
    # lang = textlangid.detect("This is some text.")
    lang = textlangid.detect("This is some text.")
    assert lang == "eng_Latn"
