# PromptCrafter2 User Manual (Streamlit Version)

## Application Overview

PromptCrafter2 is a web application designed to help you generate prompts for Stable Diffusion image generation. This app utilizes AI models or templates to create prompts, assisting you in creating images effectively.

## How to Launch the Application

1. Clone or download the repository and navigate to the promptcrafter2 folder.

2. **Create and activate a virtual environment** (recommended)

   **macOS/Linux:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   **Windows:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. To install the required libraries, run the following command in the command line or terminal:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the following command to launch the application:

   ```bash
   streamlit run app.py
   ```

5. The application will automatically open in your browser (or navigate to http://localhost:8501)

## Main Screen Operation

### Tab Structure

The application has the following 5 tabs:

1. **Prompt Generation** - Create and generate prompts
2. **Search** - Search for prompts
3. **Category Selection** - Select keywords from categories
4. **Favorites Management** - Manage favorite prompts and keywords
5. **History** - View past prompt generation history

### 1. Prompt Generation Tab

#### Keyword Input
* Enter keywords to use for prompt generation in the text area
* For multiple keywords, separate them with commas
* Example: `beautiful landscape, sunset, mountains`

#### Prompt Generation Buttons
* **Generate Prompt (Both)**: Generate both Positive and Negative prompts
* **Generate Positive Only**: Generate only Positive prompt
* **Generate Negative Only**: Generate only Negative prompt
* **Add to Favorites**: Add keywords to favorites
* **Clear Keywords**: Clear the keyword input field

#### Generated Prompt Operations
* **Positive Prompt:**
  - **Copy Positive**: Copy to clipboard
  - **Add to Favorites**: Register to favorites
  - **Clear**: Clear the prompt field

* **Negative Prompt:**
  - **Copy Negative**: Copy to clipboard
  - **Add to Favorites**: Register to favorites
  - **Clear**: Clear the prompt field

### 2. Search Tab

#### Prompt Search
1. Enter keywords in the search keyword input field
2. Click the **Search** button
3. Search results will be displayed
4. Select checkboxes to automatically add to keyword input field

* Supports both Japanese and English search
* Searches across categories, subcategories, and keywords

### 3. Category Selection Tab

#### Select Keywords from Categories
1. Select a category of interest from the top tabs (People, Background, Nature, etc.)
2. Click the expand icon for subcategories
3. Select keywords using checkboxes
4. Selected keywords are automatically added to the keyword input field

**Available Categories:**
* People
* Background
* Nature
* Buildings & Structures
* Art
* Concept
* Fantasy
* Cyberpunk
* Other style categories

**Favorites Category:**
* The Favorites category in the special categories section shows only the Keywords subcategory
* This allows quick access to your saved keyword combinations

### 4. Favorites Management Tab

#### Manage Favorite Prompts and Keywords
* **Positive Tab**: List of Positive prompt favorites
* **Negative Tab**: List of Negative prompt favorites
* **Keywords Tab**: List of keyword favorites

Each favorite has the following actions:
* **Copy**: Copy to clipboard
* **Delete**: Remove from favorites

### 5. History Tab

#### Prompt Generation History
* Past generated prompts are displayed chronologically
* Up to 100 entries are saved (oldest are automatically deleted)

**History Entry Information:**
* Generation date and time
* Keywords used
* LoRA used
* Positive Prompt
* Negative Prompt

**History Actions:**
* **Reuse**: Restore keywords and prompts for reuse
* **Copy (Pos)**: Copy Positive prompt
* **Copy (Neg)**: Copy Negative prompt
* **Delete**: Delete this history entry
* **Clear All History**: Clear all history

## Sidebar (Settings) Operation

### 1. LoRA Model Selection
* Select the LoRA model to use from the dropdown menu
* Select "None" if you don't want to use a LoRA

### 2. Template Settings

#### Positive Template
* Select the Positive prompt template you want to use
* Options:
  - realistic_positive_prompt_template (Realistic)
  - 2d_positive_prompt_template (2D)
  - 2.5d_positive_prompt_template (2.5D)
  - NSFW templates (for each style)

#### Negative Template
* Select the Negative prompt template you want to use
* Same style options as Positive templates

### 3. AI Generation Settings

#### Use AI Model
* Check to enable prompt generation using AI model
* Uncheck to use template-based generation

#### Model Name (When using AI model)
* Enter the name of a text generation model downloadable from Hugging Face Hub
* Default: `Gustavosta/MagicPrompt-Stable-Diffusion`

#### AI Generation Mode (When using AI model)
* **both**: AI generates both Positive and Negative
* **positive_only**: AI generates only Positive
* **negative_only**: AI generates only Negative

## Configuration File Editing

### 1. `app_settings.json`
* File that stores application settings
* Changes made in the sidebar are automatically saved to this file
* Can also be edited directly (requires app restart)

### 2. `categories.json`
* File describing categories and keywords
* Editing this file allows you to change categories and keywords displayed in the GUI
* Written in JSON format

### 3. `prompt_history.json`
* File where prompt generation history is saved
* Automatically generated and updated
* Deleting this file will reset the history

## Useful Tips

### 1. From Keyword Selection to Prompt Generation
1. Select multiple keywords in the Category Selection tab
2. Navigate to the Prompt Generation tab
3. Add or edit keywords as needed
4. Click the Prompt Generation button
5. Copy and use the generated prompts

### 2. Utilizing Favorites
1. After generating frequently used prompts, click "Add to Favorites"
2. Next time, easily access them from the Favorites Management tab
3. Use the "Copy" button to copy to clipboard

### 3. Regenerating from History
1. Check past prompts in the History tab
2. Use "Reuse" to regenerate with the same conditions
3. Modify keywords slightly to create new variations

## Troubleshooting

### If the model cannot be loaded
* Check if the model specified in `model_name` exists on Hugging Face Hub
* Depending on the model, downloading may take time on first startup or after model change
* Check your internet connection

### If prompts are not being generated
* Ensure keywords are entered in the keyword input field
* When using AI model:
  - Verify a text generation model is specified in `model_name`
  - Verify appropriate categories are specified in `auto_generate_areas`
* Ensure templates are correctly selected

### If browser does not open
* Manually copy and paste the URL displayed in the terminal (http://localhost:8501) into your browser
* Check if port 8501 is not being used by another application

### If history or favorites are not displayed
* Check if `prompt_history.json` or `categories.json` are corrupted
* If files don't exist, the application will create them automatically

### If memory errors occur
* Try using a lighter AI model
* Turn off AI model usage and generate using templates
* Close other applications to free up memory

## Notes

* **Regarding NSFW Categories**: Use only for research purposes. Comply with terms of service and laws.
* **When Using AI Models**: Consumes significant memory. Use lightweight models if memory is insufficient.
* **Data Storage**: History and favorites are saved locally. Regular backups are recommended.
* **Using Virtual Environment**: Always run within a virtual environment to avoid polluting the system environment.

## Shortcuts and Hints

* **Ctrl+C (Cmd+C)**: Copy
* **Browser Refresh**: If the app has issues, reload the browser (F5)
* **Multiple Windows**: Can be opened in multiple browser tabs simultaneously (shares the same session state)
* **Mobile Support**: Accessible from smartphone and tablet browsers

## System Requirements

- Python 3.8 or higher
- Memory: Minimum 4GB (8GB or more recommended when using AI models)
- Browser: Chrome, Firefox, Safari, Edge, etc.

## Disclaimer

When using the NSFW categories, please comply with the terms of service and laws. Some models may cause out-of-memory errors. If this happens, try using a lightweight model.

## Developer
yf591

## License

This application is released under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** License.

This license protects the author's rights and encourages the sharing of knowledge and innovation. If you are interested in commercial use, please contact the developer for permission.
