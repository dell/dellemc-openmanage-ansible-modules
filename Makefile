
venv:
	rm -rf .venv
	python3 -m venv .venv
	. .venv/bin/activate && \
	pip install ansible-core>=2.19 ansible-lint \
	-r requirements.txt \
	-r test-requirements.txt

ifneq ($(origin tname), undefined)
ttype?=modules
TC?=tests/unit/plugins/$(ttype)/test_$(tname).py
else ifneq ($(origin ttype), undefined)
TC?=tests/unit/plugins/$(ttype)
else
TC?=tests/unit/plugins
endif

# Examples
# 1. make unit-test # to run all
# 2. make unit-test ttype=module_utils # to run only module_utils
# 3. make unit-test ttype=modules_ttils tname=ome # to run only modules_utils/ome
# 4. make unit-test tname=idrac_secure_boot # ttype defaults to modules
# 5. make unit-test TC=tests/unit/plugins/modules/test_idrac_secure_boot.py
unit-test:
	rm -rf coverage
	PYTHONPATH=$(subst ansible_collections/dellemc/openmanage,,$(CURDIR)):$(PYTHONPATH) \
	pytest $(TC) --cov=plugins/ --cov-report=html:coverage
