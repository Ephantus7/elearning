from django import forms
from django.forms.widgets import RadioSelect, Textarea
from .models import MCQuestion, Question, Quiz
from django.forms import ModelForm
from django.contrib.admin import widgets



class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        choice_list = [x for x in question.get_answers_list()]
        self.fields["answers"] = forms.ChoiceField(choices=choice_list,
                                                   widget=RadioSelect)


class QuizAddForm(ModelForm):
    class Meta:
        model = Quiz
        fields = [
            'course', 'subject', 'title', 'description', 'url', 'category',
            'random_order', 'max_questions', 'answers_at_end', 'exam_paper',
            'single_attempt', 'pass_mark', 'success_text', 'fail_text', 'draft'
        ]
        
        widgets = {
             'course': forms.Select(
                 attrs={
                        'class': 'form-select', 'placeholder': 'Course', 'data-toggle': 'tooltip', 'data-html': 'true',
                        'title': 'Select a course for this quiz'
                 }
             ),
             
             'subject': forms.Select(
                 attrs={
                        'class': 'form-select', 'placeholder': 'Subject', 'data-toggle': 'tooltip', 'data-html': 'true',
                        'title': 'Select a subject for this quiz'
                 }
             ),
             
             'title': forms.TextInput(
                    attrs={
                        'class': 'form-control', 'placeholder': 'Title', 'data-toggle': 'tooltip', 'data-html': 'true',
                        'title': 'Enter a title for this quiz'
                    }
                ),
             
             'questions': forms.SelectMultiple(
                    attrs={
                        'class': 'form-select', 'placeholder': 'Questions', 'data-toggle': 'tooltip', 'data-html': 'true',
                        'title': 'Select questions for this quiz'
                    }
                ),
             
             'description': forms.Textarea(
                    attrs={
                        'class': 'form-control', 'placeholder': 'Description', 'data-toggle': 'tooltip', 'data-html': 'true',
                        'title': 'Enter a description for this quiz'
                    }
                ),
             'url': forms.TextInput(
                    attrs={
                        'class': 'form-control', 'placeholder': 'URL', 'data-toggle': 'tooltip', 'data-html': 'true',
                        'title': 'Enter a URL for this quiz'
                    }
                ),
             
            'category': forms.Select(
                    attrs={
                        'class': 'form-select', 'placeholder': 'Category', 'data-toggle': 'tooltip', 'data-html': 'true',
                        'title': 'Select a category for this quiz'
                    }
                ),
            
            'random_order': forms.CheckboxInput(
                    attrs={
                        'class': 'form-check-input', 'placeholder': 'Random Order', 'data-toggle': 'tooltip', 'data-html': 'true',
                        'title': 'Select this option to randomize the order of questions in this quiz'
                    }
                ),
            
            'max_questions': forms.NumberInput(
                    attrs={
                        'class': 'form-control', 'placeholder': 'Max Questions', 'data-toggle': 'tooltip', 'data-html': 'true',
                        'title': 'Enter the maximum number of questions for this quiz'
                    }
                ),
            
            'answers_at_end': forms.CheckboxInput(
                    attrs={
                        'class': 'form-check-input', 'placeholder': 'Answers at End', 'data-toggle': 'tooltip', 'data-html': 'true',
                        'title': 'Select this option to display the answers at the end of this quiz'
                    }
                ),
            
            'exam_paper': forms.CheckboxInput(
                    attrs={
                        'class': 'form-check-input', 'placeholder': 'Exam Paper', 'data-toggle': 'tooltip', 'data-html': 'true',
                        'title': 'Select this option to display this quiz as an exam paper'
                    }
                ),
            
            'single_attempt': forms.CheckboxInput(
                    attrs={
                        'class': 'form-check-input', 'placeholder': 'Single Attempt', 'data-toggle': 'tooltip', 'data-html': 'true',
                        'title': 'Select this option to allow only a single attempt at this quiz'
                    }
                ),
            
            'pass_mark': forms.NumberInput(
                    attrs={
                        'class': 'form-control', 'placeholder': 'Pass Mark', 'data-toggle': 'tooltip', 'data-html': 'true',
                        'title': 'Enter the pass mark for this quiz'
                    }
                ),
            
            'success_text': forms.Textarea(
                    attrs={
                        'class': 'form-control', 'placeholder': 'Success Text', 'data-toggle': 'tooltip', 'data-html': 'true',
                        'title': 'Enter the success text for this quiz'
                    }
                ),
            
            'fail_text': forms.Textarea(
                    attrs={
                        'class': 'form-control', 'placeholder': 'Fail Text', 'data-toggle': 'tooltip', 'data-html': 'true',
                        'title': 'Enter the fail text for this quiz'
                    }
                ),
            
            'draft': forms.CheckboxInput(
                    attrs={
                        'class': 'form-check-input', 'placeholder': 'Draft', 'data-toggle': 'tooltip', 'data-html': 'true',
                        'title': 'Select this option to save this quiz as a draft'
                    }
                ),
        }
            