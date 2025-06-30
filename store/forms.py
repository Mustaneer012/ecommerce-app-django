from django import forms
from .models import ReviewRating  # Ensure this import matches your model's location


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating  # This should be set to the ReviewRating model
        fields = ['subject', 'review', 'rating']

    # def __init__(self, *args, **kwargs):
    #     super(ReviewForm, self).__init__(*args, **kwargs)
    #     self.fields['subject'].widget.attrs.update({'placeholder': 'Enter subject'})
    #     self.fields['review'].widget.attrs.update({'placeholder': 'Write your review here'})
    #     self.fields['rating'].widget.attrs.update({'class': 'rating-input'})
