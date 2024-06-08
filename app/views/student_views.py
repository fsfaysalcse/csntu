from flask import Blueprint, render_template, request, jsonify
import openai
import pandas as pd
import markdown2

from ..models import db, Task, User, Module

student_views = Blueprint('student_views', __name__)

# Configure the OpenAI API key
openai.api_key = "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"

@student_views.route('/student')
def student_performance():
    student_id = request.args.get('id', type=int)
    student = User.query.get_or_404(student_id)

    # Get only the modules that have tasks for the given student
    modules = db.session.query(Module).join(Task).filter(Task.student_id == student_id).distinct().all()
    module_data = []

    for module in modules:
        tasks = Task.query.filter_by(student_id=student_id, module_id=module.id).all()
        total_tasks = len(tasks)
        avg_mark = sum(task.mark for task in tasks) / total_tasks if total_tasks > 0 else 0
        module_data.append({
            'module_id': module.id,
            'module_code': module.module_code,
            'module_name': module.name,
            'total_tasks': total_tasks,
            'avg_mark': avg_mark
        })

    return render_template('student_performance.html', student=student, module_data=module_data)

@student_views.route('/student/chat', methods=['POST'])
def chat():
    student_id = request.form.get('student_id', type=int)
    module_id = request.form.get('module_id', type=int)
    prompt = request.form.get('prompt')

    # Retrieve the student's module performance data
    tasks = Task.query.filter_by(student_id=student_id, module_id=module_id).all()
    total_tasks = len(tasks)
    avg_mark = sum(task.mark for task in tasks) / total_tasks if total_tasks > 0 else 0

    # Create a DataFrame for the student's module performance
    data = {
        'Task ID': [task.id for task in tasks],
        'Chapter': [task.chapter for task in tasks],
        'Mark': [task.mark for task in tasks],
        'Total Mark': [task.total_mark for task in tasks],
        'Task Type': [task.task_type for task in tasks],
        'Date': [task.datetime.strftime('%Y-%m-%d') for task in tasks]
    }
    df = pd.DataFrame(data)
    csv_data = df.to_csv(index=False)

    # Construct the message for ChatGPT
    message = f"Student's module performance data: {csv_data}\nThe student's query is: {prompt}"

    # Call the OpenAI API using the ChatCompletion endpoint
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ],
        max_tokens=150
    )

    markdown_response = markdown2.markdown(response['choices'][0]['message']['content'].strip())

    return jsonify(response=markdown_response)
