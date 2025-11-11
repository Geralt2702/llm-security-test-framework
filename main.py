import csv
import time
from test_cases import test_cases
from executor import query_model
from analyzer import analyze_response

models = ["mistral", "gemma3"]

def run_tests():
    results = []
    with open("llm_security_tests.csv", mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Model", "Category", "Prompt", "Response", "Alert"])
        for model in models:
            print(f"Testing model: {model}")
            for category, prompts in test_cases.items():
                for prompt in prompts:
                    print(f"Sending prompt: {prompt}")
                    response = query_model(model, prompt)
                    alert = analyze_response(response)
                    print(f"Response: {response[:200]}... Alert: {alert}")
                    writer.writerow([model, category, prompt, response, alert])
                    results.append((model, category, prompt, response, alert))
                    time.sleep(1)
    generate_html_report(results)

def generate_html_report(results):
    html_content = "<html><head><title>LLM Security Test Report</title></head><body>"
    html_content += "<h1>LLM Security Test Report</h1>"
    html_content += "<table border='1' style='border-collapse:collapse;'><tr><th>Model</th><th>Category</th><th>Prompt</th><th>Response</th><th>Alert</th></tr>"
    for (model, category, prompt, response, alert) in results:
        row_color = "#FFCCCC" if alert else "#CCFFCC"
        html_content += f"<tr style='background-color:{row_color};'><td>{model}</td><td>{category}</td><td>{prompt}</td><td>{response[:300]}</td><td>{alert}</td></tr>"
    html_content += "</table></body></html>"

    with open("llm_security_test_report.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Generated llm_security_test_report.html")

if __name__ == "__main__":
    run_tests()
