CFLAGS = -g -Wall -c

.Phony: all

all: serveur client

serveur: serveur.o functions.o
	gcc serveur.o functions.o -o serveur

client: client.o functions.o
	gcc client.o functions.o -o client

serveur.o: serveur.c functions.h
	gcc $(CFLAGS) -c serveur.c -o serveur.o

client.o: client.c functions.h
	gcc $(CFLAGS) -c client.c -o client.o

functions.o: functions.c functions.h
	gcc $(CFLAGS) -c functions.c -o functions.o
