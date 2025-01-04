import streamlit as st
import os
from scraper import scrape_and_append_to_csv

def main():
    st.title("Facebook Friends Scraper")
    st.write("""
    Select either a single HTML file or multiple HTML files (like a folder’s contents). 
    The app will parse each file and append the results to the specified CSV.
    """)

    input_mode = st.radio(
        "Do you want to scrape a single HTML file or multiple files?",
        ["Single HTML File", "Directory of HTML Files"]
    )

    # Let the user specify or change the output CSV location
    default_csv_path = "friends_list.csv"
    csv_file = st.text_input("Output CSV file path:", default_csv_path)

    if input_mode == "Single HTML File":
        # Let user pick a single HTML file
        uploaded_file = st.file_uploader(
            "Select a single HTML file",
            type=["html"],
            accept_multiple_files=False
        )
        
        if st.button("Scrape Single File"):
            if uploaded_file is None:
                st.warning("Please upload an HTML file first.")
            else:
                # Save the uploaded file temporarily
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.read())

                # Now run the scraper on this temp file
                try:
                    scrape_and_append_to_csv(temp_path, csv_file)
                    st.success(f"Scraped '{uploaded_file.name}' and appended to '{csv_file}'.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                finally:
                    # Optionally, remove the temp file afterward
                    if os.path.exists(temp_path):
                        os.remove(temp_path)

    else:  # "Directory of HTML Files" mode
        # Let user pick multiple HTML files
        multiple_files = st.file_uploader(
            "Select multiple HTML files from a folder",
            type=["html"],
            accept_multiple_files=True
        )

        if st.button("Scrape Directory"):
            if not multiple_files:
                st.warning("Please upload at least one HTML file.")
            else:
                errors = []
                # Loop through each file
                for uploaded_file in multiple_files:
                    temp_path = f"temp_{uploaded_file.name}"
                    # Save to a temp file
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.read())

                    # Scrape each file
                    try:
                        scrape_and_append_to_csv(temp_path, csv_file)
                    except Exception as e:
                        errors.append((uploaded_file.name, str(e)))
                    finally:
                        # Remove the temp file
                        if os.path.exists(temp_path):
                            os.remove(temp_path)

                # Show success or error messages
                if errors:
                    st.error("Some files encountered errors:")
                    for filename, err_msg in errors:
                        st.write(f"**{filename}**: {err_msg}")
                else:
                    st.success(f"Scraped {len(multiple_files)} file(s) successfully and appended to '{csv_file}'.")

if __name__ == "__main__":
    main()
