.PHONY: clean
clean:
	rm -rf *.json

.PHONY: get_data
get_data:
	python data.py

.PHONY: process_data
process_data:
	python alert.py
	python topology.py

.PHONY: all
all: clean get_data process_data
