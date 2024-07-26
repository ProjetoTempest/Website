run:
	@uvicorn Backend.src.main:app --reload

print:
	@echo $(text)