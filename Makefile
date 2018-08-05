# Copyright 2018 Iguazio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

.PHONY: all
all:
	$(error please pick a target)

.PHONY: upload
upload:
	rm -r dist
	python setup.py sdist bdist_wheel
	pipenv run twine upload dist/*

.PHONY: clean_pyc
clean_pyc:
	find nuclio -name '*.pyc' -exec rm {} \;
	find tests -name '*.pyc' -exec rm {} \;

.PHONY: flask8
flake8:
	pipenv run flake8 nuclio tests

.PHONY: test
test: clean_pyc flake8
	pipenv run python -m pytest -v tests

.PHONY: build-docker
build-docker:
	docker build -t tebeka/nuclio-jupyter .

.PHONY: upload-docker
upload-docker: build-docker
	docker push

# Testing markdown
README.html: README.md
	kramdown -i GFM $< > $@