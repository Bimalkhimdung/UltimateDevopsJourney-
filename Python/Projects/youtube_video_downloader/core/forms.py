from django import forms

class YouTubeDownloadForm(forms.Form):
    url = forms.URLField(label="YouTube Video URL", widget=forms.URLInput(attrs={"placeholder": "Enter YouTube Video URL"}))

