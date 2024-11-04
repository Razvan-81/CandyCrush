import random
from typing import List, Tuple

class CandyCrush:
    def __init__(self, size: int = 11):
        self.size = size
        self.board = [[random.randint(1, 4) for _ in range(size)] for _ in range(size)]
        self.score = 0
        self.target_score = 10000
        self.number_of_moves = 0  
        self.move_history = []
        self.process_formations()

    def print_board(self):
        print("\nCurrent Board:")
        for row in self.board:
            print(' '.join(str(x) for x in row))
        print(f"\nScore: {self.score} | Moves: {self.number_of_moves}")

    def find_all_formations(self) -> List[Tuple[List[Tuple[int, int]], int]]:
        formations = []
        formation_checks = [
            (self.find_lines_of_n, 50, 5),
            (self.find_t_formations, 30, None),
            (self.find_l_formations, 20, None),
            (self.find_lines_of_n, 10, 4),
            (self.find_lines_of_n, 5, 3)
        ]

        for check_func, points, n in formation_checks:
            if n is not None:
                new_formations = check_func(n)
            else:
                new_formations = check_func()
            formations.extend((formation, points) for formation in new_formations)

        return formations

    def find_lines_of_n(self, n: int) -> List[List[Tuple[int, int]]]:
        lines = []
        
        for i in range(self.size):
            for j in range(self.size - n + 1):
                if self.board[i][j] != 0 and all(self.board[i][j] == self.board[i][j+k] for k in range(n)):
                    lines.append([(i, j+k) for k in range(n)])
        
        for j in range(self.size):
            for i in range(self.size - n + 1):
                if self.board[i][j] != 0 and all(self.board[i][j] == self.board[i+k][j] for k in range(n)):
                    lines.append([(i+k, j) for k in range(n)])
        
        return lines

    def find_special_formation(self, pattern: List[Tuple[int, int]]) -> List[List[Tuple[int, int]]]:
        formations = []
        for i in range(self.size):
            for j in range(self.size):
                formation = []
                valid_formation = True
                
                for di, dj in pattern:
                    new_i, new_j = i + di, j + dj
                    if not (0 <= new_i < self.size and 0 <= new_j < self.size):
                        valid_formation = False
                        break
                    if self.board[new_i][new_j] == 0 or (formation and self.board[new_i][new_j] != self.board[formation[0][0]][formation[0][1]]):
                        valid_formation = False
                        break
                    formation.append((new_i, new_j))
                
                if valid_formation:
                    formations.append(formation)
        
        return formations

    def find_t_formations(self) -> List[List[Tuple[int, int]]]:
        t_pattern = [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)]
        return self.find_special_formation(t_pattern)

    def find_l_formations(self) -> List[List[Tuple[int, int]]]:
        l_pattern = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
        return self.find_special_formation(l_pattern)

    def drop_candies(self):
        for j in range(self.size):
            column = [self.board[i][j] for i in range(self.size) if self.board[i][j] != 0]
            new_candies = [random.randint(1, 4) for _ in range(self.size - len(column))]
            for i in range(self.size):
                if i < len(column):
                    self.board[i][j] = column[i]
                else:
                    self.board[i][j] = new_candies[i - len(column)]

    def process_formations(self):
        while True:
            formations = self.find_all_formations()
            if not formations:
                break
            
            for formation, points in formations:
                self.score += points
                for i, j in formation:
                    self.board[i][j] = 0
            
            self.drop_candies()

    def find_best_swap(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        best_score = 0
        best_swap = None
        
        for i in range(self.size):
            for j in range(self.size):
                if j + 1 < self.size:
                    score = self.evaluate_swap((i, j), (i, j + 1))
                    if score > best_score:
                        best_score = score
                        best_swap = ((i, j), (i, j + 1))
                
                if i + 1 < self.size:
                    score = self.evaluate_swap((i, j), (i + 1, j))
                    if score > best_score:
                        best_score = score
                        best_swap = ((i, j), (i + 1, j))

        return best_swap

    def evaluate_swap(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        temp_board = [row[:] for row in self.board]
        i1, j1 = pos1
        i2, j2 = pos2
        temp_board[i1][j1], temp_board[i2][j2] = temp_board[i2][j2], temp_board[i1][j1]
        
        formations = self.find_all_formations_on_board(temp_board)
        return sum(points for _, points in formations)

    def find_all_formations_on_board(self, board) -> List[Tuple[List[Tuple[int, int]], int]]:
        temp_board = self.board
        self.board = board
        formations = self.find_all_formations()
        self.board = temp_board
        return formations

    def swap_candies(self, pos1: Tuple[int, int], pos2: Tuple[int, int]):
        i1, j1 = pos1
        i2, j2 = pos2
        self.board[i1][j1], self.board[i2][j2] = self.board[i2][j2], self.board[i1][j1]
        self.move_history.append((pos1, pos2))

    def play_game(self):
        self.print_board()
        while self.score < self.target_score:
            best_swap = self.find_best_swap()
            if best_swap is None:
                print("No more possible moves!")
                break
            
            self.swap_candies(best_swap[0], best_swap[1])
            self.number_of_moves += 1
            print(f"Swapped {best_swap[0]} with {best_swap[1]}")
            self.process_formations()
            self.print_board()

def main():
    total_score = 0
    total_moves = 0
    num_games = 100

    for _ in range(num_games):
        game = CandyCrush()
        game.play_game()
        total_score += game.score
        total_moves += game.number_of_moves

    average_score = total_score / num_games
    average_moves = total_moves / num_games

    print(f"\nAverage Score over {num_games} games: {average_score:.2f}")
    print(f"Average Moves over {num_games} games: {average_moves:.2f}")

if __name__ == "__main__":
    main()
