import os
import json
from googletrans import Translator
from tkinter import Tk, filedialog

# List of supported languages in alphabetical order with their ISO 639 codes
supported_languages = {
    "afrikaans": "af", "amharic": "am", "arabic": "ar", "azerbaijani": "az",
    "bashkir": "ba", "belarusian": "be", "bengali": "bn", "bosnian": "bs",
    "bulgarian": "bg", "catalan": "ca", "cebuano": "ceb", "chinese": "zh",
    "chinese(simplified)": "zh-CN", "chinese(traditional)": "zh-TW", "chuvash": "cv",
    "croatian": "hr", "czech": "cs", "danish": "da", "dutch": "nl", "english": "en",
    "esperanto": "eo", "estonian": "et", "fijian": "fj", "filipino": "tl",
    "finnish": "fi", "french": "fr", "georgian": "ka", "german": "de", "greek": "el",
    "gujarati": "gu", "haitiancreole": "ht", "hebrew": "he", "hindi": "hi",
    "hungarian": "hu", "icelandic": "is", "indonesian": "id", "irish": "ga",
    "italian": "it", "japanese": "ja", "kannada": "kn", "kazakh": "kk", "khmer": "km",
    "klingon/tlhingan hol": "tlh", "korean": "ko", "kurdish": "ku", "kyrgyz": "ky",
    "lao": "lo", "latvian": "lv", "lithuanian": "lt", "luxembourgish": "lb",
    "macedonian": "mk", "malagasy": "mg", "malay": "ms", "maltese": "mt",
    "mongolian": "mn", "nepali": "ne", "norwegian": "no", "odia": "or",
    "pashto": "ps", "persian/farsi": "fa", "polish": "pl", "portuguese": "pt",
    "punjabi": "pa", "queretaro otomi": "otq", "romanian": "ro", "russian": "ru",
    "samoan": "sm", "scots gaelic": "gd", "serbian": "sr", "slovak": "sk",
    "slovenian": "sl", "spanish": "es", "swahili": "sw", "swedish": "sv",
    "tajik": "tg", "tamil": "ta", "telugu": "te", "thai": "th", "tongan": "to",
    "turkish": "tr", "turkmen": "tk", "ukrainian": "uk", "urdu": "ur", "uyghur": "ug",
    "uzbek": "uz", "vietnamese": "vi", "welsh": "cy", "xhosa": "xh", "yiddish": "yi",
    "yoruba": "yo", "zulu": "zu"
}

def get_language():
    """Prompt the user to input a supported language and return its ISO 639 code."""
    while True:
        language = input("Please enter the language to translate the variables to: ").strip().lower()
        if language in supported_languages:
            return language, supported_languages[language]
        else:
            print(f"'{language}' is not supported.")
            try_again = input("Would you like to provide another language? (yes/no): ").strip().lower()
            if try_again != 'yes':
                print("Exiting the program.")
                exit()

def extract_defaults(json_data):
    """Extract 'default' and 'translation' values from the JSON data."""
    extracted_data = {"uiTranslations": []}
    for item in json_data.get("uiTranslations", []):
        if "default" in item and "translation" in item:
            extracted_data["uiTranslations"].append({
                "default": item["default"],
                "translation": item["translation"]
            })
    return extracted_data

def translate_text(text, target_language, error_file_path):
    """Translate a given text to the target language and log errors."""
    translator = Translator()
    try:
        if text:
            translated_text = translator.translate(text, dest=target_language).text
        else:
            translated_text = text
    except Exception as e:
        error_message = f"Error translating text '{text}': {e}"
        print(error_message)
        record_error(error_message, error_file_path)
        translated_text = text
    return translated_text

