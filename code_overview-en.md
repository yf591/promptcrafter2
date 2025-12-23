# PromptCrafter2 Code Overview

## File Structure

The application follows a modular structure with clear separation of concerns:

### Core Application Files

## `app.py`
* **Overview**
  - Main entry point for the Streamlit application
  - Sets up page configuration and custom CSS
  - Orchestrates the main application flow and tab navigation
* **Code Explanation**
  - Imports UI modules from `app/ui/`
  - Configures Streamlit page settings (title, icon, layout)
  - Defines custom CSS for styling
  - Creates 5 main tabs: Prompt Generation, Search, Category Selection, Favorites Management, and History
  - Renders appropriate UI components for each tab
  - Displays footer with version and license information

## `app/config.py`
* **Overview**
  - Manages application configuration and settings
  - Handles loading and saving of configuration files (app_settings.json, categories.json)
* **Code Explanation**
  - **`DEFAULT_APP_SETTINGS`**: Defines default application settings including:
    - Prompt templates for different styles (realistic, 2D, 2.5D, NSFW variants)
    - Model configuration (model name, usage toggle)
    - AI generation settings (mode, auto-generate areas)
    - LoRA model list
    - Selected template keys
  - **`APP_SETTINGS`**: Global variable storing runtime settings
  - **`CATEGORIES`**: Global variable storing category data
  - **`load_settings(file_path=None)`**: Loads settings from JSON file or creates default
  - **`save_settings(file_path=None)`**: Saves current settings to JSON file
  - **`load_categories(file_path=None)`**: Loads categories from JSON file or creates default
  - **`save_categories(file_path=None)`**: Saves current categories to JSON file
  - **`add_prompts_from_csv(file_path)`**: Imports prompts from CSV file into Prompts category

## `app/prompt_generator.py`
* **Overview**
  - Implements prompt generation logic using AI models or templates
  - Uses Hugging Face transformers library for AI-based generation
* **Code Explanation**
  - **Global variable `generator`**: Stores the loaded AI model (pipeline)
  - **`generate_prompt(keyword, lora_name, mode="both")`**: 
    - Main function for prompt generation
    - Takes keywords, LoRA model name, and generation mode
    - Returns positive and negative prompts based on mode
    - Calls either `_generate_model_prompt` or `_generate_template_prompt`
  - **`_generate_model_prompt(keyword, prompt_type)`**: 
    - Generates prompts using AI model
    - Returns error message if model fails to load
  - **`_generate_template_prompt(keyword, prompt_type)`**: 
    - Generates prompts using configured templates
    - Replaces {keyword} placeholder with user input
    - Adds LoRA syntax if specified

## `app/favorites_manager.py`
* **Overview**
  - Manages favorite prompts and keywords
  - Handles adding and removing favorites from the categories structure
* **Code Explanation**
  - **`add_to_favorites(prompt, prompt_type, key)`**: 
    - Adds Positive or Negative prompts to favorites
    - Creates Favorites structure if it doesn't exist
    - Saves categories after adding
  - **`add_keyword_to_favorites(keywords, key)`**: 
    - Adds keyword combinations to favorites
    - Saves to Keywords subcategory in Favorites
  - **`remove_from_favorites(key, prompt_type)`**: 
    - Removes items from favorites (Positive, Negative, or Keywords)
    - Saves categories after removal

## `app/history_manager.py`
* **Overview**
  - Manages prompt generation history
  - Handles storing, loading, and deleting history entries
* **Code Explanation**
  - **`HISTORY_FILE`**: Constant defining history file path (prompt_history.json)
  - **`MAX_HISTORY`**: Maximum number of history entries (100)
  - **`add_to_history(keywords, positive_prompt, negative_prompt, lora_name)`**: 
    - Adds new history entry with timestamp
    - Maintains maximum history size by removing oldest entries
    - Saves history to JSON file
  - **`load_history()`**: 
    - Loads history from JSON file
    - Returns empty list if file doesn't exist
  - **`delete_history_item(index)`**: 
    - Removes specific history entry by index
    - Saves updated history
  - **`clear_history()`**: 
    - Removes all history entries
    - Deletes history file

### UI Module Files (app/ui/)

## `app/ui/__init__.py`
* **Overview**
  - Package initialization file for UI modules
  - Exports all UI rendering functions for easy import
* **Code Explanation**
  - Imports and exports functions from all UI modules
  - Provides centralized access to UI components

## `app/ui/session.py`
* **Overview**
  - Initializes and manages Streamlit session state
  - Sets default values for all session variables
* **Code Explanation**
  - **`initialize_session_state()`**: 
    - Initializes session state variables if not already set
    - Sets default values for:
      - Prompts (positive_prompt, negative_prompt)
      - Keywords (keywords, keywords_input)
      - Selected LoRA (selected_lora)
      - Categories (categories)
      - History (prompt_history)
      - Flags (clear_keywords_flag, clear_positive_flag, clear_negative_flag)

## `app/ui/sidebar.py`
* **Overview**
  - Renders the sidebar containing application settings
  - Handles LoRA selection and template configuration
* **Code Explanation**
  - **`render_sidebar()`**: 
    - Creates sidebar UI with st.sidebar
    - LoRA selection dropdown
    - Template selection for Positive and Negative prompts
    - AI model settings (toggle, model name, generation mode)
    - Saves settings to config when changed

