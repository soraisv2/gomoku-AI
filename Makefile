##
## EPITECH PROJECT, 2021
## B-PSU-400-NCE-4-1-malloc-victor.sorais
## File description:
## Makefile
##

SRC		=	main.py

NAME	=	pbrain-gomoku-ai

all:		$(NAME)

$(NAME):
			cp main.py $(NAME)
			chmod +x $(NAME)

# pyinstaller --onefile $(SRC) --name $(NAME)
# mv dist/$(NAME) .


clean:
			rm -rf pbrain-gomoku-ai

fclean:		clean
			rm -rf dist/
			rm -rf build/
			rm -rf src/__pycache___/
			rm -f pbrain-gomoku-ai.spec

re:			fclean all

.PHONY: 	all clean fclean re