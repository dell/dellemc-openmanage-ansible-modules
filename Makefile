
venv:
	rm -rf .venv
	python3 -m venv .venv
	. .venv/bin/activate && \
	pip install ansible ansible-lint \
	-r requirements.txt \
	-r test-requirements.txt

# Examples
# 1. make unit-test
# 2. make unit-test TC=tests/unit/plugins/modules/
# 3. make unit-test TC=tests/unit/plugins/modules/test_idrac_secure_boot.py
unit-test:
	rm -rf coverage
	PYTHONPATH=$(subst ansible_collections/dellemc/openmanage,,$(CURDIR)) \
	pytest $(TC) --cov --cov-report=html:coverage
