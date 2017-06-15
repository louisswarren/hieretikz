drinker.pdf: *.py
	python3 drinker.py

.PHONY: clean
clean:
	rm drinker.{aux,log,pdf,tex}
