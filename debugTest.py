import thunderstoneCards as tc

while True:
    a = tc.getSelection(maxTries=1)

    if not a.validate():
        break
