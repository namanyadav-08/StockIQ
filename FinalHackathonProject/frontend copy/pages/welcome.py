import streamlit as st
from utils.session import set_page
import json
from streamlit_lottie import st_lottie

def load_lottie_animation():
    """Load a Lottie animation for the welcome page"""
    # Simple stock market animation JSON
    animation_data = {
        "v": "5.7.4",
        "fr": 30,
        "ip": 0,
        "op": 60,
        "w": 400,
        "h": 400,
        "nm": "Stock Market Animation",
        "ddd": 0,
        "assets": [],
        "layers": [
            {
                "ddd": 0,
                "ind": 1,
                "ty": 4,
                "nm": "Chart Line",
                "sr": 1,
                "ks": {
                    "o": {"a": 0, "k": 100},
                    "r": {"a": 0, "k": 0},
                    "p": {"a": 0, "k": [200, 200, 0]},
                    "a": {"a": 0, "k": [0, 0, 0]},
                    "s": {"a": 0, "k": [100, 100, 100]}
                },
                "ao": 0,
                "shapes": [
                    {
                        "ty": "gr",
                        "it": [
                            {
                                "ind": 0,
                                "ty": "sh",
                                "ix": 1,
                                "ks": {
                                    "a": 1,
                                    "k": [
                                        {
                                            "i": {"x": 0.833, "y": 0.833},
                                            "o": {"x": 0.167, "y": 0.167},
                                            "t": 0,
                                            "s": [{
                                                "i": [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                                                "o": [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                                                "v": [[-150, 0], [-90, 30], [-30, -20], [30, 40], [90, -10], [150, 20]],
                                                "c": False
                                            }]
                                        },
                                        {
                                            "i": {"x": 0.833, "y": 0.833},
                                            "o": {"x": 0.167, "y": 0.167},
                                            "t": 30,
                                            "s": [{
                                                "i": [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                                                "o": [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                                                "v": [[-150, 0], [-90, -20], [-30, 30], [30, -10], [90, 40], [150, -30]],
                                                "c": False
                                            }]
                                        },
                                        {
                                            "i": {"x": 0.833, "y": 0.833},
                                            "o": {"x": 0.167, "y": 0.167},
                                            "t": 60,
                                            "s": [{
                                                "i": [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                                                "o": [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                                                "v": [[-150, 0], [-90, 30], [-30, -20], [30, 40], [90, -10], [150, 20]],
                                                "c": False
                                            }]
                                        }
                                    ]
                                }
                            },
                            {
                                "ty": "st",
                                "c": {"a": 0, "k": [0.118, 0.235, 0.447, 1]},
                                "o": {"a": 0, "k": 100},
                                "w": {"a": 0, "k": 5},
                                "lc": 2,
                                "lj": 2,
                                "bm": 0,
                                "nm": "Stroke 1",
                                "mn": "ADBE Vector Graphic - Stroke",
                                "hd": False
                            },
                            {
                                "ty": "tr",
                                "p": {"a": 0, "k": [0, 0]},
                                "a": {"a": 0, "k": [0, 0]},
                                "s": {"a": 0, "k": [100, 100]},
                                "r": {"a": 0, "k": 0},
                                "o": {"a": 0, "k": 100},
                                "sk": {"a": 0, "k": 0},
                                "sa": {"a": 0, "k": 0},
                                "nm": "Transform"
                            }
                        ],
                        "nm": "Group 1",
                        "np": 2,
                        "cix": 2,
                        "bm": 0,
                        "ix": 1,
                        "mn": "ADBE Vector Group",
                        "hd": False
                    }
                ],
                "ip": 0,
                "op": 60,
                "st": 0,
                "bm": 0
            }
        ]
    }
    return animation_data

def show_welcome():
    """Display the welcome page with a large, centralized heading and tagline, and animation below"""
    # Set website background using CSS
    st.markdown(
        """
        <style>
        body {
            background-image: url('https://static.vecteezy.com/system/resources/thumbnails/019/576/577/small/abstract-white-wavy-ripple-pattern-background-curve-line-texture-for-modern-graphic-design-element-website-banner-and-poster-or-business-card-decoration-vector.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        .stApp {
            background: transparent !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div style='text-align:center; margin-top: 4rem; margin-bottom: 2rem;'>
            <div style='font-size:5.5rem; font-weight:900; color:#2563eb; letter-spacing:-2px; line-height:1.05;'>StockIQ</div>
            <div style='font-size:2.2rem; color:#444; margin-top:1.2rem; font-weight:600;'>Your AI-powered Stock Market Predictor</div>
            <div style='font-size:1.3rem; color:#888; margin-top:0.7rem;'>Modern, Insightful, and Beautifully Simple</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    # Features section
    st.markdown("<h2 style='text-align:center; color:#2563eb; margin-top:3rem;'>Powerful Features</h2>", unsafe_allow_html=True)
    feat_col1, feat_col2, feat_col3 = st.columns(3)
    feature_card_style = (
        "background: #fff; "
        "box-shadow: 0 4px 24px rgba(0,0,0,0.07); "
        "border-radius: 18px; "
        "padding: 2rem 1.2rem 1.5rem 1.2rem; "
        "display: flex; flex-direction: column; align-items: center; "
        "height: 260px; "
        "margin-bottom: 1.5rem;"
    )
    icon_style = "font-size:2.5rem; margin-bottom:1rem; color:#2563eb;"
    title_style = "font-weight:700; font-size:1.2rem; color:#222; margin-bottom:0.5rem; text-align:center;"
    desc_style = "color:#555; text-align:center; font-size:1rem;"
    with feat_col1:
        st.markdown(f"""
            <div style='{feature_card_style}'>
                <div style='{icon_style}'>📊</div>
                <div style='{title_style}'>Advanced Analytics</div>
                <div style='{desc_style}'>Powerful stock analysis with technical indicators and AI-driven insights.</div>
            </div>
        """, unsafe_allow_html=True)
    with feat_col2:
        st.markdown(f"""
            <div style='{feature_card_style}'>
                <div style='{icon_style}'>🤖</div>
                <div style='{title_style}'>AI Assistant</div>
                <div style='{desc_style}'>Get personalized stock recommendations and answers to your questions.</div>
            </div>
        """, unsafe_allow_html=True)
    with feat_col3:
        st.markdown(f"""
            <div style='{feature_card_style}'>
                <div style='{icon_style}'>📱</div>
                <div style='{title_style}'>Modern Interface</div>
                <div style='{desc_style}'>Beautiful, responsive design with real-time updates and notifications.</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Call-to-action button with proper Streamlit functionality
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Get Started", key="welcome_btn", use_container_width=True):
            set_page("auth")