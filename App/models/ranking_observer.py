class RankingObserver:
    def update(self, student):
        print(f"Student {student.username}'s rank updated to {student.curr_rank}")
