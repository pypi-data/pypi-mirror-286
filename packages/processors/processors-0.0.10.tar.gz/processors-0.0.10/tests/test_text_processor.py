from processors import TextProcessor

def test_url_decode():
    decoded_text = TextProcessor.url_decode("Hello%25252520world%25252521")
    assert decoded_text == "Hello world!"

def test_substitute_urls():
    preprocessed_text = TextProcessor.substitute_urls("Check it at test.com or at https://www.test.com or test.com.")
    assert preprocessed_text == "Check it at :url: or at :url: or :url:."

def test_normalize_laughter():
    preprocessed_text = TextProcessor.normalize_laughter("that's funny hahhahahahh")
    assert preprocessed_text == "that's funny haha"

def test_substitute_emojis():
    preprocessed_text = TextProcessor.substitute_emojis("cool 😎")
    assert preprocessed_text == "cool :smiling face with sunglasses:"

def test_replace_consecutive_punctuation():
    preprocessed_text = TextProcessor.replace_consecutive_punctuation("do you really think so??!!!!....")
    assert preprocessed_text == "do you really think so?"

def test_preprocess_for_lang_id():
    preprocessed_text = TextProcessor.preprocess_for_lang_id(" hello%25252520world%25252521 ???!!!!!???how are you??? 😎")
    assert preprocessed_text == "Hello world! How are you?"

def test_preprocess_for_translation():
    preprocessed_text = TextProcessor.preprocess_for_translation(" hello%25252520world%25252521 ???!!!!!???how are you??? 😎")
    assert preprocessed_text == "Hello world! How are you?"

def test_preprocess():
    preprocessed_text = TextProcessor.preprocess(" hello%25252520world%25252521 ???!!!!!???how are you??? 😎")
    assert preprocessed_text == "Hello world! How are you? :smiling face with sunglasses:"
    preprocessed_text = TextProcessor.preprocess("       this is%20absolutely%20horrible%20  text😠!!!! !!??? ?    that needs to be   cleaned up         ")
    assert preprocessed_text == "This is absolutely horrible text :angry face: ! That needs to be cleaned up."
    preprocessed_text = TextProcessor.preprocess("This is a test : will it pass?")
    assert preprocessed_text == "This is a test: will it pass?"
