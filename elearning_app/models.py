from django.db import models
from django.contrib.auth.models import AbstractUser
from embed_video.fields import EmbedVideoField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import reverse


USER_TYPE_CHOICES = (
    (1, 'Admin'),
    (2, 'Teacher'),
    (3, 'Student'),
)

STATUS_CHOICES = (
    (1, 'Read'),
    (2, 'Unread'),
)


class CustomUser(AbstractUser):
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=3)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)


class Course(models.Model):
    course_code = models.IntegerField()
    course_name = models.CharField(max_length=200)
    course_description = models.TextField(max_length=1024, null=True)
    course_duration = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.course_name
    
    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'pk': self.pk})


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    stud_number = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    stud_phone = models.IntegerField()
    stud_linkedin = models.URLField(null=True, blank=True)
    stud_whatsapp = models.URLField(null=True, blank=True)
    stud_facebook = models.URLField(null=True, blank=True)
    stud_instagram = models.URLField(null=True, blank=True)
    stud_twitter = models.URLField(null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
    
    def get_absolute_url(self):
        return reverse('student_detail', kwargs={'pk': self.pk})


class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    course = models.ManyToManyField(Course)
    teacher_phone = models.IntegerField()
    objects = models.Manager()

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
    
    def get_absolute_url(self):
        return reverse('teacher_profile', kwargs={'pk': self.pk})


class Subject(models.Model):
    subject_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=200)
    subject_code = models.IntegerField()
    subject_description = models.TextField(max_length=1024)
    date_created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return self.subject_name


class AssignmentCategory(models.Model):
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "Assignment Categories"


class Assignment(models.Model):
    guideline1 = models.CharField(max_length=200)
    guideline2 = models.CharField(max_length=200)
    guideline3 = models.CharField(max_length=200, blank=True)
    guideline4 = models.CharField(max_length=200, blank=True)
    guideline5 = models.CharField(max_length=200, blank=True)

    GUIDELINES = (
        ("A", guideline1),
        ("B", guideline2),
        ("C", guideline3),
        ("D", guideline4),
        ("E", guideline5),
    )

    assignment_name = models.CharField(max_length=200)
    category = models.ForeignKey(AssignmentCategory, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    description = models.TextField(max_length=1024)
    topic = models.CharField(max_length=200)
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assignment_file = models.FileField(upload_to='assignments')
    deadline_date = models.DateField()
    deadline_time = models.TimeField()
    objects = models.Manager()
    
    class Meta:
        get_latest_by = 'updated_at'

    def __str__(self):
        return self.assignment_name

    def get_student_uploads(self):
        return self.assignmentuploads_set.all()

    def get_student_scores(self):
        return self.assignmentscores_set.all()

    def get_student_count(self):
        return self.get_student_uploads().count()

    def get_absolute_url(self):
        return reverse('assignment_details', kwargs={'pk': self.pk})


class AssignmentUploads(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    finished_assignment_file = models.FileField(upload_to='assignment/uploads')
    date_uploaded = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        verbose_name_plural = "Assignment Uploads"

    def __str__(self):
        return self.assignment.assignment_name

    def assignment_upload_score(self):
        return self.assignmentscores_set.all()

    def get_absolute_url(self):
        return reverse('assignment_details', kwargs={'pk': self.pk})


class AssignmentScores(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    scored_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    upload = models.ForeignKey(AssignmentUploads, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        verbose_name_plural = "Assignment Scores"

    def __str__(self):
        return self.assignment.assignment_name


class PastAssignments(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    finished_assignment_file = models.FileField(upload_to='assignment/uploads')
    date_uploaded = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.assignment.assignment_name


class Book(models.Model):
    book_title = models.CharField(max_length=200)
    book_image = models.ImageField(upload_to='books_thumbnails', blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    book_description = models.TextField(max_length=1024, null=True)
    book_file = models.FileField(upload_to="books")
    date_added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    objects = models.Manager()
    
    class Meta:
        get_latest_by = 'date_added'
        ordering = ['-date_added']

    def __str__(self):
        return self.book_title
    

class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, help_text="Select the course the video belongs to")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, help_text="Select the subject the video belongs to")
    video_title = models.CharField(max_length=200, help_text="Enter the title of the video")
    video_description = models.TextField(max_length=1024, null=True, help_text="Enter a short description of the video")
    date_added = models.DateTimeField(auto_now_add=True, help_text="Enter the date the video was added")
    added_by = models.ForeignKey(Teacher, on_delete=models.CASCADE, help_text="Select the teacher who added the video")
    video = EmbedVideoField(help_text="Enter the video link")
    objects = models.Manager() 

    class Meta:
        get_latest_by = 'date_added'

    def __str__(self) -> str:
        return self.video_title
    

class PastPaper(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    paper_year = models.DateField()
    paper_title = models.CharField(max_length=200)
    paper = models.FileField(upload_to="pastpapers")
    date_added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    objects = models.Manager()
    
    class Meta:
        get_latest_by = 'date_added'

    def __str__(self) -> str:
        return self.paper_title
