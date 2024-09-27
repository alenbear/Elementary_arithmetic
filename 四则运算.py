import random
from fractions import Fraction
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

# 将假分数转换为真分数的格式化函数
def format_fraction(fraction):
    if fraction.numerator == 0:
        return "0"  # 处理零的情况
    negative = fraction.numerator < 0
    abs_numerator = abs(fraction.numerator)
    denominator = fraction.denominator

    if abs_numerator >= denominator:
        integer_part = abs_numerator // denominator
        remainder = abs_numerator % denominator
        if remainder == 0:
            return f"{'-' if negative else ''}{integer_part}"
        else:
            return f"{'-' if negative else ''}{integer_part}'{remainder}/{denominator}"
    else:
        return f"{'-' if negative else ''}{abs_numerator}/{denominator}"

# 随机生成子表达式，确保分母不为零
def generate_sub_expression(max_range):
    numerator = random.randint(1, max_range - 1)
    denominator = random.randint(1, max_range - 1)
    while denominator == 0:  # 确保分母不为零
        denominator = random.randint(1, max_range - 1)
    return Fraction(numerator, denominator)

"""  
    生成一个包含随机子表达式和运算符的复合表达式，并计算其结果。  
  
    参数:  
    max_range (int): 子表达式中数字（分子和分母）的最大范围（包括边界）。  
  
    返回:  
    tuple: 包含两个元素的元组。  
        - 第一个元素是格式化后的复合表达式字符串。  
        - 第二个元素是表达式计算结果的混合分数表示。  
"""  
def generate_complex_expression(max_range):
   
    num_sub_expressions = random.randint(3, 4)  # 随机生成子表达式的数量  
    expressions = []  # 存储生成的子表达式（Fraction对象）  
    results = []     #存储生成的结果

    # 生成子表达式
    for _ in range(num_sub_expressions):
        sub_expr = generate_sub_expression(max_range)
        expressions.append(sub_expr)
        results.append(sub_expr)

    combined_expression = []  # 存储最终的表达式
    operators = []  # 存储运算符

    # 构建表达式
    for i in range(num_sub_expressions):
        combined_expression.append(expressions[i])  # 添加子表达式
        if i < num_sub_expressions - 1:  # 不是最后一个元素
            operator = random.choice(['+', '-', '*', '/'])
            combined_expression.append(operator)  # 添加运算符
            operators.append(operator)  # 存储运算符

    # 计算结果，先乘除后加减
    total_result = []  # 存储中间结果
    current_value = combined_expression[0]  # 初始化当前值为第一个子表达式

    for i in range(1, len(combined_expression)):
        if isinstance(combined_expression[i], str):  # 如果是运算符
            if combined_expression[i] in ['*', '/']: # 乘法和除法
                if combined_expression[i] == '*':
                    current_value *= combined_expression[i + 1]
                elif combined_expression[i] == '/':
                    current_value /= combined_expression[i + 1]
            else:  # 加法和减法
                total_result.append(current_value)  # 将当前值添加到结果列表
                total_result.append(combined_expression[i])  # 添加运算符
                current_value = combined_expression[i + 1]  # 更新当前值

    total_result.append(current_value)  # 添加最后的值

    # 计算加减法结果
    final_result = total_result[0]
    for i in range(1, len(total_result), 2):  # 遍历运算符
        if total_result[i] == '+':
            final_result += total_result[i + 1]
        elif total_result[i] == '-':
            final_result -= total_result[i + 1]

    # 格式化输出
    formatted_expression = []
    for item in combined_expression:  
        if isinstance(item, Fraction): # 元素是Fraction类型（即分数）  
            formatted_expression.append(format_fraction(item))
        else:
            formatted_expression.append(item)

    final_expression = " ".join(map(str, formatted_expression)) # 使用map函数将formatted_expression列表中的每个元素转换为字符串，并使用" ".join()方法将它们连接成一个字符串
 
    final_expression = final_expression.replace('*', '×').replace(' / ', ' ÷ ')  #替换字符串中的'*'为'×'，' / '为' ÷ '，使表达式更易于阅读
    final_result_as_mixed = format_fraction(final_result)

    return final_expression, final_result_as_mixed


def write_to_file(questions, answers):
    with open('Exercises.txt', 'w', encoding='utf-8') as q_file, open('Answers.txt', 'w', encoding='utf-8') as a_file:
        for i, (q, a) in enumerate(zip(questions, answers)):
            q_file.write(f"{i + 1}. {q}\n")
            a_file.write(f"{i + 1}. {a}\n")

def generate_questions(num_questions, max_range):
    questions = []
    answers = []

    while len(questions) < num_questions:
        question, answer = generate_complex_expression(max_range)
        if question not in questions:
            questions.append(question)
            answers.append(answer)

    write_to_file(questions, answers)
    return questions, answers

def create_gui():
    window = tk.Tk()
    window.title("四则运算生成器")
    window.geometry("400x400")

    tk.Label(window, text="生成题目数量:").pack(pady=10)
    num_entry = tk.Entry(window)
    num_entry.pack()

    tk.Label(window, text="数值范围（最大值）:").pack(pady=10)
    range_entry = tk.Entry(window)
    range_entry.pack()

    questions = []
    answers = []

    # def show_questions():
    #     num_questions = int(num_entry.get())
    #     max_range = int(range_entry.get())
    #     nonlocal questions, answers
    #     questions, answers = generate_questions(num_questions, max_range)

    #     question_window = tk.Toplevel(window)
    #     question_window.title("生成的题目")

    #     text_area = scrolledtext.ScrolledText(question_window, width=100, height=20)
    #     text_area.pack()
    #     for i, q in enumerate(questions):
    #         text_area.insert(tk.END, f"{i + 1}. {q}\n")

    # def show_answers():
    #     answer_window = tk.Toplevel(window)
    #     answer_window.title("生成的答案")

    #     text_area = scrolledtext.ScrolledText(answer_window, width=50, height=20)
    #     text_area.pack()
    #     for i, a in enumerate(answers):
    #         text_area.insert(tk.END, f"{i + 1}. {a}\n")


    def show_questions():  
        num_questions = num_entry.get().strip()  
        max_range = range_entry.get().strip()  
          
        if not num_questions or not max_range:  
            messagebox.showerror("错误", "请确保输入了题目数量和范围。")  
            return  
          
        try:  
            num_questions = int(num_questions)  
            max_range = int(max_range)  
        except ValueError:  
            messagebox.showerror("错误", "请确保输入的是有效的整数。")  
            return  
      
        nonlocal questions, answers  
        questions, answers = generate_questions(num_questions, max_range)  
      
        question_window = tk.Toplevel(window)  
        question_window.title("生成的题目")  
      
        text_area = scrolledtext.ScrolledText(question_window, width=100, height=20)  
        text_area.pack()  
        for i, q in enumerate(questions):  
            text_area.insert(tk.END, f"{i + 1}. {q}\n")  
  
    def show_answers():  
        if not answers:  
            messagebox.showerror("错误", "请先生成题目以查看答案。")  
            return  
      
        answer_window = tk.Toplevel(window)  
        answer_window.title("生成的答案")  
      
        text_area = scrolledtext.ScrolledText(answer_window, width=50, height=20)  
        text_area.pack()  
        for i, a in enumerate(answers):  
            text_area.insert(tk.END, f"{i + 1}. {a}\n")         

    tk.Button(window, text="显示题目", command=show_questions).pack(pady=10)
    tk.Button(window, text="显示答案", command=show_answers).pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    create_gui()
