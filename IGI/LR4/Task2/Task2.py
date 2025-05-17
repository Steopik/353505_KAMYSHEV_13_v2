from . import classes_task2
import os

def menu_task2():
    base_dir = os.path.dirname(__file__)
    input_path = os.path.join(base_dir, "Task2_input.txt")
    output_path = os.path.join(base_dir, "Task2_output.txt")
    zip_path = os.path.join(base_dir, "Task2.zip")

    txt =  classes_task2.FileWorker.reader(input_path)

    analyzer = classes_task2.SuperAnalyzer(txt)
    
    output_content = analyzer.analyze_text()
    print(output_content)

    classes_task2.FileWorker.writer(output_path, output_content)

    classes_task2.FileWorker.zipper(zip_path, output_path)
    print(classes_task2.FileWorker.get_zip_inform(zip_path))


