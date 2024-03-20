import csv
# from app.models.grading_result import GradingResult

class ResultProcessor:
    def __init__(self):
        pass

    def save_results_to_csv(self, grading_results, output_path):
        with open(output_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Student ID', 'Score'])

            for result in grading_results:
                writer.writerow([result.student_id, result.score])

    def generate_report(self, grading_results):
        total_students = len(grading_results)
        total_score = sum(result.score for result in grading_results)
        average_score = total_score / total_students

        report = f"Grading Report\n"
        report += f"Total Students: {total_students}\n"
        report += f"Average Score: {average_score:.2f}\n"

        return report