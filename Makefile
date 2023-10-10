run:
	@python clean.py
	@g++ -O3 -w 1.cpp -o 1.exe -fprofile-arcs -ftest-coverage
	@g++ -O3 -w 2.cpp -o 2.exe -fprofile-arcs -ftest-coverage
	@1.exe < 1.in > 1.out
	@2.exe < 1.in > 2.out
	@gcov 1.cpp
	@gcov 2.cpp
	@python run.py
	@python clean.py
install:
	@python -m pip install requests
	@python -m pip install prettytable
