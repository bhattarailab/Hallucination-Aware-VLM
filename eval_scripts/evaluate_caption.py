import json
import requests

# OpenAI API key
api_key = '*********' # Your OpenAI API key

# API Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Load test and ground truth JSON files
def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
    
# Save results to JSON file
def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

# Rating scale
rating_scale = [
    "1 - (Poor) Completely incorrect or misleading",
    "2 - (Not Good) Significant differences affecting diagnosis",
    "3 - (Alright) Some differences, but overall meaning preserved",
    "4 - (Good) Minor differences, clinically acceptable",
    "5 - (Very Good) Nearly identical, all findings correctly described"
]

# Function to compare descriptions
def compare_descriptions(desc1, desc2):
    """
    Compares two medical image descriptions and assigns a similarity rating.
    """
    
    prompt = f"""
    You are an expert in medical image analysis and textual interpretation. Your task is to compare two given descriptions of a medical image and determine how well they match in terms of correctness and clinical significance.
    
    ---
    ### **Instructions:**
    1. **Strictly compare the two descriptions** and evaluate their similarity.
    2. Consider whether they describe the same anatomical landmarks, abnormalities, locations, and key clinical findings.
    3. Do **NOT infer** or add external knowledge. Base your answer **strictly** on the given descriptions.
    4. Answer the following questions while comparing the descriptions:
       - Which anatomical landmark does the image belong to?
       - What color is the abnormality, if present?
       - What color is the anatomical landmark?
       - Are there any polyps present? If yes, how many?
       - Where in the image is the abnormality, if present?
       - Are there any abnormalities in the image?
       - Are there any anatomical landmarks in the image?
       - Are there any instruments in the image? If found, where and how many?
       - Are there any signs of inflammation?
       - Is there any evidence of bleeding?
       - Are there any foreign bodies present?
       - Are there any signs of infection?
    5. Rate the similarity using the following scale:
    
       - **5 - (Very Good)**: Nearly identical, all findings correctly described.
       - **4 - (Good)**: Minor differences, clinically acceptable.
       - **3 - (Alright)**: Some differences, but overall meaning preserved.
       - **2 - (Not Good)**: Significant differences affecting diagnosis.
       - **1 - (Poor)**: Completely incorrect or misleading.
    
    ---
    
    **Description 1:**  
    {desc1}  
    
    **Description 2:**  
    {desc2}  
    
    ---
    
    **Your evaluation:**
    - **Match?**: (Yes/No)
    - **Similarity Rating**: (1 to 5)
    - **Brief Justification**: (Explain why you assigned this rating)
    """
    
    payload = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200,
        "temperature": 0.1,
    }
    
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        evaluation = data["choices"][0]["message"]["content"].strip()
        
        # Extract numerical rating from response
        score = next((int(s) for s in evaluation.split() if s.isdigit() and 1 <= int(s) <= 5), None)
        return score if score else 0
    except Exception as e:
        print(f"Error processing request: {e}")
        return 0

# Match test file responses with ground truth based on image path and compare
def evaluate_json_files(test_file, groundtruth_file, output_file):
    test_data = load_json(test_file)
    groundtruth_data = load_json(groundtruth_file)
    
    scores = []
    results = []

    count = 0
    
    for test_entry in test_data:
        test_image = test_entry.get("image_path")
        test_response = test_entry.get("response")

        for gt_entry in groundtruth_data:
            if test_image in gt_entry.get("images", []):
                gt_response = gt_entry.get("response")
                score = compare_descriptions(test_response, gt_response)
                scores.append(score)
                results.append({
                    "image": test_image,
                    "score": score
                })
                print(f"Image: {test_image}\nScore: {score}\n")
                break
        count += 1
    
    # Compute average score
    avg_score = sum(scores) / len(scores) if scores else 0
    print(f"\nAverage Similarity Score: {avg_score:.2f}")
    
    results.append({"average_score": avg_score})
    save_json(output_file, results)
    return avg_score


# Example usage
test_json_list = [ '../results/final_qwen_caption_hal_aware_results.json']
groundtruth_json_path = "../results/groundtruth_test_captions.json"
output_json_list = ["../results/qwen_caption_hal_aware_cap_eval.json"]

for i, j in zip(test_json_list, output_json_list):
    average_score = evaluate_json_files(i, groundtruth_json_path, j)