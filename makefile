build:
	docker build -t football .

run:
	docker run --name football_bot -p 5555:5555 football