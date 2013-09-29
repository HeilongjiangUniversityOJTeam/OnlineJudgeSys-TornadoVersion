# -*- coding:utf-8 -*-

def getNewInstance(id, title, time_limit, memory_limit, use_able,
                   description, input, output, sample_input, sample_output, hint, source):
    return {
        "_id": id,
        "title": title,

        "time_limit": time_limit,
        "memory_limit": memory_limit,
        "use_able": use_able,

        "description": description,
        "input": input,
        "output": output,
        "sample_input": sample_input,
        "sample_output": sample_output,
        "hint": hint,
        "source": source,

        "data_files": [],

        "info": {
            'total': 0,
            'Yes': 0,
            'Presentation Error': 0,
            'Time Limit Exceeded': 0,
            'Memory Limit Exceeded': 0,
            'Wrong Answer': 0,
            'Runtime Error': 0,
            'Output Limit Exceeded': 0,
            'Compile Error': 0,
            'System Error': 0
        }
    }