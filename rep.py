import streamlit as st
import requests

# Custom CSS styles to make the app more visually appealing
st.markdown(
    """
<style>
    body {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #6c5ce7;
        color: white;
        font-weight: bold;
        border-radius: 5px;
    }
    .stTextInput>div>input {
        background-color: #dfe4ea;
        border-radius: 5px;
    }
    .stTextInput>div>label {
        color: #2f3542;
    }
    .repo-card {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .repo-name {
        font-size: 20px;
        font-weight: bold;
        color: #6c5ce7;
    }
    .repo-description {
        color: #57606f;
        margin-top: 8px;
    }
    .repo-url {
        font-size: 14px;
        margin-top: 10px;
    }
    .logo {
        display: block;
        margin: auto;
        max-width: 200px;
        padding: 10px;
    }
    .main-image {
        display: block;
        margin: 20px auto;
        max-width: 400px;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""",
    unsafe_allow_html=True,
)

def get_github_data(query, data_type):
    url = f"https://api.github.com/search/{data_type}?q={query}&sort=stars&order=desc"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["items"]
    else:
        st.error(f"Error retrieving data. Status code: {response.status_code}")
        return []

def display_repository_info(repository):
    with st.expander(label=repository["name"], expanded=True):
        st.markdown(f'<p class="repo-description">{repository["description"]}</p>', unsafe_allow_html=True)
        st.markdown(f'<a class="repo-url" href="{repository["html_url"]}" target="_blank">View on GitHub</a>', unsafe_allow_html=True)

def display_issue_info(issue):
    with st.expander(label=issue["title"], expanded=True):
        st.markdown(f'<p class="repo-description">Issue Number: {issue["number"]}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="repo-description">State: {issue["state"]}</p>', unsafe_allow_html=True)
        st.markdown(f'<a class="repo-url" href="{issue["html_url"]}" target="_blank">View on GitHub</a>', unsafe_allow_html=True)

def main():
    st.image("https://th.bing.com/th/id/OIP.cGhc54tf8cCwiPBOvxOJ2AAAAA?w=350&h=180&c=7&r=0&o=5&dpr=1.3&pid=2", width=200, caption="DATA VIEWER")
    st.title("GitHub Data Viewer")
    query = st.text_input("Enter your search query", "python")
    data_type = st.selectbox("Select data type:", ["Repositories", "Issues"])

    if st.button("Search"):
        if data_type == "Repositories":
            data = get_github_data(query, "repositories")
            if data:
                st.success(f"Found {len(data)} repositories matching '{query}'")
                for repo in data:
                    display_repository_info(repo)
            else:
                st.warning("No repositories found.")
        elif data_type == "Issues":
            data = get_github_data(query, "issues")
            if data:
                st.success(f"Found {len(data)} issues matching '{query}'")
                for issue in data:
                    display_issue_info(issue)
            else:
                st.warning("No issues found.")

if __name__ == "__main__":
    main()
