run:
	@python clean.py
	@g++ -O3 -w 1.cpp -o 1.exe -fprofile-arcs -ftest-coverage
	@echo 1.cpp 编译成功！
	@g++ -O3 -w 2.cpp -o 2.exe -fprofile-arcs -ftest-coverage
	@echo 2.cpp 编译成功！
	@1.exe < 1.in > 1.out
	@echo 1.cpp 运行成功！
	@2.exe < 1.in > 2.out
	@echo 2.cpp 运行成功！
	@gcov 1.cpp > 1.log
	@echo 1.cpp 分析成功！
	@gcov 2.cpp > 2.log
	@echo 2.cpp 分析成功！
	@python run.py
	@python clean.py
run_linux:
	@python3 clean.py
	@g++ -O3 -w 1.cpp -o 1.exe -fprofile-arcs -ftest-coverage
	@echo 1.cpp 编译成功！
	@g++ -O3 -w 2.cpp -o 2.exe -fprofile-arcs -ftest-coverage
	@echo 2.cpp 编译成功！
	@./1.exe < 1.in > 1.out
	@echo 1.cpp 运行成功！
	@./2.exe < 1.in > 2.out
	@echo 2.cpp 运行成功！
	@gcov 1.cpp > 1.log
	@echo 1.cpp 分析成功！
	@gcov 2.cpp > 2.log
	@echo 2.cpp 分析成功！
	@python3 run.py
	@python3 clean.py
install:
	@python -m pip install requests
	@python -m pip install prettytable
	@python -m pip install colorama
install_linux:
	@python3 -m pip install requests
	@python3 -m pip install prettytable
	@python3 -m pip install colorama
