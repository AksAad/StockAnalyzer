import streamlit as st

def apply_custom_theme():
    """Apply custom theme to the Streamlit app"""
    st.set_page_config(
        page_title="Stock Market Simulator",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        /* Main theme colors */
        :root {
            --primary-color: #1E3A8A;  /* Deep Navy Blue */
            --secondary-color: #1E40AF;  /* Royal Blue */
            --accent-color: #059669;  /* Emerald Green */
            --danger-color: #DC2626;  /* Red */
            --warning-color: #D97706;  /* Amber */
            --background-color: #0F172A;  /* Dark Blue */
            --card-background: #1E293B;  /* Slate */
            --text-color: #F8FAFC;  /* Light Gray */
            --text-secondary: #94A3B8;  /* Gray */
            --border-color: #334155;  /* Slate */
        }
        
        /* Main container */
        .main {
            background-color: var(--background-color);
            color: var(--text-color);
        }
        
        /* Sidebar */
        .css-1d391kg {
            background-color: var(--card-background);
            border-right: 1px solid var(--border-color);
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-color);
            font-family: 'Inter', 'Roboto', sans-serif;
            font-weight: 600;
            letter-spacing: -0.025em;
        }
        
        /* Buttons */
        .stButton>button {
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            transition: all 0.3s ease;
            font-family: 'Inter', sans-serif;
        }
        
        .stButton>button:hover {
            background-color: var(--secondary-color);
            transform: translateY(-1px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        
        /* Input fields */
        .stTextInput>div>div>input {
            background-color: var(--card-background);
            color: var(--text-color);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 0.75rem;
            font-family: 'Inter', sans-serif;
        }
        
        .stTextInput>div>div>input:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 2px rgba(30, 58, 138, 0.2);
        }
        
        /* Tables */
        .stTable {
            background-color: var(--card-background);
            border-radius: 8px;
            padding: 1rem;
            border: 1px solid var(--border-color);
        }
        
        .stTable th {
            background-color: var(--primary-color);
            color: white;
            font-weight: 500;
            padding: 0.75rem;
        }
        
        .stTable td {
            color: var(--text-color);
            padding: 0.75rem;
            border-bottom: 1px solid var(--border-color);
        }
        
        /* Metrics */
        .stMetric {
            background-color: var(--card-background);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 0.5rem;
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        .stMetric label {
            color: var(--text-secondary);
            font-size: 0.875rem;
            font-weight: 500;
        }
        
        .stMetric div {
            color: var(--text-color);
            font-size: 1.5rem;
            font-weight: 600;
        }
        
        /* Charts */
        .js-plotly-plot {
            background-color: var(--card-background) !important;
            border-radius: 8px !important;
            border: 1px solid var(--border-color) !important;
        }
        
        /* Cards */
        .stCard {
            background-color: var(--card-background);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 0.75rem 0;
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background-color: var(--card-background);
            border-radius: 8px;
            padding: 0.5rem;
            border: 1px solid var(--border-color);
        }
        
        .stTabs [data-baseweb="tab"] {
            color: var(--text-secondary);
            font-weight: 500;
            padding: 0.75rem 1.5rem;
            border-radius: 6px;
            transition: all 0.3s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: var(--primary-color);
            color: white;
        }
        
        /* Loading spinner */
        .stSpinner {
            color: var(--primary-color);
        }
        
        /* Success/Error messages */
        .stSuccess {
            background-color: var(--accent-color);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid rgba(5, 150, 105, 0.2);
            box-shadow: 0 4px 6px -1px rgba(5, 150, 105, 0.1);
        }
        
        .stError {
            background-color: var(--danger-color);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid rgba(220, 38, 38, 0.2);
            box-shadow: 0 4px 6px -1px rgba(220, 38, 38, 0.1);
        }
        
        /* Number input */
        .stNumberInput>div>div>input {
            background-color: var(--card-background);
            color: var(--text-color);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 0.75rem;
        }
        
        /* Selectbox */
        .stSelectbox>div>div>select {
            background-color: var(--card-background);
            color: var(--text-color);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 0.75rem;
        }
        
        /* Hover effects */
        .stCard:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px -4px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .stCard, .stMetric, .stTable {
            animation: fadeIn 0.3s ease-out;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Add custom fonts
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True) 