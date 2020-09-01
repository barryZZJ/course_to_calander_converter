from typing import List, Tuple, Dict

class Course:
    """
    一门课的信息
    """
    
    def __init__(self, course_name, instr_name, course_times: Dict[str, List[Tuple]]):
        """
        course_times: Dict{ location : [(start_time, end_time), ...] }
        """
        self.course_name = course_name
        self.instr_name = instr_name
        self.course_times = course_times
        
    


