import textlangid

def test_lang_id():
    # lang = textlangid.detect("This is some text.")
    lang = textlangid.detect("This is some text.")
    assert lang == "eng_Latn"
    
def test_string_too_short():    
    lang = textlangid.detect("Th")
    assert lang == "unknown"
