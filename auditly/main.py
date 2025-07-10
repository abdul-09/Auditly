import streamlit as st
import time
from seo_analyzer import SEOAnalyzer
from visualizer import create_score_gauge, create_metrics_chart
from utils import is_valid_url

# Page configuration
st.set_page_config(
    page_title="AUDITLY - Website Analysis Tool",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with animations and responsive design
st.markdown("""
    <style>
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    .stProgress > div > div > div > div {
        background-color: #FF4B4B;
    }

    .stTextInput > div > div > input {
        background-color: #262730;
        color: #FAFAFA;
        width: 100%;
        max-width: 800px;
    }

    .metric-card {
        background-color: #262730;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        animation: slideIn 0.5s ease-out;
        width: 100%;
        box-sizing: border-box;
    }

    .category-title {
        color: #FF4B4B;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
        animation: fadeIn 0.5s ease-out;
        word-wrap: break-word;
    }

    .analysis-section {
        animation: slideIn 0.5s ease-out;
        margin-bottom: 2rem;
        width: 100%;
    }

    .stMarkdown {
        animation: fadeIn 0.5s ease-out;
    }

    .metric-value {
        animation: fadeIn 1s ease-out;
    }

    /* Responsive layout adjustments */
    @media (max-width: 768px) {
        .stColumns {
            flex-direction: column;
        }

        [data-testid="column"] {
            width: 100% !important;
            margin-bottom: 1rem;
        }

        .metric-card {
            margin: 0.5rem 0;
        }

        h1 {
            font-size: 1.8rem !important;
        }

        h2 {
            font-size: 1.5rem !important;
        }

        h3 {
            font-size: 1.2rem !important;
        }
    }

    /* Chart responsiveness */
    [data-testid="stPlotlyChart"] {
        width: 100% !important;
        max-width: 100% !important;
    }

    /* Expandable sections responsiveness */
    .streamlit-expanderHeader {
        word-wrap: break-word;
        white-space: normal !important;
    }

    /* Container padding for better mobile view */
    .element-container {
        padding: 0 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Header with responsive container
st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
st.title("🔍 AUDITLY")
st.markdown("### Comprehensive SEO Analysis Tool")
st.markdown("</div>", unsafe_allow_html=True)

# URL Input with max width
url = st.text_input("Enter website URL", placeholder="https://example.com")

if url:
    if not is_valid_url(url):
        st.error("Please enter a valid URL including http:// or https://")
    else:
        with st.spinner("Analyzing website... This may take a minute"):
            try:
                # Progress indicators
                progress_bar = st.progress(0)
                status_text = st.empty()

                # Initialize analyzer
                analyzer = SEOAnalyzer(url)
                status_text.text("Initializing analysis...")
                progress_bar.progress(20)
                time.sleep(0.3)

                # Perform analysis
                status_text.text("Analyzing website content...")
                progress_bar.progress(40)
                time.sleep(0.3)

                results = analyzer.analyze()

                status_text.text("Processing results...")
                progress_bar.progress(80)
                time.sleep(0.3)

                progress_bar.progress(100)
                status_text.text("Analysis complete!")
                time.sleep(0.3)

                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()

                # Responsive layout
                with st.container():
                    # Main metrics section
                    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)

                    # Use smaller columns on mobile
                    if st.columns([1])[0].checkbox("View detailed view", value=True):
                        col1, col2 = st.columns([2, 1])
                    else:
                        col1, col2 = st.columns([1, 1])

                    with col1:
                        st.markdown("### Overall SEO Score")
                        create_score_gauge(results['overall_score'])
                        time.sleep(0.2)

                        st.markdown("### Performance Metrics")
                        create_metrics_chart(results['metrics'])
                        time.sleep(0.2)

                    with col2:
                        st.markdown("### Quick Stats")
                        st.metric("Page Load Time", f"{results['load_time']:.2f}s")
                        time.sleep(0.1)
                        st.metric("Mobile Friendly", "✅ Yes" if results['mobile_friendly'] else "❌ No")
                        time.sleep(0.1)
                        st.metric("SSL Certified", "✅ Yes" if results['ssl_certified'] else "❌ No")

                    st.markdown("</div>", unsafe_allow_html=True)

                # Detailed Analysis in tabs
                st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
                st.markdown("### Detailed Analysis")

                # Make tabs more readable on mobile
                tab_names = ["Meta", "Content", "Tech", "Speed", "Security", "Links", "Improve"]
                tabs = st.tabs(tab_names)

                # Meta Tags Analysis
                with tabs[0]:
                    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
                    st.markdown("#### 🏷️ Meta Tags Analysis")
                    for item in results['meta_analysis']:
                        time.sleep(0.1)
                        if "optimal" in item.lower() or "found" in item.lower():
                            st.success(item)
                        elif "missing" in item.lower() or "too" in item.lower():
                            st.error(item)
                        else:
                            st.info(item)
                    st.markdown("</div>", unsafe_allow_html=True)

                # Content Analysis
                with tabs[1]:
                    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
                    st.markdown("#### 📝 Content Analysis")

                    metrics = {}
                    keywords = []

                    for item in results['content_analysis']:
                        if "keywords" in item.lower():
                            keywords.append(item)
                        else:
                            category = item.split(':')[0] if ':' in item else 'General'
                            if category not in metrics:
                                metrics[category] = []
                            metrics[category].append(item)

                    # Responsive columns for content metrics
                    if len(metrics) > 3:
                        col1, col2 = st.columns(2)
                    else:
                        col1, col2 = st.columns([2, 1])

                    with col1:
                        st.markdown("##### Content Metrics")
                        for category, items in metrics.items():
                            time.sleep(0.1)
                            with st.expander(category, expanded=True):
                                for item in items:
                                    st.write(item)

                    with col2:
                        st.markdown("##### Keyword Analysis")
                        for item in keywords:
                            time.sleep(0.1)
                            st.write(item)
                    st.markdown("</div>", unsafe_allow_html=True)

                # Technical Analysis with responsive columns
                with tabs[2]:
                    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
                    st.markdown("#### ⚙️ Technical Analysis")

                    technical_items = results['technical_analysis']
                    mid = len(technical_items) // 2

                    # Single column on mobile
                    if len(technical_items) > 6:
                        col1, col2 = st.columns(2)

                        with col1:
                            for item in technical_items[:mid]:
                                time.sleep(0.1)
                                if "not" in item.lower() or "needs" in item.lower():
                                    st.error(item)
                                else:
                                    st.success(item)

                        with col2:
                            for item in technical_items[mid:]:
                                time.sleep(0.1)
                                if "not" in item.lower() or "needs" in item.lower():
                                    st.error(item)
                                else:
                                    st.success(item)
                    else:
                        for item in technical_items:
                            time.sleep(0.1)
                            if "not" in item.lower() or "needs" in item.lower():
                                st.error(item)
                            else:
                                st.success(item)

                    st.markdown("</div>", unsafe_allow_html=True)

                # Speed Analysis
                with tabs[3]:
                    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
                    st.markdown("#### ⚡ Speed Analysis")
                    for item in results['speed_analysis']:
                        time.sleep(0.1)
                        if "slow" in item.lower() or "large" in item.lower():
                            st.error(item)
                        else:
                            st.success(item)
                    st.markdown("</div>", unsafe_allow_html=True)

                # Security Analysis
                with tabs[4]:
                    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
                    st.markdown("#### 🔒 Security Analysis")
                    for item in results['security_analysis']:
                        time.sleep(0.1)
                        if "not" in item.lower() or "risk" in item.lower():
                            st.error(item)
                        else:
                            st.success(item)
                    st.markdown("</div>", unsafe_allow_html=True)

                # Link Analysis
                with tabs[5]:
                    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
                    st.markdown("#### 🔗 Link Analysis")
                    for item in results['link_analysis']:
                        time.sleep(0.1)
                        if "broken" in item.lower():
                            st.error(item)
                        else:
                            st.info(item)
                    st.markdown("</div>", unsafe_allow_html=True)

                # Improvements with better grouping
                with tabs[6]:
                    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
                    st.markdown("#### 📈 Improvement Suggestions")

                    grouped_improvements = {}
                    for item in results['improvements']:
                        category = item[1:item.find(']')]
                        if category not in grouped_improvements:
                            grouped_improvements[category] = []
                        grouped_improvements[category].append(item[item.find(']')+1:].strip())

                    # Show improvements in a more compact way on mobile
                    if len(grouped_improvements) > 4:
                        cols = st.columns(2)
                        for idx, (category, improvements) in enumerate(grouped_improvements.items()):
                            with cols[idx % 2]:
                                time.sleep(0.1)
                                with st.expander(f"{category} Improvements", expanded=True):
                                    for improvement in improvements:
                                        st.markdown(f"🔸 {improvement}")
                    else:
                        for category, improvements in grouped_improvements.items():
                            time.sleep(0.1)
                            with st.expander(f"{category} Improvements", expanded=True):
                                for improvement in improvements:
                                    st.markdown(f"🔸 {improvement}")
                    st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred while analyzing the website: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Search Rank Scout")