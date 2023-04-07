import wikipedia

# Search for a page
search_results = wikipedia.search("Python (programming language)")

# Get the page summary
page_summary = wikipedia.summary(search_results[0])
page_summary2 = wikipedia.page(search_results[0])
print(search_results)