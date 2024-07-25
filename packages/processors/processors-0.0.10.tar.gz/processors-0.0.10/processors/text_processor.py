import re
import urllib.parse
import demoji
import string

class TextProcessor:
    @staticmethod
    def url_decode(input_text):
        decoded_text = input_text
        prev_decoded_text = ""
        while prev_decoded_text != decoded_text:
            prev_decoded_text = decoded_text
            decoded_text = urllib.parse.unquote(decoded_text)
        return decoded_text
    
    @staticmethod
    def substitute_urls(input_text):
        url_pattern = re.compile(r'(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})(\.[a-zA-Z0-9]{2,})?')
        modified_text = url_pattern.sub(':url:', input_text)
        return modified_text
    
    @staticmethod
    def normalize_laughter(input_text):
        haha_pattern = re.compile(r'(?i)[ha]*(haha|hah)[ha]*')
        modified_text = haha_pattern.sub('haha', input_text)
        lol_pattern = re.compile(r'(lol)[lol|ol]*')
        modified_text = lol_pattern.sub('haha', modified_text)
        return modified_text
    
    @staticmethod
    def substitute_emojis(input_text):
        modified_text = demoji.replace_with_desc(input_text)
        return modified_text
    
    @staticmethod
    def remove_emojis(text):
        return demoji.replace(text, "")
    
    @staticmethod
    def capitalize_first_letter(input_text):
        if input_text:
            return input_text[0].upper() + input_text[1:]
        return input_text
    

    @staticmethod
    def uppercase_after_punctuation(input_string):
        def uppercase(match):
            return match.group(0).upper()
        
        pattern = r'[.!?]\s*([a-z])'
        transformed_string = re.sub(pattern, uppercase, input_string)
        return transformed_string

    @staticmethod
    def remove_leading_trailing_spaces(input_text):
        return input_text.strip()
    
    @staticmethod
    def dot_at_end_unless_punctuated(input_text):
        if input_text and input_text[-1] not in string.punctuation:
            return input_text + "."
        return input_text
    
    @staticmethod
    def remove_multiple_spaces(input_text):
        return re.sub(r'\s+', ' ', input_text)
    
    @staticmethod
    def replace_consecutive_punctuation(input_text):
        modified_text = ""
        prev_char = ""
        for char in input_text:
            if (char in string.punctuation) and (prev_char in string.punctuation):
                if (char != ".") and (prev_char != "."):
                    continue
            else:
                modified_text += char
            prev_char = char
        return modified_text
    
    @staticmethod
    def replace_consecutive_dots(input_text):
        return re.sub(r'\.{2,}', '...', input_text)
    
    @staticmethod
    def remove_spaces_before_punctuation(input_text):
        return re.sub(r'\s+([^\w\s])', r'\1', input_text)
    
    @staticmethod
    def remove_spaces_between_punctuation(input_text):
        return re.sub(r'\s*([^\w\s])\s*', r'\1', input_text)
    
    @staticmethod
    def add_space_after_punctuation(input_text):
        return re.sub(r'([^\w\s])(?![\s])', r'\1 ', input_text)
    
    @staticmethod
    def process_emoji_descriptions(text):
        # Define a regular expression pattern to match emoji descriptions
        pattern = r'(:[a-z\s]+\S+:)'

        # Find all matches of the pattern in the text
        matches = re.findall(pattern, text)
        # Process each match
        for match in matches:
            # Find the index of the match in the text
            index = text.index(match)

            # Add a space before the emoji description if needed
            if (index > 0) and (text[index-1] != ' '):
                text = text[:index] + ' ' + text[index:]

            # Add a space after the emoji description if needed
            if (index + len(match) +1 < len(text)):
                if text[index + len(match) +1] not in string.punctuation and text[index + len(match) +1] != ' ':
                    text = text[:index + len(match) +1] + ' ' + text[index + len(match) +1:]

        return text
    
    @staticmethod
    def preprocess_for_lang_id(input_text):
        if input_text:
            processed = input_text
            processed = TextProcessor.url_decode(processed)
            processed = TextProcessor.remove_emojis(processed)
            processed = TextProcessor.normalize_laughter(processed)
            processed = TextProcessor.remove_multiple_spaces(processed)
            processed = TextProcessor.remove_spaces_between_punctuation(processed)
            processed = TextProcessor.replace_consecutive_punctuation(processed)
            processed = TextProcessor.replace_consecutive_dots(processed)
            processed = TextProcessor.remove_spaces_before_punctuation(processed)
            processed = TextProcessor.add_space_after_punctuation(processed)
            processed = TextProcessor.remove_leading_trailing_spaces(processed)
            processed = TextProcessor.uppercase_after_punctuation(processed)
            processed = TextProcessor.capitalize_first_letter(processed)
            processed = TextProcessor.dot_at_end_unless_punctuated(processed)
        else:
            processed = ""
        return processed
    
    # For now no difference between lang id and translation, but that might chance over time
    @staticmethod
    def preprocess_for_translation(input_text):
        return TextProcessor.preprocess_for_lang_id(input_text)


    @staticmethod
    def preprocess(input_text):
        if input_text:
            processed = input_text
            processed = TextProcessor.url_decode(processed)
            processed = TextProcessor.normalize_laughter(processed)
            processed = TextProcessor.remove_multiple_spaces(processed)
            processed = TextProcessor.remove_spaces_between_punctuation(processed)
            processed = TextProcessor.replace_consecutive_punctuation(processed)
            processed = TextProcessor.replace_consecutive_dots(processed)
            processed = TextProcessor.remove_spaces_before_punctuation(processed)
            processed = TextProcessor.add_space_after_punctuation(processed)
            processed = TextProcessor.remove_leading_trailing_spaces(processed)
            processed = TextProcessor.uppercase_after_punctuation(processed)
            processed = TextProcessor.capitalize_first_letter(processed)
            processed = TextProcessor.substitute_emojis(processed)
            processed = TextProcessor.process_emoji_descriptions(processed)
            processed = TextProcessor.dot_at_end_unless_punctuated(processed)
        else:
            processed = ""
        return processed
