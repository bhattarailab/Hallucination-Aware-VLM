import json
import spacy
import requests
import ast
import en_core_web_sm

# Load spaCy's language model
nlp = spacy.load("en_core_web_sm")

# Set up OpenAI API key
api_key = "********"   # Your OpenAI API key
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Define category mappings
categories = {


    "color": {
    "red": [
        "red", "reddish", "reddish pink", "reddish brown", "dark red", "light red",
        "pinkish red", "red pink", "pink orange", "red orange", "pinkish orange",
        "pinkish brown", "brownish red", "brick red", "scarlet", "crimson", "maroon",
        "rose red"
    ],
    "pink": [
        "pink", "pinkish", "pinkish yellow", "pinkish brown", "pinkish orange", 
        "light pink", "pink light", "reddish pink", "red pink", "yellowish pink",
        "light pinkish", "dark pinkish", "pinkish red", "blush pink", "rose pink", 
        "coral pink", "hot pink", "pastel pink", "peach pink", "baby pink","flesh", 
        "light flesh", "dark flesh", "skin tone", "peach flesh", "flesh colored",
        "beige flesh", "rosy flesh", "normal", "flesh tone", "flesh color", "flesh shade",
        "normal color", "normal shade", "normal hue", "normal tone", "normal pigment",
        "normal coloration", "light", "lighter", "lightest", "lightest pink", "lightest shade",
        "same color", "typical color", "typical shade", "typical hue", "typical tone",
        "similar color", "similar shade", "similar hue", "similar tone", "similar pigment",
    ],
    "orange": [
        "orange", "yellowish orange", "orange yellow", "yellow orange", 
        "pinkish orange", "dark orange", "light orange", "brownish orange", 
        "tangerine", "amber", "burnt orange", "apricot", "coral orange", 
        "golden orange", "peach orange"
    ],
    "yellow": [
        "yellow", "yellowish", "yellowish pink", "yellowish brown", 
        "brownish yellow", "yellowish white", "white yellow", "light yellow",
        "dark yellow", "light yellowish", "dark yellowish", "pinkish yellow", 
        "yellow-orange", "golden yellow", "mustard yellow", "lemon yellow", 
        "sunflower yellow", "pale yellow", "cream yellow"
    ],
    "brown": [
        "brown", "brownish", "brownish yellow", "brownish red", 
        "brownish pink", "brownish orange", "reddish brown", 
        "yellowish brown", "light brown", "light brownish", 
        "dark brownish", "pinkish brown", "tan", "beige", 
        "chocolate brown", "coffee brown", "caramel brown", "rust brown"
    ],
    "blue": [
        "blue", "bluish", "dark blue", "blue dark", "bluish green", "light bluish", "dark bluish",
        "greenish blue", "blue green", "green bluish", "light bluish", "dark bluish",
        "sky blue", "navy blue", "royal blue", "aqua blue", "teal blue", "light blueish","dark blueish",
        "baby blue", "electric blue", "cobalt blue", "cerulean blue", "blueish","blueish green", "green blueish",
        "blue-colored", "bluish hue", "blueish hue", "blueish color", "blueish shade", "blueish tone",
        "blueish dye", "blueish tint", "blueish pigment", "blueish paint", "blueish material", "blueish fabric"
    ],
    "green": [
        "green", "greenish", "bluish green", "green bluish", "greenish blue", 
        "blue green", "light green", "light greenish", "dark greenish", 
        "lime green", "forest green", "emerald green", "olive green", 
        "mint green", "sea green", "sage green", "pastel green", "blueish green", "green blueish"
    ],
    "white": ["white", "off white", "ivory", "cream", "light gray"],
    "dark": ["black", "charcoal", "gray", "dark gray", "light gray", "dark",
    ],
    "n/a":["N/A","n/a", "none", "not mentioned", "not specified", "not provided","N/A.", "n/a.", "N/A"]
},


    "location": {
    "center": [
        "center", "middle", "centre", "centrally", "central", 
        "mid center", "center mid", "mid", "midpoint", "centered"
    ],
    "left": [
        "left", "center left", "left center", "top left", "upper left", 
        "bottom left", "lower left", "mid left", "left mid", "left top",
        "left bottom", "left center", "center left", "left mid", "mid left",
        "left top", "left bottom", "left center", "center left", "left mid", "mid left",
        "9'o clock", "9 o'clock"
    ],
    "right": [
        "right", "center right", "right center", "top right", "upper right", 
        "bottom right", "lower right", "mid right", "right mid", "right top",
        "right bottom", "right center", "center right", "right mid", "mid right",
        "right top", "right bottom", "right center", "center right", "right mid", "mid right",
        "3'o clock", "3 o'clock"
    ],
    "top": [
        "top", "upper", "above", "top center", "upper center", 
        "center top", "top left", "upper left", "top right", "upper right", 
        "mid top", "top mid", "12'o clock", "12 o'clock"
    ],
    "bottom": [
        "bottom", "lower", "below", "bottom center", "lower center", 
        "center bottom", "bottom left", "lower left", "bottom right", 
        "lower right", "mid bottom", "bottom mid", "6'o clock", "6 o'clock"
    ],
    "surrounding": ["surrounding", "around", "near", "nearby", "peripheral", "adjacent", "bordering", "encompassing", "encircling", "flanking"],
    "background":["scattered", "throughout", "background", "distributed", "dispersed", "spread out", "sporadic", "all over", "widespread", "consistent", "surface"],
    "n/a":["N/A","n/a", "none", "not mentioned", "not specified", "not provided","N/A.", "n/a.", "N/A"]
},


    "landmark": {"colon": ["colon", "Colon", "colon.", "Colon."],
                     "cecum": ["cecum", "Cecum", "cecum.", "Cecum."],
                     "z-line": ["z-line", "Z-line", "z-line.", "Z-line.", "z line", "Z line", ""],
                     "pylorus": ["pylorus", "Pylorus", "pylorus.", "Pylorus."],
                     "n/a": ["N/A","n/a", "none", "not mentioned", "not specified", "not provided","N/A.", "n/a.", "N/A"]},


    "polyp": {"zero": ["zero", "0", "Zero.", "zero.", "0."],
                "single": ["single", "1", "Single.", "single.", "1."],
                "multiple": ["multiple", "Multiple.", "multiple.", "more than one", "several", "numerous", "many"],
                "n/a": ["N/A","n/a", "none", "not mentioned", "not specified", "not provided","N/A.", "n/a.", "N/A"]},


    "yes_no": {"Yes":["yes", "Yes","Yes.", "yes."],
                 "No":["no", "No","No.", "no."],
                 "n/a":["N/A","n/a", "none", "not mentioned", "not specified", "not provided","N/A.", "n/a.", "N/A"]}
}


