from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

from datetime import datetime, timedelta

# initialising the parent class for a table
Base = declarative_base()


# a task table
class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())
    date = Column(Date, default=datetime.today())

    def __repr__(self):
        """
        it will look like this format
        id. task
        id. task
        id. task
        """
        return f"{self.id}. {self.task}"


class ToDoList:
    prompt = "1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add a task\n6) Delete a task\n0) Exit\n"

    def __init__(self, db_name):
        """
        initialising the database and gui
        """
        # table and database initialising
        self.choice = None
        self.engine = create_engine(f"sqlite:///{db_name}.db?check_same_thread=False")
        Base.metadata.create_all(self.engine)

        # Session and interaction with database initialising
        self.session = sessionmaker(bind=self.engine)()

        # list gui initialising
        self.today = datetime.today()
        self.choices = {'1': self.show_tasks, '5': self.add_task, '6':self.delete_task, '0': self.shutdown}
        self.running = True
        self.main()

    def shutdown(self):
        """
        shuts down the program, by terminating the while loop
        """
        self.running = False

    def show_tasks(self):
        """
        acquires all the records in the database

        if there are no tasks:
            it will prompt it

        if there are tasks:
            it will print them one by one, in an appropriate format
        """
        if self.choice == '1':
            self.today_tasks()

        elif self.choice == '2':
            self.weeks_tasks()

        elif self.choice == '3':
            self.all_tasks()

        elif self.choice == '4':
            self.missed_tasks()

    def today_tasks(self):
        tasks = self.session.query(Task).filter(Task.date == self.today.date()).all()

        print(f'Today {self.today.strftime("%d %b")}:')
        if tasks:
            for task in tasks:
                print(task)
        else:
            print("Nothing to do!")

    def weeks_tasks(self):
        end_day = self.today + timedelta(days=7)
        task_day = self.today.date()  # Convert to date object

        while task_day != end_day.date():  # Also convert end_day to date object
            tasks = self.session.query(Task).filter(Task.deadline == task_day).all()

            print(f'{task_day.strftime("%A %#d %b")}:')
            if tasks:
                for task in tasks:
                    print(task)
            else:
                print("Nothing to do!")
            print()
            task_day += timedelta(days=1)  # You can use the += operator for incrementing

    def all_tasks(self):
        tasks = self.session.query(Task).order_by(Task.deadline).all()
        print("All tasks:")
        if tasks:
            for task in tasks:
                print(f'{task}. {task.deadline.strftime("%#d %b")}')
        else:
            print("Nothing to do!")

    def missed_tasks(self):
        missed_tasks = self.session.query(Task).filter(Task.deadline < self.today.date()).order_by(Task.deadline).all()
        if missed_tasks:
            print("Missed tasks:")
            for task in missed_tasks:
                print(task)
        else:
            print("All tasks have been completed!")

    def add_task(self, deadline=None):
        """
        adds a task to the database
        """
        task = input('Enter a task\n')
        deadline = input('Enter a deadline\n')
        deadline = datetime.strptime(deadline, '%Y-%m-%d')
        self.session.add(Task(task=task, deadline=deadline, date=self.today))
        self.session.commit()
        print("The task has been added!")

    def delete_task(self):
        tasks = self.session.query(Task).order_by(Task.deadline).all()
        if tasks:
            print("Choose the number of the task you want to delete:")
            for idx, task in enumerate(tasks, start=1):
                print(f"{idx}. {task}")
            task_number = int(input()) - 1
            if 0 <= task_number < len(tasks):
                task_to_delete = tasks[task_number]
                self.session.delete(task_to_delete)
                self.session.commit()
                print("The task has been deleted!")
            else:
                print("Invalid task number!")
        else:
            print("Nothing to delete!")

    def main(self):
        """
        continuously runs the program

        the two print statements, are for line breaks, to maintain proper format of CMD Gui
        lambda: None defines a function that does nothing, as such, if wrong input was entered, it would simply go to the next iteration of the while loop
        if choice != '0' represents the exit input, then the linebreak is replaced by a "Bye!"
        """
        while self.running:
            self.choice = input(self.prompt)
            if self.choice == '1' or self.choice == '2' or self.choice == '3' or self.choice == '4':
                choice = '1'
            else:
                choice = self.choice
            print()
            self.choices.get(choice, lambda: None)()
            print() if choice != '0' else print('Bye!')


ToDoList('todo')
