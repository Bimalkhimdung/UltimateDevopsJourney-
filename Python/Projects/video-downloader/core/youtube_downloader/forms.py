from django import forms

class YouTubeDownloadsForm(forms.Form):
    url = forms.URLField(label="YouTube Video URL", widget=forms.URLInput(attrs={"placeholder": "Enter Youtube URL"}))
