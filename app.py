from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# ページ設定
st.set_page_config(
    page_title="AI専門家コンサルティングアプリ",
    page_icon="🤖",
    layout="wide"
)

# カスタムCSS
st.markdown("""
<style>
/* メインコンテナ */
.main-container {
    background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    color: white;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

/* タイトルスタイル */
.main-title {
    font-size: 3rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 1rem;
    background: linear-gradient(45deg, #f39c12, #e74c3c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

/* 説明カード */
.info-card {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: white;
}

/* 専門家カード */
.expert-card {
    background: linear-gradient(145deg, #ffffff, #f8f9fa);
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
    color: #2c3e50;
    border: 2px solid transparent;
}

.expert-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    border: 2px solid #3498db;
}

/* ボタンスタイル */
.stButton > button {
    background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 0.75rem 2rem;
    font-size: 1.1rem;
    font-weight: bold;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

/* ラジオボタンスタイル */
.stRadio > div {
    background: linear-gradient(135deg, #ffffff, #f8f9fa);
    border-radius: 10px;
    padding: 1rem;
    margin: 0.5rem 0;
    border: 1px solid #e9ecef;
    color: #2c3e50;
}

/* テキストエリアスタイル */
.stTextArea > div > div > textarea {
    border-radius: 10px;
    border: 2px solid #e0e0e0;
    transition: border-color 0.3s ease;
}

.stTextArea > div > div > textarea:focus {
    border-color: #4ECDC4;
    box-shadow: 0 0 10px rgba(78, 205, 196, 0.3);
}

/* アドバイス表示エリア */
.advice-container {
    background: linear-gradient(135deg, #2c3e50, #34495e);
    border-radius: 15px;
    padding: 2rem;
    margin: 1rem 0;
    color: white;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

/* サイドバースタイル */
.sidebar-content {
    background: linear-gradient(135deg, #ffffff, #f8f9fa);
    border-radius: 10px;
    padding: 1rem;
    margin: 0.5rem 0;
    color: #2c3e50;
    border: 1px solid #e9ecef;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

/* 専門分野選択見出し */
.expert-selection-title {
    color: #000000 !important;
    font-weight: bold;
}

/* 質問相談見出し */
.question-title {
    color: #2c3e50 !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# メインヘッダー
st.markdown("""
<div class="main-container">
    <h1 class="main-title">🤖 AI Expert Consulting</h1>
    <div class="info-card">
        <h3>✨ アプリの概要</h3>
        <p>異なる分野の専門家として振る舞うAIコンサルタントサービスです。最新のAI技術を活用して、あなたの悩みや疑問に専門的なアドバイスを提供します。</p>
    </div>
    <div class="info-card">
        <h3>🚀 操作方法</h3>
        <ol>
            <li><strong>専門分野を選択</strong> - 下のカードから相談したい分野を選んでください</li>
            <li><strong>質問を入力</strong> - 具体的な質問や相談内容を入力してください</li>
            <li><strong>回答を取得</strong> - AIエキスパートからの専門的なアドバイスを受け取ってください</li>
        </ol>
    </div>
</div>
""", unsafe_allow_html=True)

def get_expert_advice(input_text, expert_type):
    """
    入力テキストと専門家タイプを受け取り、LLMからの回答を返す関数
    
    Args:
        input_text (str): ユーザーからの質問や相談内容
        expert_type (str): 選択された専門家のタイプ
    
    Returns:
        str: LLMからの回答
    """
    # 専門家タイプに応じてシステムメッセージを設定
    system_messages = {
        "ファッションスタイリスト": "あなたは10年以上の経験を持つ優秀なファッションスタイリストです。流行に敏感で、個人の体型や好みに合わせたコーディネートの提案が得意です。",
        "栄養士・管理栄養士": "あなたは国家資格を持つ管理栄養士です。健康的な食事プランの作成、栄養バランスの改善、ダイエットサポートなどの専門知識を持っています。",
        "ITコンサルタント": "あなたは豊富な経験を持つITコンサルタントです。システム設計、プログラミング、デジタル化戦略など、IT分野全般に精通しています。",
        "心理カウンセラー": "あなたは臨床心理士の資格を持つ心理カウンセラーです。メンタルヘルス、人間関係の悩み、ストレス管理などの専門知識を持ち、共感的で親身なアドバイスを提供します。",
        "投資・資産運用アドバイザー": "あなたは金融のプロフェッショナルとして、投資戦略、資産運用、リスク管理について深い知識を持っています。個人の状況に応じた適切なアドバイスを提供します。",
        "塗装専門家": "あなたは建築塗装分野で20年以上の経験を持つ専門家です。外壁塗装、内装塗装、防水工事など、塗装に関するあらゆる知識と技術を持ち、最適な塗料選択や施工方法を提案します。",
        "労働安全衛生法専門家": "あなたは労働安全衛生法に精通した専門家です。職場の安全管理、法令遵守、リスクアセスメント、安全教育などの専門知識を持ち、働く人の安全と健康を守るアドバイスを提供します。",
        "建築設計士": "あなたは一級建築士の資格を持つ建築設計の専門家です。住宅から商業建築まで幅広い設計経験があり、構造計算、法規チェック、施工管理などの専門知識を提供します。",
        "マーケティング戦略家": "あなたはデジタルマーケティングの専門家です。ブランディング、市場分析、SNSマーケティング、広告戦略など、効果的なマーケティング手法を熟知し、ビジネス成長をサポートします。",
        "法務・契約書専門家": "あなたは企業法務に精通した法律の専門家です。契約書の作成・チェック、法的リスクの評価、コンプライアンス対応などの専門知識を持ち、法的トラブルを未然に防ぐアドバイスを提供します。",
        "人事・採用コンサルタント": "あなたは人事・採用分野の専門家です。採用戦略の立案、面接技法、人事制度設計、組織開発など、人材マネジメントの幅広い知識を持ち、組織力向上をサポートします。",
        "環境・エネルギー専門家": "あなたは環境・エネルギー分野の専門家です。省エネルギー対策、再生可能エネルギー導入、環境アセスメント、カーボンニュートラルなど、持続可能な社会の実現に向けたアドバイスを提供します。"
    }
    
    # LLMインスタンスを作成
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
    
    # メッセージを構築
    messages = [
        SystemMessage(content=system_messages[expert_type]),
        HumanMessage(content=input_text)
    ]
    
    # LLMから回答を取得
    try:
        result = llm.invoke(messages)
        return result.content
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

# メインのアプリケーション部分
col1, col2 = st.columns([2, 3])

with col1:
    st.markdown('<div class="expert-selection-title"><h3>🎯 専門分野を選択</h3></div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # 専門家の詳細情報
    expert_info = {
        "ファッションスタイリスト": {
            "icon": "👗",
            "description": "トレンド感あふれるスタイリング提案",
            "specialty": "コーディネート・体型カバー・TPO"
        },
        "栄養士・管理栄養士": {
            "icon": "🥗",
            "description": "科学的根拠に基づく栄養指導",
            "specialty": "食事プラン・栄養バランス・健康管理"
        },
        "ITコンサルタント": {
            "icon": "💻",
            "description": "最新技術による課題解決",
            "specialty": "システム設計・プログラミング・DX"
        },
        "心理カウンセラー": {
            "icon": "💭",
            "description": "心に寄り添うカウンセリング",
            "specialty": "メンタルヘルス・人間関係・ストレス"
        },
        "投資・資産運用アドバイザー": {
            "icon": "📈",
            "description": "賢い資産形成をサポート",
            "specialty": "投資戦略・リスク管理・資産運用"
        },
        "塗装専門家": {
            "icon": "🎨",
            "description": "建築塗装のプロフェッショナル",
            "specialty": "外壁塗装・内装塗装・防水工事"
        },
        "労働安全衛生法専門家": {
            "icon": "🛡️",
            "description": "職場の安全と健康を守る専門家",
            "specialty": "安全管理・法令遵守・リスクアセスメント"
        },
        "建築設計士": {
            "icon": "🏗️",
            "description": "建築設計・施工管理のエキスパート",
            "specialty": "設計・構造計算・施工管理"
        },
        "マーケティング戦略家": {
            "icon": "📊",
            "description": "効果的なマーケティング戦略を提案",
            "specialty": "デジタルマーケティング・ブランディング・市場分析"
        },
        "法務・契約書専門家": {
            "icon": "⚖️",
            "description": "法的リスクを回避する契約書作成",
            "specialty": "契約書作成・法的相談・コンプライアンス"
        },
        "人事・採用コンサルタント": {
            "icon": "👥",
            "description": "人材採用と組織運営のプロ",
            "specialty": "採用戦略・人事制度・組織開発"
        },
        "環境・エネルギー専門家": {
            "icon": "🌱",
            "description": "持続可能な環境ソリューション",
            "specialty": "省エネルギー・再生可能エネルギー・環境対策"
        }
    }
    
    # ラジオボタンで専門家の種類を選択
    expert_choice = st.radio(
        "専門分野を選択：",
        list(expert_info.keys()),
        format_func=lambda x: f"{expert_info[x]['icon']} {x}"
    )
    
    # 選択された専門家の詳細表示
    if expert_choice:
        info = expert_info[expert_choice]
        st.markdown(f"""
        <div class="expert-card">
            <h4>{info['icon']} {expert_choice}</h4>
            <p><strong>特徴:</strong> {info['description']}</p>
            <p><strong>専門領域:</strong> {info['specialty']}</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="question-title"><h3>💬 ご質問・ご相談</h3></div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # テキスト入力エリア
    user_input = st.text_area(
        "質問や相談内容を詳しく入力してください：",
        placeholder="例：\n・30代女性向けのビジネスカジュアルコーディネートを教えて\n・ダイエット中の栄養バランスの取り方は？\n・Pythonでのデータ分析を始めたいのですが...",
        height=200,
        help="具体的な状況や条件を含めて質問いただくと、より的確なアドバイスが得られます"
    )
    
    # 回答取得ボタン
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✨ 専門家に相談する", type="primary", use_container_width=True):
        if user_input.strip():
            with st.spinner(f"{expert_info[expert_choice]['icon']} {expert_choice}が回答を準備中..."):
                # 専門家からのアドバイスを取得
                advice = get_expert_advice(user_input, expert_choice)
                
                st.markdown(f"""
                <div class="advice-container">
                    <h3>{expert_info[expert_choice]['icon']} {expert_choice}からのアドバイス</h3>
                    <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 10px; margin-top: 1rem;">
                        {advice.replace(chr(10), '<br>')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("⚠️ 質問内容を入力してください。")

# サイドバーに追加情報
with st.sidebar:
    st.markdown("""
    <div class="sidebar-content">
        <h2>🌟 サービス特徴</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-content">
        <h4>🎨 ファッションスタイリスト</h4>
        <ul>
            <li>最新トレンドを取り入れたコーディネート</li>
            <li>体型や年代に合わせた提案</li>
            <li>TPOを考慮したスタイリング</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-content">
        <h4>🥗 栄養士・管理栄養士</h4>
        <ul>
            <li>科学的根拠に基づく食事指導</li>
            <li>個人の体質に合わせた栄養プラン</li>
            <li>健康維持・改善のサポート</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-content">
        <h4>💻 ITコンサルタント</h4>
        <ul>
            <li>最新技術トレンドの解説</li>
            <li>システム設計・開発支援</li>
            <li>デジタル変革の戦略提案</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-content">
        <h4>💭 心理カウンセラー</h4>
        <ul>
            <li>共感的で温かいカウンセリング</li>
            <li>ストレス管理法の提案</li>
            <li>人間関係改善のアドバイス</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-content">
        <h4>📈 投資・資産運用アドバイザー</h4>
        <ul>
            <li>リスク許容度に応じた投資戦略</li>
            <li>長期的な資産形成プラン</li>
            <li>市場動向の分析と解説</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-content">
        <h4>🎨 塗装専門家</h4>
        <ul>
            <li>外壁・内装塗装のアドバイス</li>
            <li>塗料選択と施工方法</li>
            <li>防水・耐久性の向上</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-content">
        <h4>🛡️ 労働安全衛生法専門家</h4>
        <ul>
            <li>職場安全管理の指導</li>
            <li>法令遵守とリスク評価</li>
            <li>安全教育プログラム</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-content">
        <h4>🏗️ 建築設計士</h4>
        <ul>
            <li>建築設計・構造計算</li>
            <li>法規チェック・申請業務</li>
            <li>施工管理・品質保証</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-content">
        <h4>📊 マーケティング戦略家</h4>
        <ul>
            <li>デジタルマーケティング</li>
            <li>ブランディング・市場分析</li>
            <li>SNS・広告戦略</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-content">
        <h4>⚖️ 法務・契約書専門家</h4>
        <ul>
            <li>契約書作成・リーガルチェック</li>
            <li>法的リスクの評価</li>
            <li>コンプライアンス対応</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-content">
        <h4>👥 人事・採用コンサルタント</h4>
        <ul>
            <li>採用戦略・面接技法</li>
            <li>人事制度設計</li>
            <li>組織開発・人材育成</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-content">
        <h4>🌱 環境・エネルギー専門家</h4>
        <ul>
            <li>省エネルギー対策</li>
            <li>再生可能エネルギー導入</li>
            <li>カーボンニュートラル</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #e74c3c, #c0392b); 
                padding: 1rem; border-radius: 10px; text-align: center;
                color: white; border: 1px solid rgba(255, 255, 255, 0.2);">
        <h4>⚠️ 重要な注意事項</h4>
        <p>このアプリはAIによる一般的なアドバイスを提供するものです。<br>
        重要な決定については、必ず専門機関や資格を持つ専門家にご相談ください。</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #2c3e50;">
        <small>© 2025 AI Expert Consulting<br>
        Powered by OpenAI & Streamlit</small>
    </div>
    """, unsafe_allow_html=True)

# フッター
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; 
            background: linear-gradient(135deg, #ecf0f1, #bdc3c7); 
            border-radius: 15px; margin-top: 3rem;
            color: #2c3e50;">
    <h3>🚀 AI Expert Consultingをお試しいただき、ありがとうございます！</h3>
    <p>より良いサービス提供のため、フィードバックをお待ちしております。</p>
    <div style="margin-top: 1rem;">
        <span style="background: #e74c3c; color: white; padding: 0.5rem 1rem; 
                     border-radius: 20px; margin: 0 0.5rem;">AI Technology</span>
        <span style="background: #27ae60; color: white; padding: 0.5rem 1rem; 
                     border-radius: 20px; margin: 0 0.5rem;">Expert Knowledge</span>
        <span style="background: #3498db; color: white; padding: 0.5rem 1rem; 
                     border-radius: 20px; margin: 0 0.5rem;">User Friendly</span>
    </div>
</div>
""", unsafe_allow_html=True)