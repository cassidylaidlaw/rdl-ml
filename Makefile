
PYTHON=python3

DATADIR=data

# Scrape awesome-rails GitHub to get a list of rails repositories
$(DATADIR)/ruby-repos/awesome-rails-repos.csv : scripts/scrape_awesome_rails.py
	mkdir -p $(dir $@)
	$(PYTHON) $^ $@
