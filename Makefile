
PYTHON=python3

DATADIR=data

.PHONY : download

# Scrape awesome-rails GitHub to get a list of rails repositories
$(DATADIR)/ruby-repos/awesome-rails-repos.csv : scripts/scrape_awesome_rails.py
	mkdir -p $(dir $@)
	$(PYTHON) $^ $@

# Download GitHub repos (URLs are found in column 2 (0-indexed) of csv file)
$(DATADIR)/ruby-repos/%/ : scripts/download_github_repos.py $(DATADIR)/ruby-repos/%.csv
	mkdir -p $@
	$(PYTHON) $^ 2 $@
	
download : $(DATADIR)/ruby-repos/awesome-rails-repos/
	
# Extract identifiers from ruby files
$(DATADIR)/word2vec/%.identifiers.txt : scripts/extract_identifiers.py \
	$(DATADIR)/ruby-repos/%/
	mkdir -p $(dir $@)
	$(PYTHON) $^ $@