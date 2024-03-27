from django import forms
from store.models import Review, Reply, Contact, Subscriber


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


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ("name", "email", "subject", "message")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "subject": forms.TextInput(attrs={"placeholder": "Subject"}),
            "message": forms.Textarea(attrs={"placeholder": "Write your message here"}),
        }


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ("email",)
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control me-1",
                    "type": "search",
                    "placeholder": "Enter your email",
                    "aria-label": "Search",
                }
            ),
        }
