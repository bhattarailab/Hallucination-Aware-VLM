import json
import requests

# OpenAI API key
api_key = '*******' # your OpenAI API Key

# API Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Your **original questions**:
questions = [
    "Which anatomical landmark or organ does the image belong to among colon, cecum, pylorus, or z-line? Just select one of the following if it's present in the context text. If not, return N/A.",
    "If the color of the anatomical landmark is explicitly mentioned, just answer in a single or two words maximum. If it's not mentioned, return N/A.",
    "If the location or position of the anatomical landmark is explicitly mentioned, where is it located? Just answer with a location or position describing word. Absolutely limit your answer to a single or two words at maximum. If it's not mentioned, return N/A.",
    "Is there any abnormality present in the image? If yes, return Yes. If not, return No.",
    "If the color of the abnormality is explicitly mentioned, just answer in a single or two words maximum. If it's not mentioned, return N/A.",
    "If the location or position of the abnormality is explicitly mentioned, just answer in a single or two words maximum. If it's not mentioned, return N/A.",
    "Are there any polyps present? Just answer how many polyps are there? Possible answers are (Zero, Single, Multiple). If it's not mentioned, return N/A.",
    "Are there any instruments visible in the image? If yes, return Yes. If not, return No. If it's not mentioned, return N/A.",
    "Are there any signs of inflammation present in the image? If yes, return Yes. If not, return No. If it's not mentioned, return N/A.",
    "Is there evidence of bleeding in the image? If yes, return Yes. If not, return No. If it's not mentioned, return N/A.",
    "Are there any foreign bodies present in the image? If yes, return Yes. If not, return No. If it's not mentioned, return N/A.",
    "Are there any signs of infection present in the image? If yes, return Yes. If not, return No. If it's not mentioned, return N/A."
]

# Function to generate AI responses in batch
def generate_answers_bulk(context):
    """
    Sends all questions in a single API call for better accuracy, efficiency, and cost reduction.
    """

    if not context.strip():
        return ["N/A"] * len(questions)

    prompt = "You are given this extracted text from a medical image report:\n\n"
    prompt += f"------\n{context}\n------\n\n"
    prompt += "Your task is to answer the following questions **strictly based on the provided text**.\n"
    prompt += "✅ Keep answers **1-2 words max**.\n"
    prompt += "✅ Just return the answer don't tag question in the answer.\n"
    prompt += "✅ Extract and return **exact words** from the text.\n"
    prompt += "✅ If the information is missing, return **'N/A'**.\n"
    prompt += "✅ **Do NOT infer, explain, or add extra knowledge**.\n\n"

    # Additional prompts to enforce answer ordering
    prompt += "⚠️ **IMPORTANT:**\n"
    prompt += "- Answer **each question in order**, prefixed by `A1:`, `A2:`, ..., `A12:`.\n"
    prompt += "- **Do NOT** swap, mix, or skip answers. Ensure strict ordering.\n"
    prompt += "- Each answer must be **directly below** its corresponding question.\n"
    prompt += "- **Missing information?** Write `'N/A'` explicitly.\n\n"
    prompt += "**Now, answer the following questions:**\n"
    for i, question in enumerate(questions, 1):
        prompt += f"{i}{question}\nA{i}:\n"

    payload = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300,  # Enough for all answers
        "temperature": 0.1,
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        raw_answers = data["choices"][0]["message"]["content"].split("\n")
        print (raw_answers)

        answers = []
        for i in range(len(questions)):
            if i < len(raw_answers):
                answer = raw_answers[i].replace(f"A{i+1}:", "").strip()
                answers.append(answer if answer else "N/A")
            else:
                answers.append("N/A")
        return answers

    except Exception as e:
        print(f"Error processing bulk request: {e}")
        return ["Error"] * len(questions)

# Load JSON file
try:
    with open("../results/final_qwen_caption_hal_aware_results.json", "r") as f:  # Replace with your results file path
        data = json.load(f)
except FileNotFoundError:
    print("Error: File not found.")
    exit()

# Initialize dataset
vqa_dataset = {}

print("Generating answers...")
count = 0

for entry in data:
    
    # Case 1: 'image_path' exists as a single string
    if "image_path" in entry:
        image_id = entry["image_path"]
    # Case 2: 'images' exists as a list
    elif "images" in entry and isinstance(entry["images"], list) and entry["images"]:
        image_id = entry["images"][0]  # Use the first image path
    # Fallback case
    else:
        image_id = f"image_{count}"


    response_text = entry.get("response", "").strip()
    
    if not response_text:
        print(f"Warning: No response text found for {image_id}")
        continue

    # Get all answers in one API call
    answers = generate_answers_bulk(response_text)
    print (answers)

    vqa_dataset[image_id] = [{"question": q, "answer": a} for q, a in zip(questions, answers)]
    
    count += 1
    print(f"Processed {count} images...")

# Save the dataset
output_file = "../results/qwen_caption_hal_aware_caption2vqa.json" # Replace with your output file path
with open(output_file, "w") as f:
    json.dump(vqa_dataset, f, indent=4)

print(f"VQA dataset generated and saved as {output_file}")