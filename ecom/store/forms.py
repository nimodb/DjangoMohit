from django import forms
from store.models import Product
from members.models import Review, Reply


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.NumberInput(attrs={"class": "form-control"}),
            "comment": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Leave a comment here"}
            ),
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Leave a message here"}
            ),
        }
