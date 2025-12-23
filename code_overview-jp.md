# PromptCrafter2 各ファイルのコードの概要

## ファイル構成

アプリケーションは明確な関心の分離を持つモジュラー構造に従っています。

### コアアプリケーションファイル

## `app.py`
* **概要**
  - Streamlitアプリケーションのメインエントリーポイント
  - ページ設定とカスタムCSSを設定
  - メインアプリケーションフローとタブナビゲーションを管理
* **コードの解説**
  - `app/ui/`からUIモジュールをインポート
  - Streamlitページ設定を構成（タイトル、アイコン、レイアウト）
  - スタイリング用のカスタムCSSを定義
  - 5つのメインタブを作成：プロンプト生成、検索、カテゴリ選択、お気に入り管理、履歴
  - 各タブに適切なUIコンポーネントをレンダリング
  - バージョンとライセンス情報を含むフッターを表示

## `app/config.py`
* **概要**
  - アプリケーション設定と構成を管理
  - 設定ファイル（app_settings.json、categories.json）の読み込みと保存を処理
* **コードの解説**
  - **`DEFAULT_APP_SETTINGS`**: デフォルトアプリケーション設定を定義：
    - 異なるスタイルのプロンプトテンプレート（realistic、2D、2.5D、NSFWバリアント）
    - モデル設定（モデル名、使用トグル）
    - AI生成設定（モード、自動生成エリア）
    - LoRAモデルリスト
    - 選択されたテンプレートキー
  - **`APP_SETTINGS`**: 実行時設定を格納するグローバル変数
  - **`CATEGORIES`**: カテゴリデータを格納するグローバル変数
  - **`load_settings(file_path=None)`**: JSONファイルから設定を読み込むか、デフォルトを作成
  - **`save_settings(file_path=None)`**: 現在の設定をJSONファイルに保存
  - **`load_categories(file_path=None)`**: JSONファイルからカテゴリを読み込むか、デフォルトを作成
  - **`save_categories(file_path=None)`**: 現在のカテゴリをJSONファイルに保存
  - **`add_prompts_from_csv(file_path)`**: CSVファイルからプロンプトをPromptsカテゴリにインポート

## `app/prompt_generator.py`
* **概要**
  - AIモデルまたはテンプレートを使用したプロンプト生成ロジックを実装
  - AI基盤の生成にHugging Face transformersライブラリを使用
* **コードの解説**
  - **グローバル変数 `generator`**: 読み込まれたAIモデル（パイプライン）を格納
  - **`generate_prompt(keyword, lora_name, mode="both")`**: 
    - プロンプト生成のメイン関数
    - キーワード、LoRAモデル名、生成モードを受け取る
    - モードに基づいてPositiveとNegativeプロンプトを返す
    - `_generate_model_prompt`または`_generate_template_prompt`を呼び出す
  - **`_generate_model_prompt(keyword, prompt_type)`**: 
    - AIモデルを使用してプロンプトを生成
    - モデルの読み込みに失敗した場合はエラーメッセージを返す
  - **`_generate_template_prompt(keyword, prompt_type)`**: 
    - 設定されたテンプレートを使用してプロンプトを生成
    - {keyword}プレースホルダーをユーザー入力で置換
    - 指定された場合はLoRA構文を追加

## `app/favorites_manager.py`
* **概要**
  - お気に入りプロンプトとキーワードを管理
  - カテゴリ構造からお気に入りの追加と削除を処理
* **コードの解説**
  - **`add_to_favorites(prompt, prompt_type, key)`**: 
    - PositiveまたはNegativeプロンプトをお気に入りに追加
    - Favorites構造が存在しない場合は作成
    - 追加後にカテゴリを保存
  - **`add_keyword_to_favorites(keywords, key)`**: 
    - キーワードの組み合わせをお気に入りに追加
    - FavoritesのKeywordsサブカテゴリに保存
  - **`remove_from_favorites(key, prompt_type)`**: 
    - お気に入りからアイテムを削除（Positive、Negative、またはKeywords）
    - 削除後にカテゴリを保存

## `app/history_manager.py`
* **概要**
  - プロンプト生成履歴を管理
  - 履歴エントリの保存、読み込み、削除を処理
