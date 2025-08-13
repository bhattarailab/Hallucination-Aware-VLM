import json

def evaluate_vqa_answers(groundtruth_file, test_file, output_file):
    """
    Compares the chosen answers from a test file with ground truth answers.
    Votes as correct (1) if any test answer is in the ground truth answer list, otherwise incorrect (0).
    
    Parameters:
        groundtruth_file (str): Path to the ground truth JSON file.
        test_file (str): Path to the test JSON file.
        output_file (str): Path to save the evaluation results.
    """
    
    # Load the JSON files
    with open(groundtruth_file, "r", encoding="utf-8") as f:
        groundtruth_data = json.load(f)
    
    with open(test_file, "r", encoding="utf-8") as f:
        test_data = json.load(f)
    
    evaluation_results = {}  # Stores evaluation per image
    total_correct = 0
    total_questions = 0

    # Iterate through images in the test file
    for image_path, test_questions in test_data.items():
        if image_path not in groundtruth_data:
            print(f"Skipping {image_path}, not found in ground truth.")
            continue
        
        groundtruth_questions = groundtruth_data[image_path]
        image_results = []

        # Ensure both lists have the same number of questions
        min_length = min(len(test_questions), len(groundtruth_questions))

        for i in range(min_length):
            test_qa = test_questions[i]
            groundtruth_qa = groundtruth_questions[i]

            test_answer = set(test_qa.get("chosen answer", []))  # Get list, default to empty
            groundtruth_answer = set(groundtruth_qa.get("chosen answer", []))  # Default empty

            if not groundtruth_answer:
                print ("Groundtruth empty case, skip this case")
                total_questions -= 1
                is_correct = 0
            elif test_answer & groundtruth_answer:
                is_correct = 1  # Correct match
            else:
                is_correct = 0  # Incorrect match

            image_results.append({
                "question": test_qa.get("question", ""),
                "test answer": list(test_answer),
                "groundtruth answer": list(groundtruth_answer),
                "correct": is_correct
            })

            total_correct += is_correct
            total_questions += 1

        evaluation_results[image_path] = image_results


    # Calculate overall accuracy
    accuracy = (total_correct / total_questions) * 100 if total_questions > 0 else 0
    print(f"Total Correct: {total_correct}/{total_questions} | Accuracy: {accuracy:.2f}%")

    # Save evaluation results to JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(evaluation_results, f, indent=4)

    print(f"Evaluation results saved to {output_file}")

# Example Usage
evaluate_vqa_answers(
    groundtruth_file="../dataset/Gut-VLM/train_test_split/VQA_format_testset_only.json", 
    test_file="../results/qwen_caption_hal_aware_caption2vqa_parsed.json",
    output_file="../results/qwen_hal_aware_QAAS_results.json"
)