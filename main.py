import streamlit as st
from PIL import Image
from sentiment_analysis import analyze_sentiment
from utils import (
    fetch_movie_details, fetch_movie_reviews, fetch_google_recommendations, fetch_reviews_from_ai,
    get_watch_verdict, get_mood_based_on_review, extract_text_from_image, fetch_movie_recommendations_from_ai,
    calculate_overall_sentiment
)

st.title("🎬CineSence AI Movie Sentiment & Recommendation System")

movie_name = st.text_input("Enter a movie name")

if st.button("Fetch & Analyze"):
    movie = fetch_movie_details(movie_name)
    
    if movie:
        st.write(f"### 🎥 {movie['title']}")
        st.write(f"**Genre:** {movie['genre']}")
        #st.write(f"**Description:** {movie['description']}")
        st.write(f"**IMDb Rating:** {movie['imdb_rating']}")

        # ✅ **AI-Generated Summary (Now Always Full Length)**
        ai_review = fetch_reviews_from_ai(movie["title"])
        
        st.write("### 🤖 Summary & Verdict")
        st.write(f"📌 **Summary:** {ai_review}")  # Show full AI summary
        st.write(f"🎭 **Best Mood to Watch:** {get_mood_based_on_review(ai_review)}")
        st.write(f"🎯 **Verdict:** {get_watch_verdict(movie['imdb_rating'])}")
        st.markdown("---")

        # ✅ **Overall Sentiment Calculation**
        all_reviews = fetch_movie_reviews(movie["id"], movie["title"])
        overall_sentiment = calculate_overall_sentiment(all_reviews)
        st.write(f"### 📊 {overall_sentiment}")
        st.markdown("---")

        # ✅ **Collapsible Long Reviews (First 3-4 Lines Visible)**
        if all_reviews:
            for index, review in enumerate(all_reviews[:10]):
                sentiment, score = analyze_sentiment(review)
                
                # Split review into lines & show only the first 3-4
                review_lines = review.split("\n")
                short_review = "\n".join(review_lines[:4])  # Show only 3-4 lines initially

                st.write(f"📌 **Review {index+1}:** {sentiment} (Score: {score:.2f})")
                st.write(short_review + "...")  # Show short version
                
                with st.expander("Show More"):
                    st.write(review)  # Full review expands here
                
                st.markdown("---")
        else:
            st.warning("⚠ No reviews found.")

        # ✅ Movie Recommendations (Google & AI Fallback)
        recommendations = fetch_google_recommendations(movie["genre"])
        if not recommendations:
            recommendations = fetch_movie_recommendations_from_ai(movie["genre"])

        st.write("### 🎬 Recommended Movies ")
        if recommendations:
            for rec in recommendations[:5]:
                st.write(f"- {rec}")
        else:
            st.warning("⚠ No recommendations found.")

# ✅ Custom Text & Image-Based Sentiment Analysis
st.write("## 📝 Analyze Text or Image Sentiment")
user_text = st.text_area("Enter text for sentiment analysis")

uploaded_image = st.file_uploader("Upload an image with text for sentiment analysis", type=["png", "jpg", "jpeg"])

if st.button("Analyze Sentiment"):
    extracted_text = None

    # ✅ **Added Spinner for Image Processing**
    with st.spinner("🔍 Extracting text from the image..."):
        if uploaded_image:
            image = Image.open(uploaded_image)
            extracted_text = extract_text_from_image(image)

    text_to_analyze = extracted_text if extracted_text else user_text

    if text_to_analyze.strip():
        sentiment, score = analyze_sentiment(text_to_analyze)
        st.write(f"**Extracted Text:** {text_to_analyze}" if extracted_text else "")
        st.write("**Sentiment:**", sentiment)
        st.write("**Sentiment Score:**", score)
    else:
        st.warning("⚠ Please enter text or upload an image with text.")
