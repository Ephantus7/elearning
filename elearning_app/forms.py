from django.forms import ModelForm
from .models import AssignmentUploads, AssignmentScores, Assignment, Book, Video, PastPaper
from django import forms
from django.contrib.admin import widgets
from embed_video.fields import EmbedVideoFormField
from django.contrib.auth.forms import AuthenticationForm

class AssignmentUploadForm(ModelForm):
    class Meta:
        model = AssignmentUploads
        fields = ['finished_assignment_file']

        widgets = {
            'finished_assignment_file': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Upload Assignment'
                }
            ),
        }


class AssignmentScoreForm(ModelForm):
    class Meta:
        model = AssignmentScores
        fields = ['score']

        widgets = {
            'score': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Score'
                    ''
                }
            ),
        }
        
        
class NewAssignmentForm(ModelForm):

    class Meta:
        model = Assignment
        
        fields = [
            'guideline1',  'guideline2', 'guideline3', 'guideline4', 'guideline5',
            
            'assignment_name', 'category', 'description', 'topic', 'course',
            'subject', 'assignment_file', 'deadline_date', 'deadline_time',
        ]
        
        widgets = {
            'guideline1': forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'placeholder': 'Guideline 1',
                    'data-toggle': 'tooltip', 
                    'data-html': 'true',
                    'title': 'Enter the first guideline',
                }   
            ),
            
            'guideline2': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Guideline 2',
                    'data-toggle': 'tooltip',
                    'data-html': 'true',
                    'title': 'Enter the second guideline',
                }   
            ),
            
            'guideline3': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Guideline 3',
                    'data-toggle': 'tooltip',
                    'data-html': 'true',
                    'title': 'Enter the third guideline',
                    
                }   
            ),
            
            'guideline4': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Guideline 4',
                    'data-toggle': 'tooltip',
                    'data-html': 'true',
                    'title': 'Enter the fourth guideline',
                    
                }   
            ),
            
            'guideline5': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Guideline 5',
                    'data-toggle': 'tooltip',
                    'data-html': 'true',
                    'title': 'Enter the fifth guideline',
            
                }   
            ),
            
            'assignment_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Assignment Name',
                    'data-toggle': 'tooltip',
                    'data-html': 'true',
                    'title': 'Enter the assignment name',
                    'required': 'true',
                }
            ),
            
            'course': forms.Select(
                attrs={
                    'class': 'form-select',
                    'placeholder': 'Course',
                    'data-toggle': 'tooltip',
                    'data-html': 'true',
                    'title': 'Select the assignment course',
                    'required': 'true',
                }
            ),
            
            'subject': forms.Select(
                attrs={
                    'class': 'form-select',
                    'placeholder': 'Subject',
                    'data-toggle': 'tooltip',
                    'data-html': 'true',
                    'title': 'Select the assignment subject',
                }
            ),
            
            'category': forms.Select(
                attrs={
                    'class': 'form-select',
                    'placeholder': 'Category',
                    'data-toggle': 'tooltip',
                    'data-html': 'true',
                    'title': 'Select the assignment category',
                }
            ),
            
            'description': forms.Textarea(
                attrs={
                    'style': 'height: 100px',
                    'class': 'form-control',
                    'placeholder': 'Description',
                    'data-toggle': 'tooltip',
                    'data-html': 'true',
                    'title': 'Enter the assignment description',
                }
            ),
            
            'topic': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Topic',
                    'data-toggle': 'tooltip',
                    'data-html': 'true',
                    'title': 'Enter the assignment topic',
                }
            ),
            
            'assignment_file': forms.FileInput(
                attrs={
                    'type': 'file',
                    'id': 'formFile',
                    'class': 'form-control',
                    'placeholder': 'Assignment File',
                    'data-toggle': 'tooltip',
                    'data-html': 'true',
                    'title': 'Upload the assignment file',
                }
            ),
            
            'deadline_date': forms.DateInput(
                
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'tooltip': 'Enter the deadline date',
                    'data-toggle': 'tooltip',
                    'data-html': 'true',
                    'title': 'Enter the deadline date',
                }
            ),
            
            'deadline_time': forms.TimeInput(
                
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                    'tooltip': 'Enter the deadline time',
                    'data-toggle': 'tooltip',
                    'data-html': 'true',
                    'title': 'Enter the deadline time',
                }
            ),        
        }   
        

