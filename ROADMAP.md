# E-Commerce Product Data Collector Roadmap

## Version 1 — API Data Collection

- [x] Connect to the API
- [x] Fetch product data
- [x] Handle request errors
- [x] Accept a search keyword from the user
- [x] Validate user input
- [x] Select relevant product fields
- [x] Handle missing data
- [x] Remove duplicate products
- [x] Filter results
- [x] Sort results
- [x] Export results to CSV
- [x] Export results to JSON
- [x] Display a process summary
- [x] Reject invalid numeric values such as NaN and infinity
- [x] Validate numeric fields received from the API
- [x] Refactor the program into reusable functions
- [x] Generate safe timestamped output filenames

## Version 1.1 — Code Quality

- [x] Organize the program with a `main()` function
- [x] Separate input, API, cleaning, filtering, sorting, and export operations
- [x] Add file output error handling
- [ ] Add type hints
- [ ] Add docstrings
- [ ] Add automated tests

## Version 2 — BeautifulSoup

- [ ] Collect product data from public web pages
- [ ] Parse HTML elements
- [ ] Add pagination support
- [ ] Respect website rules and robots.txt
- [ ] Combine API and website data

## Version 3 — Pandas

- [ ] Convert data into a DataFrame
- [ ] Clean missing values
- [ ] Remove duplicate records
- [ ] Generate an Excel report
- [ ] Create category summaries
- [ ] Analyze prices and stock levels

## Version 4 — Selenium

- [ ] Collect data from dynamic web pages
- [ ] Add browser automation
- [ ] Handle explicit waits
- [ ] Navigate through multiple pages
- [ ] Add a retry system

## Final Portfolio Version

- [ ] Split the code into modules
- [ ] Add a configuration file
- [ ] Add logging
- [ ] Write basic tests
- [x] Add sample output files
- [x] Complete the README
- [ ] Add screenshots
- [ ] Publish a GitHub release