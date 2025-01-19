import json

def convert_to_jsonl_for_evaluation(data, filename):
    with open(filename, 'w') as f:
        for product in data['products']:
            entry = {
                "custom_id": product["product_id"],
                "method": "POST", 
                "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-4o-mini",
                    "messages": [
                        {
                            "role": "system",
                            "content": """Assume you are a category manager for an e-commerce company based in India.
                            You have been tasked with cleaning up the product categorization of the product catalogue.
                            Objective: Evaluate whether the product is correctly mapped to its given category 
                            based on the product's name and description.
                                
                                Instructions:
                                You will receive a dataset containing the following columns:
                                - Product ID: A unique identifier for the product.
                                - Product Name: The name of the product.
                                - Product Description: The description of the product.
                                - Category: The category to which the product is tagged.

                                Output Format:
                                For each product, return a valid JSON with the following fields:
                                - Category Name: The category from the input data.
                                - Product ID: The identifier from the input data.
                                - Product Name: The name from the input data.
                                - Tagging: Mark the product-category mapping as "Correct" or "Incorrect."
                                - Confidence Score: A number between 0 and 1 indicating your 
                                confidence in the correctness of the categorization.
                                """
                        },
                        {
                            "role": "user",
                            "content": json.dumps({
                                "product_id": product["product_id"],
                                "name": product["name"],
                                "description": product["description"],
                                "category": product["category"]
                            })
                        }
                    ]
                }
            }
            json.dump(entry, f)
            f.write('\n')
def convert_to_jsonl_for_embeddings(data, output_file):
    """Convert product data to JSONL format for embeddings"""
    with open(output_file, 'w') as f:
        for product in data['products']:
            entry = {
                "custom_id": product["product_id"],
                "method": "POST",
                "url": "/v1/embeddings", 
                "body": {
                    "model": "text-embedding-3-small",
                    "input": f"Product name is: {product['name']}\nProduct description is: {product['description']}"
                }
            }
            json.dump(entry, f)
            f.write('\n')

def main():
    # Read JSON data from file
    with open('product_data.json', 'r') as f:
        data = json.load(f)

    # Convert the given JSON data to a JSONL file
    convert_to_jsonl_for_evaluation(data, 'products_data_evaluation.jsonl')

    # Convert the given JSON data to a JSONL file for embeddings
    convert_to_jsonl_for_embeddings(data, 'products_data_embeddings.jsonl')

if __name__ == "__main__":
    main()