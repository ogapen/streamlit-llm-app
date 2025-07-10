#!/usr/bin/env python3
"""
AI Expert Consulting アプリケーションのテストスクリプト
基本的な機能とインポートをテストします
"""

import os
import sys

def test_imports():
    """必要なライブラリのインポートテスト"""
    print("🔍 ライブラリのインポートテスト...")
    
    try:
        import streamlit as st
        print("✅ Streamlit: OK")
    except ImportError as e:
        print(f"❌ Streamlit: {e}")
        return False
    
    try:
        from langchain_openai import ChatOpenAI
        print("✅ LangChain OpenAI: OK")
    except ImportError as e:
        print(f"❌ LangChain OpenAI: {e}")
        return False
    
    try:
        from langchain.schema import SystemMessage, HumanMessage
        print("✅ LangChain Schema: OK")
    except ImportError as e:
        print(f"❌ LangChain Schema: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ Python-dotenv: OK")
    except ImportError as e:
        print(f"❌ Python-dotenv: {e}")
        return False
    
    return True

def test_environment():
    """環境設定のテスト"""
    print("\n🔍 環境設定テスト...")
    
    # .envファイルの存在確認
    if os.path.exists('.env'):
        print("✅ .envファイル: 存在します")
        
        # 環境変数の読み込みテスト
        try:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key and api_key.startswith('sk-'):
                print(f"✅ OpenAI API Key: 正常に設定されています ({api_key[:10]}...{api_key[-4:]})")
            else:
                print("⚠️ OpenAI API Key: 設定されていないか無効です")
        except Exception as e:
            print(f"❌ 環境変数読み込みエラー: {e}")
    else:
        print("⚠️ .envファイル: 存在しません（作成してください）")
    
    # .env.exampleファイルの存在確認
    if os.path.exists('.env.example'):
        print("✅ .env.exampleファイル: 存在します")
    else:
        print("❌ .env.exampleファイル: 存在しません")
    
    # .gitignoreファイルの存在確認
    if os.path.exists('.gitignore'):
        print("✅ .gitignoreファイル: 存在します")
    else:
        print("❌ .gitignoreファイル: 存在しません")

def test_app_structure():
    """アプリケーション構造のテスト"""
    print("\n🔍 アプリケーション構造テスト...")
    
    # メインアプリファイルの存在確認
    if os.path.exists('app.py'):
        print("✅ app.py: 存在します")
    else:
        print("❌ app.py: 存在しません")
    
    # requirements.txtの存在確認
    if os.path.exists('requirements.txt'):
        print("✅ requirements.txt: 存在します")
    else:
        print("❌ requirements.txt: 存在しません")
    
    # READMEファイルの存在確認
    if os.path.exists('README.md'):
        print("✅ README.md: 存在します")
    else:
        print("❌ README.md: 存在しません")

def main():
    """メインテスト関数"""
    print("🚀 AI Expert Consulting アプリケーションテスト開始\n")
    
    # 各テストを実行
    import_test_passed = test_imports()
    test_environment()
    test_app_structure()
    
    print("\n" + "="*50)
    
    if import_test_passed:
        print("🎉 全ての必須ライブラリが正常にインストールされています！")
        print("📝 次のステップ:")
        print("   1. .envファイルにOpenAI API キーを設定")
        print("   2. streamlit run app.py でアプリを起動")
        print("   3. ブラウザで http://localhost:8501 を開く")
    else:
        print("❌ インポートエラーがあります。requirements.txtから依存関係を再インストールしてください。")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main()