* **コードの解説**
  - **`HISTORY_FILE`**: 履歴ファイルパス（prompt_history.json）を定義する定数
  - **`MAX_HISTORY`**: 最大履歴エントリ数（100）
  - **`add_to_history(keywords, positive_prompt, negative_prompt, lora_name)`**: 
    - タイムスタンプ付きの新しい履歴エントリを追加
    - 最も古いエントリを削除して最大履歴サイズを維持
    - 履歴をJSONファイルに保存
  - **`load_history()`**: 
    - JSONファイルから履歴を読み込む
    - ファイルが存在しない場合は空のリストを返す
  - **`delete_history_item(index)`**: 
    - インデックスで特定の履歴エントリを削除
    - 更新された履歴を保存
  - **`clear_history()`**: 
    - すべての履歴エントリを削除
    - 履歴ファイルを削除

### UIモジュールファイル (app/ui/)

## `app/ui/__init__.py`
* **概要**
  - UIモジュールのパッケージ初期化ファイル
  - すべてのUIレンダリング関数をエクスポート
* **コードの解説**
  - すべてのUIモジュールから関数をインポートしてエクスポート
  - UIコンポーネントへの一元的なアクセスを提供

## `app/ui/session.py`
* **概要**
  - Streamlitセッション状態を初期化して管理
  - すべてのセッション変数のデフォルト値を設定
* **コードの解説**
  - **`initialize_session_state()`**: 
    - まだ設定されていない場合、セッション状態変数を初期化
    - 以下のデフォルト値を設定：
      - プロンプト（positive_prompt、negative_prompt）
      - キーワード（keywords、keywords_input）
      - 選択されたLoRA（selected_lora）
      - カテゴリ（categories）
      - 履歴（prompt_history）
      - フラグ（clear_keywords_flag、clear_positive_flag、clear_negative_flag）

## `app/ui/sidebar.py`
* **概要**
  - アプリケーション設定を含むサイドバーをレンダリング
  - LoRA選択とテンプレート設定を処理
* **コードの解説**
  - **`render_sidebar()`**: 
    - st.sidebarでサイドバーUIを作成
    - LoRA選択ドロップダウン
    - PositiveとNegativeプロンプトのテンプレート選択
    - AIモデル設定（トグル、モデル名、生成モード）
    - 変更時に設定をconfigに保存

## `app/ui/main_content.py`
* **概要**
  - メインプロンプト生成インターフェースをレンダリング
  - キーワード入力、プロンプト生成、お気に入りを処理
* **コードの解説**
  - **`generate_prompts(mode="both")`**: 
    - キーワード入力を検証
    - prompt_generator.generate_prompt()を呼び出す
    - 生成されたプロンプトでセッション状態を更新
    - 履歴に追加
  - **`save_to_favorites(prompt_type, key)`**: 
    - PositiveまたはNegativeプロンプトをお気に入りに保存
    - 入力を検証してカテゴリを更新
  - **`save_keywords_to_favorites(key)`**: 
    - キーワードの組み合わせをお気に入りに保存
    - カテゴリとセッション状態を更新
  - **`render_main_content()`**: 
    - キーワード入力エリアをレンダリング
    - 生成ボタン（両方、Positiveのみ、Negativeのみ、お気に入りに追加、クリア）
    - アクションボタン付きでPositiveとNegativeプロンプトを表示
    - 保存/キャンセルオプション付きお気に入り追加フォームを処理

## `app/ui/search.py`
* **概要**
  - キーワードとプロンプトの検索機能を実装
  - すべてのカテゴリ、サブカテゴリ、アイテムを検索
* **コードの解説**
  - **`search_prompts(query)`**: 
    - カテゴリ全体で大文字小文字を区別しない検索を実行
    - カテゴリコンテキスト付きの一致するアイテムのリストを返す
  - **`render_search()`**: 
    - 検索入力フィールドとボタンをレンダリング
    - チェックボックス付きで検索結果を表示
    - 選択されたアイテムをキーワード入力に追加
    - 日本語と英語の検索をサポート

## `app/ui/category.py`
* **概要**
  - カテゴリ選択インターフェースをレンダリング
  - カテゴリをメイングループと特殊グループに整理