class NewBookForm(ModelForm):
    
    class Meta:
          model = Book
          
          fields = [ 'book_title', 'book_image', 'course', 'subject', 'book_description', 'book_file'] 
          
          widgets = {
              'book_title': forms.TextInput(
                  attrs={
                      'type': 'text', 'class': 'form-control', 'placeholder': 'Book Title', 'data-toggle': 'tooltip',
                      'data-html': 'true', 'title': 'Enter the book title',
                  }
              ), 
              
              'book_image': forms.FileInput(
                  attrs={
                      'type': 'file', 'class': 'form-control', 'placeholder': 'Book Image', 'data-toggle': 'tooltip',
                        'data-html': 'true', 'title': 'Upload the book image',
                    }
                ),
              
                'course': forms.Select(
                    attrs={
                        'class': 'form-select', 'placeholder': 'Course', 'data-toggle': 'tooltip',
                        'data-html': 'true', 'title': 'Select the book course',
                    }
                ),
                
                'subject': forms.Select(
                    attrs={
                        'class': 'form-select', 'placeholder': 'Subject', 'data-toggle': 'tooltip',
                        'data-html': 'true', 'title': 'Select the book subject',
                    }
                ),
                
                'book_description': forms.Textarea(
                    attrs={
                        'style': 'height: 100px', 'class': 'form-control', 'placeholder': 'Book Description', 'data-toggle': 'tooltip',
                        'data-html': 'true', 'title': 'Enter the book description',
                    }
                ),
                
                'book_file': forms.FileInput(
                    attrs={
                        'type': 'file', 'class': 'form-control', 'placeholder': 'Book File', 'data-toggle': 'tooltip',
                        'data-html': 'true', 'title': 'Upload the book file',
                    }
                ),
                
            }
          
          
class NewPastPaperForm(ModelForm):
    
    class Meta:
        model = PastPaper
        
        fields = [ 'course', 'subject', 'paper_year', 'paper', 'paper_title' ]
        
        widgets = {
            'course': forms.Select(
                attrs={
                    'class': 'form-select', 'placeholder': 'Course', 'data-toggle': 'tooltip', 
                    'data-html': 'true', 'title': 'Select the past paper course',
                }
            ),
            
            'subject': forms.Select(
                attrs={
                    'class': 'form-select', 'placeholder': 'Subject', 'data-toggle': 'tooltip',
                    'data-html': 'true', 'title': 'Select the past paper subject',
                }
            ),
            
            'paper_title': forms.TextInput(
                attrs={
                    'type': 'text', 'class': 'form-control', 'placeholder': 'Paper Title', 'data-toggle': 'tooltip',
                    'data-html': 'true', 'title': 'Enter the past paper title',
                }
            ),   
            
             'paper_year': forms.DateInput(
                
                attrs={
                    'type': 'date', 'class': 'form-control', 'tooltip': 'Enter the past paper year',
                    'data-toggle': 'tooltip', 'data-html': 'true', 'title': 'Enter the past paper year',
                }
            ),
             
             'paper': forms.FileInput(
                    attrs={
                        'type': 'file', 'class': 'form-control', 'placeholder': 'Past Paper', 'data-toggle': 'tooltip',
                        'data-html': 'true', 'title': 'Upload the past paper',
                    }
                ),
        }
        

class NewVideoForm(ModelForm):
    
    class Meta:
        
        model = Video
        
        fields = [ 'course', 'subject', 'video_title', 'video_description', 'video' ]
        
        widgets = {
            'course': forms.Select(
                attrs={
                    'class': 'form-select', 'placeholder': 'Course', 'data-toggle': 'tooltip',
                    'data-html': 'true', 'title': 'Select the video course',
                }
            ),
            
            'subject': forms.Select(
                attrs={
                    'class': 'form-select', 'placeholder': 'Subject', 'data-toggle': 'tooltip',
                    'data-html': 'true', 'title': 'Select the video subject',
                }
            ),
            
            'video_title': forms.TextInput(
                attrs={
                    'type': 'text', 'class': 'form-control', 'placeholder': 'Video Title', 'data-toggle': 'tooltip',
                    'data-html': 'true', 'title': 'Enter the video title',
                }
            ),
            
            'video_description': forms.Textarea(
                attrs={
                    'style': 'height: 100px', 'class': 'form-control', 'placeholder': 'Video Description', 'data-toggle': 'tooltip',
                    'data-html': 'true', 'title': 'Enter the video description',
                }
            ),
                        
        }
          
            