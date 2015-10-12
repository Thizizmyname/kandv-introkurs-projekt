import thunderstoneCards as tc
TESTS = 1000

counter = 0.0
for _ in range(TESTS):
    selection = tc.getSelection()

    if not selection.validate():
        counter += 1


ratio = counter/TESTS
print ratio