## `app/ui/main_content.py`
* **Overview**
  - Renders the main prompt generation interface
  - Handles keyword input, prompt generation, and favorites
* **Code Explanation**
  - **`generate_prompts(mode="both")`**: 
    - Validates keyword input
    - Calls prompt_generator.generate_prompt()
    - Updates session state with generated prompts
    - Adds to history
  - **`save_to_favorites(prompt_type, key)`**: 
    - Saves Positive or Negative prompts to favorites
    - Validates input and updates categories
  - **`save_keywords_to_favorites(key)`**: 
    - Saves keyword combinations to favorites
    - Updates categories and session state
  - **`render_main_content()`**: 
    - Renders keyword input area
    - Generation buttons (both, positive only, negative only, add to favorites, clear)
    - Displays Positive and Negative prompts with action buttons
    - Handles favorites addition forms with save/cancel options

## `app/ui/search.py`
* **Overview**
  - Implements search functionality for keywords and prompts
  - Searches across all categories, subcategories, and items
* **Code Explanation**
  - **`search_prompts(query)`**: 
    - Performs case-insensitive search across categories
    - Returns list of matching items with category context
  - **`render_search()`**: 
    - Renders search input field and button
    - Displays search results with checkboxes
    - Adds selected items to keyword input
    - Supports both Japanese and English search

## `app/ui/category.py`
* **Overview**
  - Renders category selection interface
  - Organizes categories into main and special groups
* **Code Explanation**
  - **`add_keyword_to_input(keyword, display_name=None)`**: 
    - Adds selected keyword to session state
    - Stores display information for user feedback
  - **`render_category_selection()`**: 
    - Divides categories into two groups (main and special)
    - Creates tabs for each category
    - Displays subcategories with expandable sections
    - Special handling for Favorites category (shows only Keywords)
    - Renders keyword buttons for selection

## `app/ui/favorites.py`
* **Overview**
  - Manages favorites display and actions
  - Shows Positive, Negative, and Keywords favorites
* **Code Explanation**
  - **`render_favorites_manager()`**: 
    - Creates tabs for Positive, Negative, and Keywords favorites
    - Displays each favorite in an expander
    - Shows favorite content in disabled text area
    - Provides Copy and Delete buttons for each favorite
    - Updates categories and session state after deletion

## `app/ui/history.py`
* **Overview**
  - Displays prompt generation history
  - Allows reusing, copying, and deleting history entries
* **Code Explanation**
  - **`render_history()`**: 
    - Loads history from history_manager
    - Displays entries in reverse chronological order (newest first)
    - Shows timestamp, keywords, LoRA, and both prompts for each entry
    - Provides action buttons:
      - Reuse: Restores keywords and prompts to main interface
      - Copy (Pos/Neg): Copies prompts to clipboard
      - Delete: Removes single history entry
    - Clear All History button to remove all entries

## Configuration Files

## `categories.json`
* **Overview**
  - Hierarchical structure of keyword categories
  - Organizes prompts into major, medium, and minor categories
* **Code Explanation**
  - Categories include: People, Nature, Buildings & Structures, Art, Concept, Fantasy, Cyberpunk, NSFW, etc.
  - Each category contains subcategories
  - Each subcategory contains keyword pairs (Japanese: English)
  - Favorites category structure:
    - Positive: Saved positive prompts
    - Negative: Saved negative prompts
    - Keywords: Saved keyword combinations

## `app_settings.json`
* **Overview**
  - Stores current application settings
  - Automatically updated when settings change in UI
* **Code Explanation**
  - Contains all template strings for different styles
  - Model configuration and AI generation settings
  - LoRA list and selected templates
  - Created automatically with defaults if doesn't exist

## `prompt_history.json`
* **Overview**
  - Stores prompt generation history
  - Automatically created and maintained
* **Code Explanation**
  - Array of history objects with:
    - timestamp: Generation date/time
    - keywords: Input keywords
    - positive_prompt: Generated positive prompt
    - negative_prompt: Generated negative prompt
    - lora_name: Selected LoRA model
  - Limited to 100 most recent entries

## Data Flow

1. **User Input**: Keywords entered in main_content.py
2. **Generation**: prompt_generator.py creates prompts using AI or templates
3. **Storage**: 
   - Prompts stored in session state
   - History saved via history_manager.py
   - Favorites saved via favorites_manager.py
4. **Persistence**: 
   - config.py manages settings (app_settings.json)
   - favorites_manager.py manages favorites (categories.json)
   - history_manager.py manages history (prompt_history.json)
5. **Display**: UI modules render data from session state and files

## Key Technologies

- **Streamlit**: Web framework for UI
- **Hugging Face Transformers**: AI model loading and inference
- **PyTorch**: Backend for AI models
- **Pyperclip**: Clipboard operations
- **JSON**: Data persistence

## Design Patterns

- **Modular Architecture**: Separation of concerns (config, logic, UI)
- **Session State Management**: Streamlit session state for UI reactivity
- **File-based Persistence**: JSON files for settings and data
- **Component-based UI**: Reusable UI modules
- **Global Configuration**: Centralized settings management
