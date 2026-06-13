# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: bbeaurai <bbeaurai@student.42lehavre.fr    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/06/04 13:42:06 by bbeaurai          #+#    #+#              #
#    Updated: 2026/06/13 09:29:59 by bbeaurai         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

UV = uv
VENV = .venv
PYTHON = $(VENV)/bin/python
INSTALL_LOG = /tmp/callmemaybe-uv-install.log
PROJECT_FILES = pyproject.toml uv.lock

RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[0;33m
BLUE = \033[0;34m
PINK = \033[35m
NC = \033[0m

all : run

$(PYTHON) :
	@echo ""
	@echo "$(YELLOW)VENV ACTIVATION$(NC)"
	@$(UV) venv $(VENV)
	clear

install : $(PYTHON) $(PROJECT_FILES) llm_sdk/pyproject.toml
	@echo ""
	@log_file="$(INSTALL_LOG)"; \
	printf "$(PINK)DEPENDENCY INSTALL$(NC)\n"; \
	( \
		while :; do \
			for frame in '|' '/' '-' '\\'; do \
				printf "\r$(PINK)Checking dependencies... %s$(NC)" "$$frame"; \
				sleep 0.12; \
			done; \
		done \
	) & \
	spinner=$$!; \
	trap 'kill $$spinner 2>/dev/null' EXIT INT TERM; \
	{ \
		$(UV) sync --python $(PYTHON) && \
		$(UV) pip install --python $(PYTHON) -q -e llm_sdk/; \
	} >"$$log_file" 2>&1; \
	status=$$?; \
	kill $$spinner 2>/dev/null; \
	wait $$spinner 2>/dev/null; \
	trap - EXIT INT TERM; \
	if [ $$status -ne 0 ]; then \
		printf "\r$(RED)Checking dependencies... [FAILED]$(NC)\n"; \
		cat "$$log_file"; \
		exit $$status; \
	fi; \
	printf "\r$(GREEN)Checking dependencies... [OK]$(NC)\n"
	clear

run : install
	@echo ""
	@echo "$(GREEN)LAUNCH IN PROGRESS...$(NC)"
	clear
	@$(UV) run --python $(PYTHON) main.py

debug : install
	@$(UV) run --python $(PYTHON) python -m pdb main.py

lint : install
	@echo ""
	@echo "$(RED)TESTING FLAKE8 / MYPY...$(NC)"
	@$(UV) run --python $(PYTHON) flake8 --exclude .venv,venv,llm_sdk
	@$(UV) run --python $(PYTHON) mypy . --explicit-package-bases --exclude "(^|/)(\\.venv|venv|llm_sdk)($$|/)" --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	@echo ""

lint-strict : install
	@echo ""
	@echo "$(RED)TESTING FLAKE8 / MYPY STRICT...$(NC)"
	@$(UV) run --python $(PYTHON) flake8 . --exclude .venv,venv,llm_sdk
	@$(UV) run --python $(PYTHON) mypy . --strict --explicit-package-bases --exclude "(^|/)(\\.venv|venv|llm_sdk)($$|/)"
	@echo ""

clean :
	@echo ""
	@echo "$(RED)CLEANING...$(NC)"
	@find . -name "__pycache__" -exec rm -rf {} \+
	@find . -name ".mypy_cache" -exec rm -rf {} \+
	@find . -name ".vscode" -exec rm -rf {} \+
	@echo "$(GREEN)DELETE [OK]...$(NC)"

uninstall : $(PYTHON)
	@$(UV) pip uninstall --python $(PYTHON) -y llm-sdk

uninstall_venv :
	rm -rf $(VENV) venv

.PHONY: all clean debug install lint lint-strict run uninstall uninstall_venv