* **コードの解説**
  - **`add_keyword_to_input(keyword, display_name=None)`**: 
    - 選択されたキーワードをセッション状態に追加
    - ユーザーフィードバック用の表示情報を保存
  - **`render_category_selection()`**: 
    - カテゴリを2つのグループに分割（メインと特殊）
    - 各カテゴリのタブを作成
    - 展開可能なセクションでサブカテゴリを表示
    - Favoritesカテゴリの特別処理（Keywordsのみを表示）
    - 選択用のキーワードボタンをレンダリング

## `app/ui/favorites.py`
* **概要**
  - お気に入りの表示とアクションを管理
  - Positive、Negative、Keywordsのお気に入りを表示
* **コードの解説**
  - **`render_favorites_manager()`**: 
    - Positive、Negative、Keywordsのお気に入りタブを作成
    - 各お気に入りをエクスパンダーで表示
    - 無効化されたテキストエリアにお気に入りの内容を表示
    - 各お気に入りにコピーと削除ボタンを提供
    - 削除後にカテゴリとセッション状態を更新

## `app/ui/history.py`
* **概要**
  - プロンプト生成履歴を表示
  - 履歴エントリの再利用、コピー、削除を許可
* **コードの解説**
  - **`render_history()`**: 
    - history_managerから履歴を読み込む
    - 逆時系列順（新しい順）でエントリを表示
    - 各エントリのタイムスタンプ、キーワード、LoRA、両方のプロンプトを表示
    - アクションボタンを提供：
      - 再利用：キーワードとプロンプトをメインインターフェースに復元
      - コピー（Pos/Neg）：プロンプトをクリップボードにコピー
      - 削除：単一の履歴エントリを削除
    - すべてのエントリを削除する「履歴を全削除」ボタン

## 設定ファイル

## `categories.json`
* **概要**
  - キーワードカテゴリの階層構造
  - プロンプトを大分類、中分類、小分類に整理
* **コードの解説**
  - カテゴリには以下が含まれます：People、Nature、Buildings & Structures、Art、Concept、Fantasy、Cyberpunk、NSFWなど
  - 各カテゴリにはサブカテゴリが含まれる
  - 各サブカテゴリにはキーワードペア（日本語：英語）が含まれる
  - Favoritesカテゴリ構造：
    - Positive：保存されたPositiveプロンプト
    - Negative：保存されたNegativeプロンプト
    - Keywords：保存されたキーワードの組み合わせ

## `app_settings.json`
* **概要**
  - 現在のアプリケーション設定を保存
  - UIで設定が変更されると自動的に更新
* **コードの解説**
  - 異なるスタイルのすべてのテンプレート文字列を含む
  - モデル設定とAI生成設定
  - LoRAリストと選択されたテンプレート
  - 存在しない場合はデフォルトで自動作成

## `prompt_history.json`
* **概要**
  - プロンプト生成履歴を保存
  - 自動的に作成および保守
* **コードの解説**
  - 以下を含む履歴オブジェクトの配列：
    - timestamp：生成日時
    - keywords：入力キーワード
    - positive_prompt：生成されたPositiveプロンプト
    - negative_prompt：生成されたNegativeプロンプト
    - lora_name：選択されたLoRAモデル
  - 最新の100エントリに制限

## データフロー

1. **ユーザー入力**：main_content.pyでキーワードを入力
2. **生成**：prompt_generator.pyがAIまたはテンプレートを使用してプロンプトを作成
3. **保存**：
   - プロンプトはセッション状態に保存
   - 履歴はhistory_manager.py経由で保存
   - お気に入りはfavorites_manager.py経由で保存
4. **永続化**：
   - config.pyが設定を管理（app_settings.json）
   - favorites_manager.pyがお気に入りを管理（categories.json）
   - history_manager.pyが履歴を管理（prompt_history.json）
5. **表示**：UIモジュールがセッション状態とファイルからデータをレンダリング

## 主要技術

- **Streamlit**：UI用Webフレームワーク
- **Hugging Face Transformers**：AIモデルの読み込みと推論
- **PyTorch**：AIモデルのバックエンド
- **Pyperclip**：クリップボード操作
- **JSON**：データの永続化

## 設計パターン

- **モジュラーアーキテクチャ**：関心の分離（設定、ロジック、UI）
- **セッション状態管理**：UI反応性のためのStreamlitセッション状態
- **ファイルベースの永続化**：設定とデータ用のJSONファイル
- **コンポーネントベースのUI**：再利用可能なUIモジュール
- **グローバル設定**：一元化された設定管理
