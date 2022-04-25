from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from db import Model, engine


class User(Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Question(Model):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    question = Column(String(200))
    ata_description = Column(String(100))
    level = Column(Integer)
    training_id = Column(Integer, ForeignKey('training.id', ondelete="CASCADE"))
    enabled = Column(Boolean, default=True, nullable=False)
    checked = Column(Boolean, default=False, nullable=False)
    ataDigit = Column(String(8))
    book_page = Column(String(20))
    issue_date = Column(Date)
    check_date = Column(Date)
    change_date = Column(Date)
    ref_to_old_id = Column(Integer, default=0)
    ref_to_new_id = Column(Integer, default=0)
    issued_by = Column(String(30))
    checked_by = Column(String(30))
    changed_by = Column(String(30))
    avg_incorrect_percentage = Column(Integer, default=0)
    times = Column(Integer, default=0)
    disable_reason = Column(String(50))
    answers = relationship('Answer',
                           backref='answers',
                           lazy='dynamic',
                           cascade="all, delete")
    exam_questions = relationship('ExamQuestion',
                                  backref='exam_questions',
                                  lazy='dynamic',
                                  cascade="all, delete")

    def __repr__(self):
        return '<Question {}>'.format(self.question)


class Answer(Model):
    __tablename__ = 'answer'

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('question.id', ondelete="CASCADE"))
    answer = Column(String(200))
    correct = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return '<Answer {}>'.format(self.answer)


class Training(Model):
    __tablename__ = 'training'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    questions = relationship('Question',
                             backref='questions',
                             lazy='dynamic',
                             cascade="all, delete")
    caf_info = relationship('CAF',
                            backref='caf',
                            lazy='dynamic',
                            cascade="all, delete")
    courses = relationship('Course', backref='courses', lazy='dynamic')


class Student(Model):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    surname = Column(String(30))
    dob = Column(Date)
    variant = Column(Integer)
    course_id = Column(Integer, ForeignKey('course.id'))

    def __repr__(self):
        return '<Student {}>'.format(self.surname)


class Course(Model):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    number_of_variants = Column(Integer)
    training_id = Column(Integer, ForeignKey('training.id'))
    students = relationship('Student', backref='courseID', lazy='dynamic', cascade="all, delete")
    exams = relationship('Exam', backref='exam_id', lazy='dynamic', cascade="all, delete")
    course_number_vdtm = Column(String(50))


class Exam(Model):
    __tablename__ = 'exam'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    course_id = Column(Integer, ForeignKey('course.id'))
    ata_chapters = Column(String(30))
    is_reexam = Column(Boolean, default=False, nullable=False)
    first_attempt_id = Column(Integer)
    second_attempt_id = Column(Integer)
    is_checked = Column(Boolean, default=False, nullable=False)
    note_for_examiner = Column(String(30))
    answers_key_var1 = Column(String(200))
    answers_key_var2 = Column(String(200))
    questions = relationship('ExamQuestion',
                             backref='questions',
                             lazy='dynamic',
                             cascade="all, delete")

    stats = relationship('QuestionResult',
                             backref='stats',
                             lazy='dynamic',
                             cascade="all, delete")


class ExamQuestion(Model):
    __tablename__ = 'examquestion'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('question.id', ondelete='CASCADE'))
    exam_id = Column(Integer, ForeignKey('exam.id'))
    variant_number = Column(Integer)
    seq_number = Column(Integer)
    is_used = Column(Boolean, default=False, nullable=False)
    incorrect_percentage = Column(Integer, default=0)
    incorrect_number = Column(Integer, default=0)

    last_seq_number = Column(Integer)

    def __repr__(self):
        return '<Exam Question from question ID {}>'.format(self.question_id)


class CAF(Model):
    __tablename__ = 'CAF'
    id = Column(Integer, primary_key=True)
    training_id = Column(Integer, ForeignKey('training.id', ondelete='CASCADE'))
    ata_digit = Column(String(10))
    questions_number = Column(Integer)
    level = Column(Integer)
    description = Column(String(200))
    tution_hours = Column(String(30))


class Result(Model):
    __tablename__ = 'result'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id', ondelete='CASCADE'))
    exam_id = Column(Integer, ForeignKey('exam.id', ondelete='CASCADE'))
    percentage = Column(Integer)
    incorrect_questions = Column(String(50))

class QuestionResult(Model):
    __tablename__ = 'question_result'
    id = Column(Integer, primary_key=True)
    exam_id = Column(Integer, ForeignKey('exam.id', ondelete='CASCADE'))
    question_id = Column(Integer, ForeignKey('question.id', ondelete='CASCADE'))
    student_id = Column(Integer, ForeignKey('student.id', ondelete='CASCADE'))
    correct = Column(Boolean)

if __name__ == "__main__":
    user = User(username='Ivan', email='gaga@trat.com')
    from sqlalchemy.orm import sessionmaker

    Session = sessionmaker(autoflush=False)
    sess = Session(bind=engine)
    sess.add(user)
    sess.commit()
    print(user.id)
