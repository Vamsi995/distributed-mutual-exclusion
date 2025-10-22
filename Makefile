PORT1=8001
PORT2=8002
PORT3=8003
PORT4=8004


.PHONY: run_clients
run_clients:

	python3 client1.py -port $(PORT1) -client 1 & echo $$! > pids.txt; \
	sleep 1; \
	python3 client2.py -port $(PORT2) -client 2 & echo $$! >> pids.txt; \
	sleep 1; \
	python3 client3.py -port $(PORT3) -client 3 & echo $$! >> pids.txt; \

	sleep 2; \
	python3 master.py -port $(PORT4) -inputfile testcases.txt -outputfile output.txt & echo $$! >> pids.txt


stop:
	@echo "Killing processes..."
	@xargs kill < pids.txt || true
	@rm -f pids.txt


