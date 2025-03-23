from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the CSV file into a DataFrame
df = pd.read_csv(r"dataset.csv")

# Dictionary for English → Konkani
english_to_konkani = {}

# Process each row of the CSV for English → Konkani mapping
for index, row in df.iterrows():
    # Extract English word (first column)
    if pd.notna(row.iloc[0]) and isinstance(row.iloc[0], str):
        english_word = row.iloc[0].strip().lower()
    else:
        continue  # Skip invalid rows

    # Collect all Konkani translations from columns 2 and beyond
    translations = [
        str(row.iloc[i]).strip()
        for i in range(1, len(row)) if pd.notna(row.iloc[i]) and isinstance(row.iloc[i], str)
    ]

    # Store in English-to-Konkani dictionary
    if english_word in english_to_konkani:
        english_to_konkani[english_word].extend(translations)
    else:
        english_to_konkani[english_word] = translations

# Function to translate a given term in either direction
def translate_term(term):
    term_lower = term.strip().lower()

    # **English → Konkani**
    if term_lower in english_to_konkani:
        return [(None, english_to_konkani[term_lower])]

    # **Konkani → English (Search in DataFrame Columns 2 and Beyond)**
    for index, row in df.iterrows():
        konkani_words = [
            str(row.iloc[i]).strip().lower()
            for i in range(1, len(row)) if pd.notna(row.iloc[i]) and isinstance(row.iloc[i], str)
        ]

        if term_lower in konkani_words:
            return [(None, [row.iloc[0]])]  # Return the English word from the first column

    return [(None, ["Translation not found"])]

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get("query", "").lower()
    matches = list(set(english_to_konkani.keys()))  # Autocomplete only for English words
    suggestions = [word for word in matches if word.startswith(query)]
    return jsonify(suggestions[:5])

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/admin_vocab')
def admin_vocab():
    return render_template('admin_vocab.html')

@app.route('/phrases')
def phrases():
    return render_template('phrases.html')

@app.route('/designation')
def designation():
    return render_template('designation.html')

@app.route('/department')
def department():
    return render_template('department.html')

@app.route('/degrees')
def degrees():
    return render_template('degrees.html')


@app.route('/translate', methods=['POST'])
def translate():
    input_word = request.form['input_word']
    translations = translate_term(input_word)
    return render_template('W2W.html', input_word=input_word, translations=translations)

if __name__ == '__main__':
    app.run(debug=True)
