YOU:
	echo ""

lint:
	bash lint.sh fight_counter
	bash lint.sh tests

run:
	python3 -m fight_counter --run-gui 1