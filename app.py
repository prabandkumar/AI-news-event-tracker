import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------
# PAGE TITLE
# --------------------------------

st.title("📰 AI News Event Clustering System")

st.write(
    "This dashboard displays clustered news events, "
    "event timelines, summaries, and related articles."
)

# --------------------------------
# SIDEBAR
# --------------------------------

st.sidebar.title("📂 Navigation")

st.sidebar.write("AI News Event Clustering Dashboard")

st.sidebar.write("Select an event group to explore timelines, summaries, and related articles.")

# --------------------------------
# EVENT LABELS
# --------------------------------

event_labels = {
    0: "Trump Campaign and Election Strategy",
    1: "Hillary Clinton Controversies",
    2: "Trump Media Reactions and Public Opinion",
    3: "Race Politics and Black Lives Matter",
    4: "Republican Support and Trump Movement"
}

# --------------------------------
# LOAD DATA
# --------------------------------

df = pd.read_csv("cleaned_news.csv")

df['date'] = pd.to_datetime(df['date'])

# --------------------------------
# SELECT EVENT
# --------------------------------

selected_cluster = st.selectbox(
    "Select Event Group",
    list(event_labels.keys()),
    format_func=lambda x: event_labels[x]
)

# filter cluster
cluster_articles = df[df['cluster'] == selected_cluster]

# sort by date
cluster_articles = cluster_articles.sort_values(by='date')

# --------------------------------
# EVENT SUMMARY
# --------------------------------

st.header("📌 Event Summary")

summaries = {
    0: "This event focused on Donald Trump’s campaign strategy, debates, immigration discussions, and political developments during the 2016 election.",

    1: "This event covered controversies surrounding Hillary Clinton, including campaign criticism, public reactions, and political debates.",

    2: "This event highlighted media reactions, protests, and public opinion related to Donald Trump during the election season.",

    3: "This event focused on race politics, Black Lives Matter discussions, and political responses during the 2016 election.",

    4: "This event included Republican support movements, anti-Trump campaigns, and political strategy discussions."
}

st.write(summaries[selected_cluster])

st.metric(
    "Number of Articles",
    len(cluster_articles)
)

# --------------------------------
# EVENT TIMELINE
# --------------------------------

st.header("📅 Event Evolution Timeline")

timeline_articles = cluster_articles.head(5)

for i, (_, row) in enumerate(timeline_articles.iterrows(), 1):

    title = row['title'].split(" - ")[0]

    st.markdown(
        f"""
        ### 🔹 {row['date'].date()}
        **Event:** {title}
        """
    )

    st.write("---")

search_term = st.text_input("🔍 Search Articles")

if search_term:

    cluster_articles = cluster_articles[
        cluster_articles['title']
        .str.contains(search_term, case=False)
    ]

# --------------------------------
# ARTICLES INSIDE EVENT
# --------------------------------

st.header("📰 Articles Inside Event")

for i, (_, row) in enumerate(cluster_articles.iterrows(), 1):

    with st.expander(f"{i}. {row['title']}"):

        st.write(f"📅 Date: {row['date'].date()}")

        st.write(f"🏢 Source: {row['publication']}")

        # short preview
        content = str(row['content'])[:300]

        st.write(content + "...")