# Define category groups
color_question_indices = {1, 4}
location_question_indices = {2, 5}

# Function to lemmatize text
def lemmatize(word):
    doc = nlp(word.lower().replace("-", " "))
    return " ".join(token.lemma_ for token in doc).strip()

# Function to categorize answers for a given image in a **single prompt**
def categorize_answers_bulk(answers):
    lemmatized_answers = [lemmatize(ans) for ans in answers]
    
    prompt = f"""
    You are an expert in linguistic and contextual similarity. 

    You are given a list of 12 answers and a predefined dictionary of categories, where each category contains a set of synonymous words representing variations of the same concept.

    ### Your Task:
    - Determine which **category (or categories)** each answer belongs to, selecting the most relevant **subcategory** based on **meaning and similarity**, not just exact matches.
    - Answers may match multiple categories, so consider **synonyms, similar meanings, and semantic relationships** while selecting the best match.
    - Maintain the **original order of the answers** in the output, ensuring they are returned in the **exact same sequence** as provided.
    - **Use fuzzy matching and semantic similarity** to handle variations in wording, spelling, and meaning.

    ### Additional Context:
    - **Words with similar meanings** should be grouped accordingly. For example:
        - `"peripheral"`, `"periphery"`, and `"surrounding"` all match the **"surrounding"** subcategory under **"location"**.
        - `"crimson"`, `"scarlet"`, and `"maroon"` all match the **"red"** subcategory under **"color"**.
    - **Semantic similarity should be prioritized over direct word matching**, using **fuzzy matching, embeddings, or contextual similarity**.
    -  **If an answer belongs to multiple categories**, list all relevant categories and subcategories.

    ### Expected Distributions:
    - **Answer 1** is related to **landmark**.
    - **Answers 2 and 5** are related to **color**.
    - **Answers 3 and 6** are related to **location**.
    - **Answers 4, 8, 9, 10, 11, and 12** are related to **yes_no**.
    - **Answer 7** is related to **polyp**.

    Ensure that your classification aligns with these expected distributions.

    ### Input Data:
    **Categories:**  
    {categories}

    **Answers:**  
    {lemmatized_answers}

    Now, categorize the answers based on the provided category mappings and return the results in the required format.
        
    ### **🚨 STRICT INSTRUCTIONS (FOLLOW EXACTLY)**
    ✅ **1. Maintain Answer Order:** Do not change the order of answers. The i-th answer in the input must correspond to the i-th output.  
    ✅ **2. Return a List of Lists:** Each answer should be returned as a list inside another list, even if it belongs to only one category.  
    ✅ **3. Empty Lists for No Match:** If an answer does not match any category, return an empty list `[]`. But remember if an answer is 'N\A' or 'not mentioned' or other variations, it should be categorized as 'n/a'.
    ✅ **4. Do NOT Wrap in Code Blocks:** Do **not** use `python`, `plaintext`, `json`, or any other formatting blocks in your response.  
    ✅ **5. No Extra Text:** Do **not** add explanations, headers, prefixes, or additional formatting—return only the structured list.


    ### **Expected Output Format (Strictly a List of Lists in Plain Text, Matching Each Answer in Order):**  
    ✅ **Valid Examples (Ensure strict order preservation):**  
    `[["cecum"], ["pink","red"], ["n/a"], ["Yes"], ["white"], ["left"], ["multiple"], ["Yes"], ["Yes"], ["Yes"], ["No"], ["No"]]`
    
    ❌ **Invalid Examples (DO NOT return these formats):**  
    - ```python ["red"] ``` ❌ *(Incorrect: Do NOT wrap output in a code block.)*  
    - ```json ["red"] ``` ❌ *(Incorrect: Do NOT return JSON-formatted output.)*  
    - `"Right lower abdomen. ["right", "bottom"]"` ❌ *(Incorrect: Do NOT include extra text before the list.)*  
    - `"["red"]."` ❌ *(Incorrect: Do NOT add punctuation outside of the list.)*  
    
    """


    payload = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300,
        "temperature": 0.1
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        # Ensure the response contains the expected structure
        if "choices" not in data or not data["choices"]:
            print("Error: No choices returned from OpenAI.")
            return [[]] * len(answers)
        
        content = data["choices"][0]["message"]["content"].strip()

        # Use ast.literal_eval to safely parse Python-style lists instead of JSON
        try:
            parsed_output = ast.literal_eval(content)
            if isinstance(parsed_output, list) and all(isinstance(i, list) for i in parsed_output):
                return parsed_output
            else:
                print("Error: OpenAI response is not in expected format.")
                return [[]] * len(answers)
        except (SyntaxError, ValueError):
            print("Error: Could not parse OpenAI response. Response received:", content)
            return [[]] * len(answers)

    except requests.exceptions.RequestException as e:
        print("Error: Request to OpenAI API failed:", str(e))
        return [[]] * len(answers)

# Process single image
def process_image(image_path, qa_pairs):
    answers = [qa["answer"].strip() for qa in qa_pairs]
    print (answers)
    
    # Single prompt categorization for **all** answers in the image
    results = categorize_answers_bulk(answers)

    print (results)

    updated_qa_pairs = []
    for i, qa in enumerate(qa_pairs):
        chosen_answer = results[i] if i < len(results) else []
        updated_qa_pairs.append({
            "question": qa["question"],
            "given answer": qa["answer"],
            "chosen answer": chosen_answer
        })

    return image_path, updated_qa_pairs

# Load input JSON
input_file = "../results/qwen_caption_hal_aware_caption2vqa.json"
with open(input_file) as f:
    data = json.load(f)

# Process images 
updated_data = {}
count = 0

for img, qa_pairs in data.items():
    # if count >= 100:
    #     break  # Stop processing after 3 iterations
    
    updated_data[img] = process_image(img, qa_pairs)[1]
    count += 1  # Increment the counter
    print ("Processing image", count)

# Save output JSON
output_file = "../results/qwen_caption_hal_aware_caption2vqa_parsed.json"
with open(output_file, "w") as f:
    json.dump(updated_data, f, indent=4)