import requests
import json

class SeleniumToPlaywrightConverter:
    def __init__(self, model_name="llama3.2:3b"):
        self.model = model_name
        self.api_url = "http://localhost:11434/api/generate"
        self.logs = []


    def log(self, level, message):
        self.logs.append({"level": level, "message": message})

    def convert(self, java_code: str) -> str:
        self.logs = []
        self.log("info", f"Starting conversion using local LLM: {self.model}")
        
        prompt = self._construct_prompt(java_code)
        
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2, 
                    # Lower context window to avoid OOM on smaller machines
                    "num_ctx": 2048 
                }
            }
            
            self.log("info", "Sending request to Ollama...")
            response = requests.post(self.api_url, json=payload, timeout=120)
            
            if response.status_code != 200:
                error_msg = f"Ollama Error ({response.status_code}): {response.text}"
                self.log("error", error_msg)
                return f"// {error_msg}"
                
            result = response.json()
            generated_text = result.get('response', '')
            
            # Extract code block if present
            code = self._clean_output(generated_text)
            
            self.log("info", "Conversion successful.")
            return code
            
        except requests.exceptions.ConnectionError:
            self.log("error", "Could not connect to Ollama. Is it running on port 11434?")
            return "// Error: Ollama is not accessible at localhost:11434."
        except Exception as e:
            self.log("error", f"LLM Error: {str(e)}")
            return f"// Error converting code: {str(e)}"


    def _construct_prompt(self, java_code: str) -> str:
        return f"""
You are an expert Test Automation Engineer. Convert the following Selenium Java code to Playwright TypeScript.

**Rules:**
1. Use 'test' and 'expect' from '@playwright/test'.
2. Use async/await for all actions.
3. Use modern locators (e.g., page.locator(), page.getByRole()).
4. Do NOT include markdown formatting (like ```typescript). Just output the code.
5. If there are assertions, convert them to `expect()`.

**Input (Java):**
{java_code}

**Output (Playwright TypeScript):**
"""

    def _clean_output(self, text: str) -> str:
        # Remove markdown code blocks if the LLM adds them
        text = text.strip()
        if text.startswith("```typescript"):
            text = text.replace("```typescript", "", 1)
        elif text.startswith("```ts"):
            text = text.replace("```ts", "", 1)
        elif text.startswith("```"):
            text = text.replace("```", "", 1)
            
        if text.endswith("```"):
            text = text[:-3]
            
        return text.strip()

if __name__ == "__main__":
    converter = SeleniumToPlaywrightConverter()
    sample = 'driver.get("http://google.com");'
    print(converter.convert(sample))
