.PHONY: check fix

HATCH = hatch

check:
	$(HATCH) $(HATCHFLAGS) fmt --check
	$(HATCH) $(HATCHFLAGS) run types:check
	$(HATCH) $(HATCHFLAGS) test

fix:
	$(HATCH) $(HATCHFLAGS) fmt
