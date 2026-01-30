# Project Constitution (gemini.md)

## 🌟 North Star
A web-based application that converts Selenium Java test code into readable Playwright JavaScript/TypeScript code. Users input Java code via the UI, and the system displays the converted code and saves it to a new directory.

## 💾 Data Schemas

### 1. ConversionRequest
- **Source**: UI Input
- **Structure**:
  ```json
  {
    "input_code": "string (Java Selenium Code)",
    "target_language": "string ('typescript' | 'javascript')",
    "output_dir": "string (Optional path to save)"
  }
  ```

### 2. ConversionResult
- **Source**: Conversion Tool Output
- **Structure**:
  ```json
  {
    "success": "boolean",
    "converted_code": "string (Playwright TS/JS Code)",
    "logs": [
      {
        "level": "string ('info' | 'warning' | 'error')",
        "message": "string"
      }
    ]
  }
  ```

## 🧠 Behavioral Rules
1.  **Readability Over Strictness**: Prioritize generating idiomatic, readable Playwright code over an exact line-by-line translation of the Java Selenium code.
2.  **Handling Ambiguity**: If a Selenium command implies a wait or a complex interaction, use Playwright's auto-waiting web assertions where possible.
3.  **UI Feedback**: The UI must show both the converted code and any "Translation Notes" (logs) for things that couldn't be perfectly mapped.

## 🏗️ Architectural Invariants
1.  **3-Layer Architecture:**
    -   Layer 1: Architecture (`architecture/` - SOPs)
    -   Layer 2: Navigation (LLM Reasoning)
    -   Layer 3: Tools (`tools/` - Deterministic Scripts)

2.  **Protocol**: B.L.A.S.T. (Blueprint, Link, Architect, Stylize, Trigger)

3.  **Data-First**: No coding until Schema is defined.

4.  **Self-Annealing**: Analyze -> Patch -> Test -> Update Architecture.

