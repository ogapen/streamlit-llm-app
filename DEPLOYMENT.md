# 🚀 Streamlit Community Cloud デプロイガイド

このガイドでは、AI Expert ConsultingアプリをStreamlit Community Cloudにデプロイする手順を説明します。

## 📋 前提条件

- [x] GitHubアカウント
- [x] OpenAI APIキー
- [x] Streamlit Community Cloudアカウント

## 🔧 デプロイ手順

### 1. GitHubリポジトリの準備

```bash
# 変更をコミットしてプッシュ
git add .
git commit -m "Add Streamlit Community Cloud deployment configuration"
git push origin main
```

### 2. Streamlit Community Cloudでのアプリ作成

1. **Streamlit Community Cloud** (https://share.streamlit.io/) にアクセス
2. **New app** をクリック
3. リポジトリ情報を入力：
   - **Repository**: `ogapen/streamlit-llm-app`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL** (optional): カスタムURL

### 3. シークレット（環境変数）の設定

1. アプリ作成後、**Settings** → **Secrets** に移動
2. 以下の環境変数を設定：

```toml
OPENAI_API_KEY = "sk-proj-your-actual-api-key-here"
```

### 4. デプロイの確認

- アプリが自動的にビルドされ、デプロイされます
- デプロイ完了後、提供されたURLでアプリにアクセス可能

## 🔗 リポジトリ情報

- **GitHub Repository**: https://github.com/ogapen/streamlit-llm-app
- **Main Branch**: main
- **Entry Point**: app.py

## 📁 デプロイに含まれるファイル

```
streamlit-llm-app/
├── .streamlit/
│   ├── config.toml              # Streamlit設定
│   └── secrets.toml.example     # シークレット設定例
├── app.py                       # メインアプリケーション
├── requirements.txt             # Python依存関係
├── README.md                    # プロジェクト説明
├── DEPLOYMENT.md               # このファイル
└── .gitignore                  # Git除外設定
```

## ⚙️ 設定ファイル詳細

### config.toml
- アプリのテーマとサーバー設定
- 自動的に適用される

### secrets.toml
- 環境変数（APIキーなど）
- Streamlit Community CloudのWebインターフェースで設定

## 🔒 セキュリティ注意事項

- `.env` ファイルは `.gitignore` に含まれており、リポジトリにプッシュされません
- OpenAI APIキーは必ずStreamlit Community Cloudのsecrets機能で設定してください
- 実際のAPIキーをコードに直接書き込まないでください

## 🐛 トラブルシューティング

### よくある問題と解決方法

1. **アプリが起動しない**
   - requirements.txtの依存関係を確認
   - Python バージョンの互換性を確認

2. **OpenAI API エラー**
   - Streamlit Cloud の Secrets でAPIキーが正しく設定されているか確認
   - APIキーの有効性と残高を確認

3. **モジュールが見つからない**
   - requirements.txt に必要なパッケージが全て含まれているか確認

## 📞 サポート

問題が発生した場合は、以下を確認してください：
- Streamlit Community Cloud のログ
- GitHub リポジトリの Issues
- OpenAI API の使用状況

---

© 2025 AI Expert Consulting | Powered by Streamlit Community Cloud