def translate_large_file(file_path, target_language, error_file_path, chunk_size=5000):
    """Translate 'default' values in a large JSON file to the target language."""
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    
    total_items = len(json_data.get("uiTranslations", []))
    translated_count = 0

    for item in json_data.get("uiTranslations", []):
        if "default" in item:
            text = item["default"]
            if text:
                # If the text is longer than the chunk size, split it into chunks for translation
                if len(text) > chunk_size:
                    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
                    translated_text = ''.join(translate_text(chunk, target_language, error_file_path) for chunk in chunks)
                else:
                    translated_text = translate_text(text, target_language, error_file_path)
                item["translation"] = translated_text
            translated_count += 1
            print(f"Translating item {translated_count} of {total_items}...")

    # Save the translated data back to the JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)

def update_translations(original_json, translated_json, language, language_code):
    """Update the original JSON with translated values from the translated JSON."""
    original_data = original_json["uiTranslations"]
    translated_data = translated_json["uiTranslations"]

    # Create a dictionary of default values from the original data for quick lookup
    original_defaults = {item["default"]: item for item in original_data if "default" in item}
    
    for item in translated_data:
        default_text = item["default"]
        if default_text in original_defaults:
            original_defaults[default_text]["translation"] = item["translation"]
    
    # Update display and key information in the original JSON
    original_json["display"] = language.capitalize()
    original_json["key"] = language_code
    
    return original_json

def record_error(error_message, error_file_path):
    """Record an error message to the error log file."""
    with open(error_file_path, 'a', encoding='utf-8') as error_file:
        error_file.write(error_message + '\n')

def ensure_unique_folder_path(base_folder_path):
    """Ensure that the folder path is unique by adding a number suffix if needed."""
    folder_path = base_folder_path
    count = 1
    while os.path.exists(folder_path):
        folder_path = f"{base_folder_path}_{count}"
        count += 1
    return folder_path

def main():
    """Main function to handle the translation process."""
    # Get the language from the user
    language, language_code = get_language()
    print(f"Selected language: {language}")

    # Initialize Tkinter and hide the root window
    root = Tk()
    root.withdraw()
    
    # Ask the user to select the JSON file
    file_path = filedialog.askopenfilename(
        title="Select the JSON file",
        filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
    )
    
    if not file_path:
        print("No file selected. Exiting.")
        return

    # Load the JSON data from the provided file path
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    # Extract the version number from the JSON data
    version = json_data.get("version", "unknown_version")

    # Extract the default and translation values from the JSON data
    extracted_data = extract_defaults(json_data)

    # Create a unique subfolder for the language and version
    base_dir = os.path.dirname(file_path)
    subfolder_name = f"REDCap_{version}_{language}"
    subfolder_path = ensure_unique_folder_path(os.path.join(base_dir, subfolder_name))
    os.makedirs(subfolder_path, exist_ok=True)

    # Define the output file name for the extracted data
    extracted_file = os.path.join(subfolder_path, f'{language}.json')

    # Define the error log file name
    error_file_path = os.path.join(subfolder_path, f'REDCap_{version}_{language}_Error.log')

    # Save the extracted data to a new JSON file
    with open(extracted_file, 'w', encoding='utf-8') as file:
        json.dump(extracted_data, file, ensure_ascii=False, indent=4)

    # Translate the "default" values in the new JSON file
    translate_large_file(extracted_file, language_code, error_file_path)

    # Load the translated data
    with open(extracted_file, 'r', encoding='utf-8') as file:
        translated_data = json.load(file)

    # Update the original JSON with the translated values
    updated_json = update_translations(json_data, translated_data, language, language_code)

    # Define the final output file name
    final_output_file = os.path.join(subfolder_path, f'REDCap_{version}_{language}.json')

    # Save the updated JSON data
    with open(final_output_file, 'w', encoding='utf-8') as file:
        json.dump(updated_json, file, ensure_ascii=False, indent=4)

    # Delete the user-defined language JSON file
    os.remove(extracted_file)

    print(f'Updated JSON file saved as {final_output_file}')
    print(f'Temporary translation file {extracted_file} deleted.')

if __name__ == "__main__":
    main()
